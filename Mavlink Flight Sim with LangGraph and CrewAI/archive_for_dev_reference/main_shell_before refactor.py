import sys
import os
from dotenv import load_dotenv
import yaml
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Dict
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod

load_dotenv()

# Set model name
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

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
    return state

def should_continue(state: State) -> str:
    return 'planning'

def run():
    print("## Welcome to Mission One Demo")
    print('-------------------------------')

    workflow = StateGraph(State)

    workflow.add_node("planning", planning_node)
    workflow.add_node("ask_human", ask_human)
    workflow.add_node("execute", execute_node)

    workflow.add_edge(START, "planning")

    # Update conditional edges for planning
    workflow.add_conditional_edges(
        "planning",
        should_continue,
        {
            "ask_human": "ask_human",
            "execute": "execute"  # Direct transition to execute if conditions are met
        }
    )

    # Direct transition from ask_human back to planning
    workflow.add_edge("ask_human", "planning")

    workflow.add_edge("execute", END)

    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory, interrupt_before=["ask_human"])

    # Display the graph as a PNG
    display(Image(
        app.get_graph().draw_mermaid_png(
            curve_style=CurveStyle.LINEAR,
            wrap_label_n_words=9,
            draw_method=MermaidDrawMethod.API,
            background_color="white",
            padding=10,
        )
    ))

    # Save the PNG to a file
    png_filename = "workflow_graph.png"
    with open(png_filename, "wb") as f:
        f.write(app.get_graph().draw_mermaid_png(
            curve_style=CurveStyle.LINEAR,
            wrap_label_n_words=9,
            draw_method=MermaidDrawMethod.API,
            background_color="white",
            padding=10,
        ))
    
    print(f"Workflow graph saved as {png_filename}")


if __name__ == "__main__":
    run()
