import os
from dotenv import load_dotenv
from graph import create_workflow
from graph_utils import display_and_save_graph
import yaml

load_dotenv()

# Set model name
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

def run():
    print("## Welcome to MavLink Flight Sim Demo Through LangGraph-CrewAI Integration")
    print('-------------------------------')

    #gather any mission parameters
    with open('src/mission_input.yaml', 'r') as file:
        mission_config = yaml.safe_load(file)

    mission = mission_config['mission']

    #5 random waypoints to make errors clear
    example_waypoint_dict = [
        [34.052235, -118.243683, 100],  # Los Angeles, USA
        [51.507351, -0.127758, 200],    # London, UK
        [35.689487, 139.691711, 300],    # Tokyo, Japan
        [-33.448376, -70.769402, 150],   # Santiago, Chile
        [55.755825, 37.617298, 250],     # Moscow, Russia
    ]

    initial_state = {
        "mission": mission,
        "user_feedback": "No Feedback",
        "waypoint_dict": example_waypoint_dict,
        "has_gotten_feedback": False
    }

    #create the workflow/graph
    app = create_workflow()

    #run the workflow/graph
    result = app.invoke(initial_state)

    # way to display the graph, comment out if not needed
    display_and_save_graph(app)
    
    #print(final_state)

if __name__ == "__main__":
    run()
