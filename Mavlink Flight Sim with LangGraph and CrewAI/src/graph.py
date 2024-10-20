from typing import Literal
from langgraph.graph import StateGraph, START, END

#import the nodes
from graph.graph_nodes.planning import planning
from graph.graph_nodes.ask_mission_feedback import ask_mission_feedback
from graph.graph_nodes.execute import execute
from graph.graph_nodes.human_mission_input import human_mission_input
from graph.graph_nodes.load_sample_mission import load_sample_mission

#import the missionState: central data structure
from graph.missionState import MissionState

#routing functions
#this is the routing function for the human_mission_input node
#it determines whether we load a sample mission or continue planning
#all routing functions are similar in logic
def route_human_mission_input(state: MissionState) -> Literal["load_sample_mission", "planning"]:
    if state.get('mission'):
        return "planning"
    else:
        return "load_sample_mission"

def route_load_sample_mission(state: MissionState) -> Literal["planning"]:
    return "planning"

def route_planning(state: MissionState) -> Literal["ask_mission_feedback", "execute"]:
    if state['user_feedback'] == 'continue':
        return 'execute'
    else:
        return 'ask_mission_feedback'

def route_ask_mission_feedback(state: MissionState) -> Literal["planning", "human_mission_input", "execute"]:
    if state['user_feedback'] == 'continue':
        return "execute"
    elif state['user_feedback'] == 'restart':
        return "human_mission_input"
    else:
        return "planning"

#create the workflow/graph
def create_workflow():
    workflow = StateGraph(MissionState)

    workflow.add_node("human_mission_input", human_mission_input)
    workflow.add_node("load_sample_mission", load_sample_mission)
    workflow.add_node("planning", planning)
    workflow.add_node("ask_mission_feedback", ask_mission_feedback)
    workflow.add_node("execute", execute)

    workflow.add_edge(START, "human_mission_input")
    workflow.add_conditional_edges("human_mission_input", route_human_mission_input)
    workflow.add_edge("load_sample_mission", "planning")
    workflow.add_conditional_edges("planning", route_planning)
    workflow.add_conditional_edges("ask_mission_feedback", route_ask_mission_feedback)
    workflow.add_edge("execute", END)

    app = workflow.compile()
    return app


# def run_workflow(app, initial_state):
#     # Run the workflow/graph
#     result = app.invoke(initial_state)
#     print(result)

    #########################################################
    #this is how you would run the workflow where you have 1 instance of human input
    #it seemed weird that I could only run the workflow once and give it human input once
    #i created the work around using a crewAI crew to take input instead and ensure we could
    #give more robust instruction and do it multiple times

    #keeping this code for reference if we find a better way in the future
    #########################################################

    #memory = MemorySaver()

    # for event in app.stream(initial_state, thread, stream_mode="values"):
    #     print(event)
    #app = workflow.compile(checkpointer=memory, interrupt_after=["ask_human"])

    # initial_input = {"user_feedback": "continue planning"}

    # # Thread
    # thread = {"configurable": {"thread_id": "1"}}

    # # Run the graph until the first interruption
    # for event in app.stream(initial_input, thread, stream_mode="values"):
    #     print(event)

    # # Get actual human input
    # try:
    #     user_input = input("Tell me how you want to update the state: ")
    # except:
    #     user_input = "continue planning!"

    # # Update the state as if we are the human_feedback node
    # app.update_state(thread, {"user_feedback": user_input}, as_node="ask_human")

    # # Check the state
    # print("--State after update--")
    # print(app.get_state(thread))

    # # Continue the graph execution
    # for event in app.stream(None, thread, stream_mode="values"):
    #     print(event)


    #human input

