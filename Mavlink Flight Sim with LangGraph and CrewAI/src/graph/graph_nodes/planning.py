from missionState import MissionState
from crewAI_crews.crews import PlanningCrew
import ast

def planning(state: MissionState) -> MissionState:
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
            "user_feedback": state['user_feedback'],
        })

        # print(plan_output)

        # print(f"Printing Plan Output Tasks: {plan_output.tasks_output}")

        waypoint_dict = plan_output.raw
        waypoint_dict = ast.literal_eval(waypoint_dict)
        state['waypoint_dict'] = waypoint_dict

    else:
        print("Skipping planning node as user feedback is 'continue'")
    #sets feedback to no feedback?
    return state
