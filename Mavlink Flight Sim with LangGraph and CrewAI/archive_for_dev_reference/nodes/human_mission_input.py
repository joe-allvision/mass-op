from graph.missionState import MissionState
import yaml
from crewAI_crews.crews import InitialInputCrew

def human_mission_input(state: MissionState) -> MissionState:
    # TODO: Implement logic to get mission input from the user
    if state['has_gotten_feedback']:
        #if the state has gotten feedback but seems to be 
        state['mission'] = state['user_feedback']

        #resets user feedback to no feedback
        state['user_feedback'] = 'No Feedback'
        pass
    else:
        with open('src/mission_input.yaml', 'r') as file:
            mission_config = yaml.safe_load(file)
        print("Available missions:")

        mission_options = []
        for key in mission_config.keys():
            mission_options.append(key)
            print(f"  - {key}")

        human_input = input("Please describe your mission or indicate a loaded situation to continue with: ")
        
        #may be unnecessary -> did to fix yaml error but may have not been necessary
        mission_options = str(mission_options)
        
        user_input_crew = InitialInputCrew().crew()
        result = user_input_crew.kickoff(inputs={'input': human_input, 'mission_options': mission_options})
        print(result)

        user_input_task_output = result.raw
        #if the state is not in the yaml, then it is a new mission
        if user_input_task_output not in mission_config.keys():
            state['mission'] = user_input_task_output
        else:
            state['mission'] = mission_config[user_input_task_output]
    
    return state

