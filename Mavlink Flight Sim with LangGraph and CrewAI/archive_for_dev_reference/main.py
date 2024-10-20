import sys
import os
from crews import PlanningCrew
from dotenv import load_dotenv
import yaml
from flight_sim_interaction import fly
import ast
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Dict
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

# Set model name
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

class State(TypedDict):
    mission: str
    mission_simple: str
    plan: List[Dict[str, float]]
    human_response: str

def planning_node(state: State) -> State:
    mission = state['mission']
    mission_simple = state['mission_simple']
    planning_crew = PlanningCrew().crew()
    plan_output = planning_crew.kickoff(inputs={
        "mission": mission,
        "mission_simple": mission_simple,
    })
    #state['plan'] = ast.literal_eval(plan_output.raw)
    state['plan'] = ast.literal_eval(plan_output)
    return state

def execute_node(state: State) -> State:
    print("Executing plan:")
    for waypoint in state['plan']:
        print(f"Latitude: {waypoint['lat']}, Longitude: {waypoint['lon']}, Altitude: {waypoint['alt']}")
    fly(state['plan'])
    return state

def ask_human(state: State) -> State:
    print("Current plan:")
    for waypoint in state['plan']:
        print(f"Latitude: {waypoint['lat']}, Longitude: {waypoint['lon']}, Altitude: {waypoint['alt']}")
    user_input = input("Review the plan. Type 'approve' to proceed or provide modifications: ")
    state['human_response'] = user_input
    return state

def should_continue(state: State) -> str:
    if not state['plan']:
        return 'planning'
    elif state['human_response'].lower() == 'approve':
        return 'execute'
    else:
        return 'ask_human'

def run():
    print("## Welcome to Mission One Demo")
    print('-------------------------------')

    with open('src/mission_input.yaml', 'r') as file:
        mission_config = yaml.safe_load(file)

    mission = mission_config['mission']
    mission_simple = mission_config['mission_simple']

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
            "execute": "execute",
            "planning": "planning"
        }
    )

    workflow.add_conditional_edges(
        "ask_human",
        should_continue,
        {
            "planning": "planning",
            "execute": "execute",
            "ask_human": "ask_human"
        }
    )

    workflow.add_edge("execute", END)

    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory, interrupt_before=["ask_human"])

    inputs = {
        "mission": mission,
        "mission_simple": mission_simple,
        "plan": [],
        "human_response": ""
    }

    config = {"configurable": {"thread_id": "1"}}

    for output in app.stream(inputs, config, stream_mode="values"):
        print(f"Current state: {output}")
        
        if output.get('next') == ['ask_human']:
            # Human input is needed
            user_input = input("Review the plan. Type 'approve' to proceed or provide modifications: ")
            app.update_state(config, {"human_response": user_input}, as_node="ask_human")
        
        if output.get('next') == []:
            print("Mission execution completed.")
            break

if __name__ == "__main__":
    run()
