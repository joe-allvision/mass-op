from langchain_core.tools import tool


@tool
def operate_systems(operator: str, action: str, system: str, value: str):
    """
    Use this to operate the aircraft systems.
    'operator' can be any of the following: 'pilot', 'copilot', 'search operator', or 'ground station operator'.
    'action' can be either 'query', 'operate', or 'report'.
    'system' can be any aircraft or ground control system.
    'value' is the value to set the system to, if applicable. if not applicable, set to 'n/a'.
    """
    return {"operator": operator, "action": action, "system": system, "value": value}


@tool
def radio(speaker: str, listener: str, conversation: str):
    """Use this to parse any conversation between the two speakers"""
    return {"speaker": speaker, "listener": listener, "content": conversation}
