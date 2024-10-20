import sys
import os
from crews import PlanningCrew
from dotenv import load_dotenv
import yaml
from flight_sim_interaction import fly
import ast

load_dotenv()

# Set model name
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

def run():
    """
    Run the crew.
    """
    print("## Welcome to Mission One Demo")
    print('-------------------------------')

    # Load mission configuration from YAML file
    with open('src/mission_input.yaml', 'r') as file:
        mission_config = yaml.safe_load(file)

    mission = mission_config['mission']
    mission_simple = mission_config['mission_simple']

    # Step 1: Execute PlanningCrew to generate the mission plan
    planning_crew = PlanningCrew().crew()
    plan_output = planning_crew.kickoff(inputs={
        "mission": mission,
        "mission_simple": mission_simple,
    })

    the_way= plan_output.raw

    the_way = ast.literal_eval(the_way)
    print(the_way)

    for lat, lon, altitude in the_way:
        print(f"Latitude: {lat}, Longitude: {lon}, Altitude: {altitude}")
    
    fly(the_way)


run()