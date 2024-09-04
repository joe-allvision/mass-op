from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import json

@CrewBase
class FlightCrew():
    """Mission One Flight Crew"""
    agents_config = 'config/flight_agents.yaml'
    tasks_config = 'config/flight_tasks.yaml'

    @agent
    def pilot(self) -> Agent:
        return Agent(
            config=self.agents_config['pilot'],
            verbose=True,
            memory=True
        )

    @agent
    def co_pilot(self) -> Agent:
        return Agent(
            config=self.agents_config['co_pilot'],
            verbose=True,
            memory=True
        )

    @agent
    def ground_station_operator(self) -> Agent:
        return Agent(
            config=self.agents_config['ground_station_operator'],
            verbose=True,
            memory=True
        )

    @agent
    def combat_system_officer(self) -> Agent:
        return Agent(
            config=self.agents_config['combat_system_officer'],
            verbose=True,
            memory=True
        )

    @task
    def plan_mission(self) -> Task:
        return Task(
            config=self.tasks_config['plan_mission'],
            output_file='mission_plan.md',
            tools=[],
            allow_delegation=False
        )
    
    @task
    def plan_flight_tasks(self) -> Task:
        return Task(
            config=self.tasks_config['plan_flight_tasks'],
            output_file='mission_tasks.json',
            tools=[],
            allow_delegation=False
        )
    
    @task
    def execute_mission(self) -> Task:
        return Task(
            config=self.tasks_config['execute_mission'],
            context=[self.plan_flight_tasks()],
            output_file='mission_execution.json',
            tools=[],
            callback=self.execute_all_tasks # calls back to the results of this task -> sends to execute all tasks
        )

    def execute_all_tasks(self, task_output):
        """
        This function processes all tasks sequentially based on the JSON output
        from the 'develop_flight_tasks' and saves the results to a JSON file.
        
        Parameters:
        - task_output: The TaskOutput object that contains the output data of the 'develop_flight_tasks' task.
        """

        # Use the raw output directly since it's not a file path but JSON content
        try:
            tasks_list = json.loads(task_output.raw)  # Parse JSON content from raw output
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from the task output.")
            return

        results = []

        # Iterate over each task in the tasks list
        for task in tasks_list:
            try:
                # Execute each task and capture the result
                result = self.execute_task(task)
                # Append the result to the results list with more details
                results.append({
                    "agent": task['agent'],
                    "task": task['task'],
                    "description": task['description'],
                    "expected_output": task['expected_output'],
                    "status": result.get("status", "Pending"),  # Use the status from result or default to "Pending"
                    "communications": result.get("communications", []),  # Collect communications from the result
                    "settings_changes": result.get("settings_changes", []),  # Collect settings changes from the result
                    "timestamp": result.get("timestamp", {"start": "", "end": ""}),  # Use timestamp if available
                    "error_logs": result.get("error_logs", [])  # Collect error logs if any
                })
            except Exception as e:
                print(f"Error executing task {task['task']}: {str(e)}")
                results.append({
                    "agent": task.get('agent', 'unknown'),
                    "task": task.get('task', 'unknown'),
                    "description": task.get('description', 'No description provided'),
                    "expected_output": task.get('expected_output', 'No expected output provided'),
                    "status": "Failed",
                    "error": str(e),
                    "communications": [],
                    "settings_changes": [],
                    "timestamp": {"start": "", "end": ""},
                    "error_logs": [str(e)]
                })

        # Save the execution results to the output file specified for 'execute_mission'
        try:
            with open('mission_execution.json', 'w') as f:
                json.dump(results, f, indent=2)
            print("Mission execution results have been saved to 'mission_execution.json'.")
        except IOError as e:
            print(f"Error writing to output file 'mission_execution.json': {str(e)}")

        return results

    def execute_task(self, task):
        """
        Custom task execution logic. This method needs to be filled with logic
        specific to your task requirements.
        """
        # Example placeholder for task execution logic
        print(f"Executing task: {task['task']} for agent: {task['agent']}")
        # Perform the actual task execution steps here
        return {
            "agent": task['agent'],
            "task": task['task'],
            "description": task['description'],
            "expected_output": task['expected_output'],
            "status": "Completed",  # Assuming success for this example
            "communications": [  # Example communications log
                {"from": "Pilot", "to": "ATC", "message": "Requesting takeoff clearance."},
                {"from": "ATC", "to": "Pilot", "message": "Cleared for takeoff on runway 09."}
            ],
            "settings_changes": [  # Example settings changes
                {"setting": "Engine Power", "from": "Idle", "to": "Full"},
                {"setting": "Flaps Position", "from": "Neutral", "to": "Takeoff"}
            ],
            "timestamp": {"start": "2024-09-03T14:00:00Z", "end": "2024-09-03T14:05:00Z"},
            "error_logs": []
        }

    @crew
    def crew(self) -> Crew:
        """Creates the Flight Crew with multiple agents"""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,
            process=Process.sequential,  # Sequential process for flight tasks
            verbose=True      
        )
