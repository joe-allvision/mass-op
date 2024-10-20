from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Dict
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod
from langgraph.checkpoint.memory import MemorySaver
from crews import FeedbackCrew, PlanningCrew
import ast
from flight_sim_interaction import fly

#input should be more descriptive
#TODO: add waypoint_dict to state, it will be used by the execute node
class State(TypedDict):
    mission: str
    user_feedback: str
    waypoint_dict: List[List[float]]


def planning_node(state: State) -> State:
    print("Planning node")
    
    # there is probably a better way to do this, such as connecting directly from human input to execution
    # however I tried to design human input crew to be more flexible and robust for future use
    
    # checks if user feedback is not continue, meaning it should continue planning
    if state["user_feedback"] != "continue":
        # Create the crew and kickoff, ensure feedback is incorporated into the plan
        planning_crew = PlanningCrew().crew()
        #TODO: look for ways to pass the state between crews. right now these inputs are just sent as strings
        plan_output = planning_crew.kickoff(inputs={
            "mission": state['mission'],
            "mission_simple": "Fly to Brooklyn Bridge",
            "user_feedback": state['user_feedback'],
            "previous_waypoints": state['waypoint_dict']
        })
        print(plan_output)

        waypoint_dict = plan_output.raw
        waypoint_dict = ast.literal_eval(waypoint_dict)
        state['waypoint_dict'] = waypoint_dict
    else:
        print("Skipping planning node as user feedback is 'continue'")
    #sets feedback to no feedback?
    return state

def execute_node(state: State) -> State:
    print("Executing plan")
    fly(state['waypoint_dict'])
    return state

# blank node -> human input actually occurs in workflow. this node is important because 
# the interupt_before is set to this node, meaning the workflow will run until this node is reached
# then the workflow will resume from this node when human input is detected
def ask_human(state: State) -> State:
    print("Asking human for input")
    user_feedback = 'Please Input User Feedback'
    feedback_crew = FeedbackCrew().crew()
    result = feedback_crew.kickoff(inputs={'feedback': user_feedback})
    print(result)

    state['user_feedback'] = result.raw
    return state

def should_continue(state: State) -> str:
    # if the feedback is next node it will still pass through to planning first
    # planning will execute again -> temp fix is a check at the start of planning node
    print("should continue")
    if state['user_feedback'] == 'continue':
        return 'execute'
    else:
        return 'ask_human'

def create_workflow(initial_state: dict):
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
    app = workflow.compile()


    #run the workflow/graph
    result = app.invoke(initial_state) 
    print(result)

    #########################################################
    #this is how you would run the workflow where you have 1 instance of human input
    #it seemed weird that I could only run the workflow once and give it human input once
    #i created the work around using a crewAI crew to take input instead and ensure we could
    #give more robust instruction and do it multiple times

    #keeping this code for reference if we find a better way in the future
    #########################################################


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

    return app
