import functools
import operator
from typing import Annotated, Literal, Sequence, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode

import flight_roles
import flight_tools

load_dotenv()


# This defines the object that is passed between each node
# in the graph. We will create different nodes for each agent and tool
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str


def create_agent(llm, tools, system_message: str):
    """Create an agent."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                flight_roles.agent_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    return prompt | llm.bind_tools(tools, tool_choice="any")


# Helper function to create a node for a given agent
def agent_node(state, agent, name):
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        # Since we have a strict workflow, we can
        # track the sender so we know who to pass to next.
        "sender": name,
    }


def router(state) -> Literal["call_tool", "__end__", "continue"]:
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        # The previous agent is invoking a tool
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return "__end__"
    return "continue"


llm = ChatOpenAI(model="gpt-4o", max_tokens=200, temperature=0.5)
# llm = llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

pilot = create_agent(
    llm,
    [flight_tools.radio, flight_tools.operate_systems],
    system_message=flight_roles.pilot_role,
)
pilot_node = functools.partial(agent_node, agent=pilot, name="Pilot")

# chart_generator
ground_control = create_agent(
    llm,
    [flight_tools.radio, flight_tools.operate_systems],
    system_message=flight_roles.gc_role,
)
gc_node = functools.partial(agent_node, agent=ground_control, name="GC")

# copilot
copilot = create_agent(
    llm,
    [flight_tools.radio, flight_tools.operate_systems],
    system_message=flight_roles.copilot_role,
)
copilot_node = functools.partial(agent_node, agent=copilot, name="Co-Pilot")

# search_operator
search_operator = create_agent(
    llm,
    [flight_tools.radio, flight_tools.operate_systems],
    system_message=flight_roles.search_operator_role,
)
search_operator_node = functools.partial(
    agent_node, agent=search_operator, name="Search Operator"
)

workflow = StateGraph(AgentState)

workflow.add_node("Pilot", pilot_node)
workflow.add_node("GC", gc_node)
workflow.add_node("Co-Pilot", copilot_node)
tools = [flight_tools.radio, flight_tools.operate_systems]
tool_node = ToolNode(tools)
workflow.add_node("call_tool", tool_node)
workflow.add_node("Search Operator", search_operator_node)

# the params are: 'from', 'to', 'condition'
workflow.add_conditional_edges(
    "Co-Pilot",
    router,
    {"continue": "Pilot", "call_tool": "call_tool", "__end__": END},
)
workflow.add_conditional_edges(
    "GC",
    router,
    {"continue": "Co-Pilot", "call_tool": "call_tool", "__end__": END},
)
workflow.add_conditional_edges(
    "Pilot",
    router,
    {"continue": "GC", "call_tool": "call_tool", "__end__": END},
)
workflow.add_conditional_edges(
    "Search Operator",
    router,
    {"continue": "Pilot", "call_tool": "call_tool", "__end__": END},
)

workflow.add_conditional_edges(
    "call_tool",
    # Each agent node updates the 'sender' field
    # the tool calling node does not, meaning
    # this edge will route back to the original agent
    # who invoked the tool
    lambda x: x["sender"],
    {
        "Pilot": "Pilot",
        "GC": "GC",
        "Co-Pilot": "Co-Pilot",
        "Search Operator": "Search Operator",
    },
)
workflow.add_edge(START, "GC")
graph = workflow.compile()


events = graph.stream(
    {
        "messages": [
            HumanMessage(
                content="Please role play communications of these four actors and the sim for a takeoff sequence from dead stop at the end of the runway just before takeoff to airborne and on course to the first search area.",
            )
        ],
    },
    # Maximum number of steps to take in the graph
    {"recursion_limit": 150},
)

for i, s in enumerate(events, 1):
    key = list(s.keys())[0]
    if key == "call_tool":
        print(
            f"Step{int(i/2)}: {s[key]['messages'][0].name} --> {s[key]['messages'][0].content}"
        )
        print("----")
