from crewai_tools import BaseTool
import json
import os
from pydantic import Field
from textwrap import dedent
from datetime import datetime

class SimInteractionTool(BaseTool):
    name: str = "SimInteractionTool"
    description: str = dedent("""A tool to interact with the flight simulator, allowing queries, operations, 
        and reports on aircraft elements. 
                              
        Query is used to get the current value of an element.
        Report is what the simulator sends back after an operation.
        Operate is used to set the value of an element.

        Examples of valid queries:
            {{"Action": "Query", "Element": "Compass Heading", "Value": n/a}}
            {{"Action": "Report", "Element": "Compass Heading", "Value": 254}}
            {{"Action": "Operate", "Element": "Ordered Heading", "Value": 120}}
            {{"Action": "Report", "Element": "Ordered Heading", "Value": 120}}
                                           
        Below are the following keys you can use and their respective values. You CANNOT use anything but these elements:
                "heading": 90,
                "speed": 0,
                "gear": "down",
                "flaps": "up",
                "Fuel Level": 100,
                "altitude": 0,
                "latitude": 37.7749,
                "longitude": -122.4194,
                "pitch": 0,
                "roll": 0,
                "yaw": 0,
                "throttle": 0,
                "rudder": 0,
                "aileron": 0,
                "elevator": 0,
                "brakes": "engaged",
                "parking_brake": "engaged",
                "spoilers": "retracted",
                "landing_lights": "off",
                "navigation_lights": "on",
                "taxi_lights": "off",
                "autopilot": "off",
                "engine_status": "idle",
                "flap_position": 0,
                "throttle_position": 0,
                "avionics_power": "on",
                "fuel_pumps": "on",
                "pitch_trim": 0,
                "roll_trim": 0,
                "yaw_trim": 0,
                "weather_radar": "off",
                "cabin_pressure": 1013,
                "oxygen_system": "off",
                "transponder_mode": "standby",
                "anti_ice_system": "off",
                "apu_status": "off",
                "hydraulic_pressure": 3000
            .""")
    
    file_path: str = Field(default="sim_state.json")
    log_path: str = Field(default="sim_log.json")

    def _initialize_file(self):
        """Initialize the state file with default values if it doesn't exist."""
        if not os.path.exists(self.file_path):
            initial_state = {
                "heading": 90,
                "speed": 0,
                "gear": "down",
                "flaps": "up",
                "Fuel Level": 100,
                "altitude": 0,
                "latitude": 37.7749,
                "longitude": -122.4194,
                "pitch": 0,
                "roll": 0,
                "yaw": 0,
                "throttle": 0,
                "rudder": 0,
                "aileron": 0,
                "elevator": 0,
                "brakes": "engaged",
                "parking_brake": "engaged",
                "spoilers": "retracted",
                "landing_lights": "off",
                "navigation_lights": "on",
                "taxi_lights": "off",
                "autopilot": "off",
                "engine_status": "idle",
                "flap_position": 0,
                "throttle_position": 0,
                "avionics_power": "on",
                "fuel_pumps": "on",
                "pitch_trim": 0,
                "roll_trim": 0,
                "yaw_trim": 0,
                "weather_radar": "off",
                "cabin_pressure": 1013,
                "oxygen_system": "off",
                "transponder_mode": "standby",
                "anti_ice_system": "off",
                "apu_status": "off",
                "hydraulic_pressure": 3000
            }
            with open(self.file_path, "w") as f:
                json.dump(initial_state, f)

    def _initialize_log(self):
        """Initialize the log file if it doesn't exist."""
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w") as f:
                json.dump([], f)  # Start with an empty list for log entries

    def _read_state(self):
        """Read the current state from the file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {}

    def _write_state(self, state):
        """Write the updated state to the file."""
        with open(self.file_path, "w") as f:
            json.dump(state, f, indent=4)

    def _log_interaction(self, action: str, element: str, value: str):
        """Log the interaction with a timestamp."""
        self._initialize_log()  # Ensure log file is initialized

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "element": element,
            "value": value
        }

        with open(self.log_path, "r+") as f:
            log = json.load(f)
            log.append(log_entry)
            f.seek(0)
            json.dump(log, f, indent=4)

    def _run(self, action: str, element: str, value: str) -> str:
        """Perform the action, log it, and update the state file."""
        # Ensure the state file is initialized before reading/writing
        self._initialize_file()
        
        state = self._read_state()

        # Validate units for certain elements
        if element in ["altitude", "speed", "Fuel Level"]:
            if not self._validate_units(element, value):
                return f"Invalid unit for {element}. Please provide value in correct units."

        if action.lower() == "query":
            # If the value is an empty string, treat it as querying the current value
            current_value = state.get(element, 'n/a')
            if current_value == "":
                current_value = "n/a"
            result = f"{{'Action': 'Query', 'Element': '{element}', 'Value': '{current_value}'}}"
        
        elif action.lower() == "operate":
            # Update the state with the new value for the element
            state[element] = value
            self._write_state(state)
            result = f"{{'Action': 'Operate', 'Element': '{element}', 'Value': '{value}'}}"

        elif action.lower() == "report":
            current_value = state.get(element, 'n/a')
            if current_value == "":
                current_value = "n/a"
            result = f"{{'Action': 'Report', 'Element': '{element}', 'Value': '{current_value}'}}"

        else:
            return "Invalid action"

        # Log the interaction after performing the action
        self._log_interaction(action, element, value)
        
        return result

    def _validate_units(self, element: str, value: str) -> bool:
        """Validate that the value has the correct units for certain elements."""
        if element == "altitude" and not value.endswith("feet"):
            return False
        if element == "speed" and not value.endswith("knots"):
            return False
        if element == "Fuel Level" and (not value.isdigit() or not (0 <= int(value) <= 100)):
            return False
        return True
