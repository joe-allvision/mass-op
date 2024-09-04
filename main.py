import sys
import os
from crews import FlightCrew
from dotenv import load_dotenv
import yaml
load_dotenv()

# change the model name here
os.environ["OPENAI_MODEL_NAME"]="gpt-4o"


def run():
    """
    Run the crew.
    """

    print("## Welcome to Mission One Demo")
    print('-------------------------------')

    with open('src/mission_input.yaml', 'r') as file:
        mission_config = yaml.safe_load(file)

    mission = mission_config['mission']
    rules = mission_config['rules']
    responsibilities = mission_config['responsibilities']
    task_standards = mission_config['task_standards']
    
    mission = input("What is the mission?\n") 

    inputs = {
        "mission": mission,
        "rules": rules,
        "responsibilities": responsibilities,
        "task_standards": task_standards
    }

    game = FlightCrew().crew().kickoff(inputs=inputs)

    print("\n\n################################################")
    print("## Here is the result")
    print("################################################\n")
    print(game)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        FlightCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        FlightCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        FlightCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

run()
