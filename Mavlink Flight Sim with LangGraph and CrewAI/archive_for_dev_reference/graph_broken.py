from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Dict
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    mission: str
    mission_simple: str
    plan: List[Dict[str, float]]
    human_response: str

def planning_node(state: State) -> State:
    print("Planning node")
    return state

def execute_node(state: State) -> State:
    print("Executing plan")
    return state

def ask_human(state: State) -> State:
    print("Asking human for input")
    # Get user input
    try:
        user_input = input("Tell me how you want to update the state: ")
    except:
        user_input = "continue planning"
    # Update the state with the human response
    state['human_response'] = user_input
    return state

def should_continue(state: State) -> str:
    # Decide the next node based on the human response
    if state['human_response'] == 'continue planning':
        return 'planning'
    else:
        return 'execute'

def create_workflow():
    workflow = StateGraph(State)

    workflow.add_node("planning", planning_node)
    workflow.add_node("ask_human", ask_human)
    workflow.add_node("execute", execute_node)

    workflow.add_edge(START, "planning")

    workflow.add_conditional_edges(
        "planning",
        should_continue,
        {
            "ask_human": "ask_human",
            "execute": "execute"
        }
    )

    workflow.add_edge("ask_human", "planning")
    workflow.add_edge("execute", END)

    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory, interrupt_before=["ask_human"])

    return app
