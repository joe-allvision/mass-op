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

mission_commander = create_agent(
    llm,
    [flight_tools.mavproxy_command, flight_tools.telemetry_request, flight_tools.system_alert, flight_tools.communication],
    system_message=flight_roles.mission_commander_role,
)
mission_commander_node = functools.partial(agent_node, agent=mission_commander, name="Mission_Commander")

# chart_generator
flight_operator= create_agent(
    llm,
    [flight_tools.mavproxy_command, flight_tools.telemetry_request, flight_tools.system_alert, flight_tools.communication],
    system_message=flight_roles.flight_operator_role,
)
flight_operator_node = functools.partial(agent_node, agent=flight_operator, name="Flight_Operator")

# copilot
autopilot_system = create_agent(
    llm,
    [flight_tools.autopilot_status_update, flight_tools.system_alert],
    system_message=flight_roles.autopilot_system_role,
)
autopilot_system_node = functools.partial(agent_node, agent=autopilot_system, name="autopilot_system")

# search_operatoe
systems_analyst = create_agent(
    llm,
    [flight_tools.mavproxy_command, flight_tools.telemetry_request, flight_tools.system_alert, flight_tools.communication],
    system_message=flight_roles.systems_analyst_role,
)
systems_analyst_node = functools.partial(
    agent_node, agent=systems_analyst, name="Systems_analyst"
)

workflow = StateGraph(AgentState)

workflow.add_node("Mission_Commander", mission_commander_node)
workflow.add_node("Flight_Operator", flight_operator_node)
workflow.add_node("autopilot_system", autopilot_system_node)
workflow.add_node("Systems_analyst", systems_analyst_node)
tools = [flight_tools.mavproxy_command, flight_tools.telemetry_request, flight_tools.system_alert, flight_tools.communication, flight_tools.autopilot_status_update]

tool_node = ToolNode(tools)
workflow.add_node("call_tool", tool_node)

# the params are: 'from', 'to', 'condition'
workflow.add_conditional_edges(
    "Mission_Commander",
    router,
    {"continue": "Flight_Operator", "call_tool": "call_tool", "__end__": END},
)
workflow.add_conditional_edges(
    "Flight_Operator",
    router,
    {"continue": "Systems_analyst", "call_tool": "call_tool", "__end__": END},
)
workflow.add_conditional_edges(
    "Systems_analyst",
    router,
    {"continue": "Mission_Commander", "call_tool": "call_tool", "__end__": END},
)
workflow.add_conditional_edges(
    "autopilot_system",
    lambda x: x["sender"],
    {
        "Mission_Commander": "Mission_Commander",
        "Flight_Operator": "Flight_Operator",
        "autopilot_system": "autopilot_system",
        "Systems_analyst": "Systems_analyst",
    },
)

workflow.add_conditional_edges(
    "call_tool",
    # Each agent node updates the 'sender' field
    # the tool calling node does not, meaning
    # this edge will route back to the original agent
    # who invoked the tool
    lambda x: x["sender"],
    {
        "Mission_Commander": "Mission_Commander",
        "Flight_Operator": "Flight_Operator",
        "autopilot_system": "autopilot_system",
        "Systems_analyst": "Systems_analyst",
    },
)
workflow.add_edge(START, "Mission_Commander")
graph = workflow.compile()


events = graph.stream(
    {
        "messages": [
            HumanMessage(
                content="Begin the mission to deliver the package to the specified coordinates: 37.7749, -122.4194",
            )
        ],
    },
    # Maximum number of steps to take in the graph
    {"recursion_limit": 150},
)

'''
for i, s in enumerate(events, 1):
    key = list(s.keys())[0]
    if key == "call_tool":
        print(
            f"Step{i}: {s[key]['messages'][0].name} --> {s[key]['messages'][0].content}"
        )
        print("----")
'''
for s in events:
    print(s)
    print("----")
