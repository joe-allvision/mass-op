from missionState import MissionState
from flight_sim_interaction import fly

def execute(state: MissionState) -> MissionState:
    print("Executing plan")
    fly(state['waypoint_dict'])
    return state

