import operator
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from tic_tac_toe import TicTacToe


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


class Agent:
    """
    A graph consists of:
        * nodes: agents or functions
        * edges: connect nodes
        * conditional edges: decisions of where to go next
    """

    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", ToolNode(tools))
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END},
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state["messages"][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState):
        messages = state["messages"]
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {"messages": [message]}


prompt = """You are a tic-tac-toe player. You can place a token an "X" on the board.
Your opponent places an "O" on the board. You get to start first. 
You can call the tool `llm_move` with the `position` argument where the value is an
integer between 1 and 9, inclusively. An empty board looks like
 | | 
-----
 | | 
-----
 | |

The positions on the board are
1|2|3
-----
4|5|6
-----
7|8|9

If you place an invalid move with the tool call, the tool will tell you, so try another position.
You can also observe the board without making a move. You should oberve the board as your first move.
If you believe you have won the game, call the tool `check_if_llm_won` as the last step
to confirm if you have won.
"""

load_dotenv()
model = ChatOpenAI(model="gpt-3.5-turbo")
# model = ChatOpenAI(model="gpt-4")
# model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

ttt = TicTacToe()
bot = Agent(
    model,
    [tool(ttt.llm_move), tool(ttt.observe_board), tool(ttt.check_if_llm_won)],
    system=prompt,
)

messages = [
    HumanMessage(
        content='Win a game of tic tac toe. You are "X" and your opponent is "O".'
    )
]
for chunk in bot.graph.stream({"messages": messages}, stream_mode="values"):
    chunk["messages"][-1].pretty_print()
