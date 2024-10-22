from graph_contents.missionState import MissionState
from crewAI_crews.crews import FeedbackCrew


#this node currently uses the feedback crew, which is a human in the loop
#the benefit of using this and langgraph is we are able to recieve feedback multiple times
#I wasn't able to directly figure out iterative human in the loop with langgraph
#there is an example in graph.py but that would only get human input once
def ask_mission_feedback(state: MissionState) -> MissionState:
    print("Asking human for input")
    
    #sets temporary feedback to be sent to crew
    #not a perfect solution but it works for now
    user_feedback = 'Please Input User Feedback'
    #creates crew object
    feedback_crew = FeedbackCrew().crew()
    result = feedback_crew.kickoff(inputs={'feedback': user_feedback,
                                           'mission': state['mission'],
                                           'previous_waypoints': state['waypoint_dict']})
    print(result)

    #crew_output.tasks_output.get(task_name)
    task_output = result.tasks_output

    #feedback output is either the feedback or to continue to the next node
    feedback_output = task_output[0].raw
    #mission change output is either 
    mission_change_output = task_output[1].raw

    print(f"Printing Feedback Output: {feedback_output}")
    print(f"Printing Mission Change Task: {mission_change_output}")

    #if the mission output indicates restart then the user feedback is changed to restart
    #in order for the router to send the user back to human_mission_input
    #the feedback now becomes the new mission for the next iteration.
    
    #this logic helps determine where the mission routes to next, it's a bit convoluted but is explained below
    if mission_change_output == 'restart':
        #routing for ask feedback looks at user feedback to determine next step -> therefore we set it's value here to send back to start
        state['user_feedback'] = mission_change_output

        #the new mission will be formed from the feedback
        state['mission'] = feedback_output
    else:
        state['user_feedback'] = feedback_output

    #user feedback changes to true to do the correct logic in human_mission_input
    state['has_gotten_feedback'] = True

    return state
