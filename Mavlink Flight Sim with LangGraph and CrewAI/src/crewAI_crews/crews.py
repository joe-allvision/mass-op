from crewai import Agent, Crew, Process, Task, Flow
from crewai.project import CrewBase, agent, crew, task
import json
import os
from datetime import datetime
from crewAI_crews.tools.sopSAR import Search_SOPs_In_Depth
from textwrap import dedent

#TODO: need to update tasks to have previous waypoints as input AND make the task output absolutely concretely impossible to mess up
#TODO: hypothesis: currently waypoints, feedback and mission are sent as input it's probable that we could send a state object that 
# contains all of these things, and it would be better for memory and sending back and forth
@CrewBase
class PlanningCrew():
    """Mission Planning Crew"""
    # agents_config = 'src/crewAI_crews/config/planning_agents.yaml'
    # tasks_config = 'src/crewAI_crews/config/planning_tasks.yaml'

    agents_config = 'config/planning_agents.yaml'
    tasks_config = 'config/planning_tasks.yaml'

    @agent
    def planner(self) -> Agent:
        search_SOPs = Search_SOPs_In_Depth()
       
        return Agent(
            config=self.agents_config['planner'],
            verbose=True,
            memory=True,
            tools=[search_SOPs]
        )
    
    @agent
    def map_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['map_planner'],
            verbose=True,
            memory=True
        )

    @task
    def generate_mission_plan_dict(self) -> Task:
        """Task to generate a mission plan"""
        return Task(
            config=self.tasks_config['generate_mission_plan_dict'],  # Use config for this task
            output_file='mission_dict.txt',
        )
    
    @task
    def create_map_plan(self):
        # Get the current date
        current_date = datetime.now().date()

        # Create the output folder path based on the current date
        output_folder = os.path.join('qGC_outputs', str(current_date))

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Generate the output file name with timestamp
        current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        output_file = os.path.join(output_folder, f'map_plan_{current_datetime}.plan')

        return Task(
            config=self.tasks_config['create_map_plan'],
            output_file=output_file,
        )
    
    @task
    def ensure_correct_data_type(self) -> Task:
        """Task to generate a mission plan"""
        return Task(
            config=self.tasks_config['ensure_correct_data_type'],  # Use config for this task
            #if there are errors in the data type, this output fill will help with debugging
            #output_file='mission_dict.txt',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Planning Crew with a planner agent"""
        return Crew(
            agents=[self.planner(), self.map_planner()],
            tasks=[self.generate_mission_plan_dict(), self.create_map_plan(), self.ensure_correct_data_type()],
            process=Process.sequential,
            verbose=True      
        )

class FeedbackCrew():
    """Feedback Evaluation Crew"""

    def feedback_agent(self):
        return Agent(
            role='Feedback Evaluator',
            goal=dedent("""
                Evaluate user feedback to determine whether the feedback 
                indicates readiness to move forward.
            """),
            backstory=dedent("""
                You excel at interpreting user feedback to decide whether 
                it signals satisfaction with the current state. If the user is 
                ready to proceed, signal the next node.
            """),
            verbose=False,
            allow_delegation=False
        )

    def feedback_task(self):
        """Task to analyze user feedback"""
        return Task(
            description=dedent("""
                Analyze the user feedback provided. If the feedback, {feedback} indicates 
                that the user is satisfied and ready to move forward, return "continue". 
                Otherwise, return the feedback unchanged.
            """),
            expected_output='Either the original feedback or "continue".',
            agent=self.feedback_agent(),
            tools=[], 
            human_input=True,
        )

    def mission_change_agent(self):
        return Agent(
            role='Mission Change Evaluator',
            goal=dedent("""
                Evaluate user feedback to determine whether the feedback
                indicates a need for a change in the mission. If a change is 
                needed, modify the existing mission or start a new one.
            """),
            backstory=dedent("""
                You excel at interpreting user feedback to decide whether 
                it signals a need for a change in the mission. If the user feedback 
                indicates a significant change, such as a new location or a new type 
                of operation, start a new mission. Otherwise, modify the existing mission.
            """),
            verbose=False,
            allow_delegation=False
        )

    def mission_change_task(self):
        """Task to analyze user feedback and modify the mission if needed"""
        return Task(
            description=dedent("""
                Analyze the user feedback provided. If the feedback, {feedback} indicates 
                that the user is satisfied and ready to move forward, return {mission}. 
                If the feedback indicates a need for a change in the mission, modify the 
                existing mission, {mission} or if the feedback indicates a 
                significant change like a new location or type of operation, return "restart".
                               
                
                If you choose to modify the mission: (DISREGARD OTHERWISE)               
                Consider the following previous waypoints: {previous_waypoints} to assist in modifying the mission
                Do not put these waypoints in the next mission but use these waypoints to inform the next mission.
            """),
            expected_output='Either the original mission, a modified mission, "restart"',
            agent=self.mission_change_agent(),
            tools=[], 
            human_input=False,
        )

    def crew(self):
        """Creates the Feedback Crew with a feedback agent"""
        return Crew(
            agents=[self.feedback_agent(), self.mission_change_agent()],
            tasks=[self.feedback_task(), self.mission_change_task()],
            #agents=[self.feedback_agent()],
            #tasks=[self.feedback_task()],
            process=Process.sequential
        )

class InitialInputCrew():
    """Initial Input Evaluation Crew"""

    def mission_evaluation_agent(self):
        return Agent(
            role='Mission Evaluation Expert',
            goal=dedent("""
                Evaluate user input {input} to determine if it describes one of the 
                existing mission options or a new mission.
            """),
            backstory=dedent("""
                You are an expert in the USAF and regularly help plan missions. 
                Your task is to analyze the user input and determine if it matches 
                one of the provided mission options or if it describes an entirely 
                new mission.
            """),
            verbose=False,
            allow_delegation=False
        )

    def mission_evaluation_task(self):
        """Task to evaluate if the user input matches an existing mission or is a new mission"""
        return Task(
            description=dedent("""
                Analyze the user input provided: "{input}". If the input matches one of the 
                mission options in {mission_options}, return the corresponding 
                mission option. If the input describes a new mission, return the users
                input as the new mission.
            """),
            expected_output='One of the mission options from {mission_options} or the new mission.',
            agent=self.mission_evaluation_agent(),
            tools=[],
        )

    @crew
    def crew(self):
        """Creates the Initial Input Crew with a mission evaluation agent"""
        return Crew(
            agents=[self.mission_evaluation_agent()],
            tasks=[self.mission_evaluation_task()],
            process=Process.sequential,
        )
