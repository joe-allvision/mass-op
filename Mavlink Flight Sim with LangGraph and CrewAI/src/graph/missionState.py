from typing import TypedDict, List

class MissionState(TypedDict):
    mission: str
    user_feedback: str
    waypoint_dict: List[List[float]]
    has_gotten_feedback: bool
