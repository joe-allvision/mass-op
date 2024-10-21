# Urban SAR: MavLink Flight Simulation and LangGraph + CrewAI Integration

This project integrates natural language processing with sample flight simulation technologies, utilizing the CrewAI and LangGraph frameworks to process inputs and execute operations within a simulated environment. The primary objective of this project is to convert natural language inputs, have agents process these inputs, and execute a flight simulation script using QGroundControl, ArduPilot, and MAVLink.

## Table of Contents
- [Overview](#overview)
- [Setup](#setup)
- [Running the Simulation](#running-the-simulation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Disclaimer](#disclaimer)
- [License](#license)

## Overview

In addition, this project integrates agents crews built in CrewAI as nodes in LangGraph. This approach joins the ergonomics of CrewAI and the flexibility of LangGraph. Ihis pattern also enables human-in-the-loop interactions through feedback at defined points in the agentic workflow.

In this workflow, agents create a flight plan based on high-level guidance for a search and rescue mission and predefined processes. The simulated flight is a MAVlink script; the agents generate the waypoints and append them to the flight script. 

## Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/joe-allvision/mass-op.git
   cd mass-op
   ```

2. **Update Environment Variables**
   - Ensure you have a `.env` file in the root directory with your API key:
   ```
   API_KEY=your_api_key_here
   ```

3. **Install Dependencies**
   - Install necessary tools and libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a Virtual Environment**
   - Use a virtual environment for better isolation:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

## Running the Simulation

Execute the main script from the terminal to start the simulation:

```bash
python src/main.py
```

Ensure you have access to GPT-4o as the simulation uses it by default.

## Configuration

### `mission_input.yaml`

The `mission_input.yaml` file provides sample missions. You can load any of these and add more as you desire.

You can modify the `mission_input.yaml` file to customize the mission parameters and agent behaviors.

## Project Structure

```
mass-op/
├── src/
│   ├── main.py                 # Main script to run the simulation
│   ├── mission_input.yaml      # Configuration file for mission parameters
│   ├── graph/
│   │   ├── create_workflow.py  # Workflow creation for the simulation
│   │   ├── graph_utils.py      # Utilities for graph operations
│   │   ├── graph_nodes/
│   │   │   ├── load_sample_mission.py  # Loads sample missions
│   │   │   ├── node_a.py               # Additional node
│   │   │   ├── node_b.py               # Additional node
│   │   │   ├── node_c.py               # Additional node
│   ├── crewAI_crews/
│   │   ├── config/
│   │   │   ├── planning_agents.yaml  # Agent configurations
│   │   │   ├── planning_tasks.yaml   # Task configurations
│   │   ├── crews.py            # Defines the crew and their roles
│   │   ├── tools/
│   │   │   ├── sopSAR.py       # Tools for search and rescue operations
├── README.md                   # Project documentation
├── .env                        # Environment variables file (not included, must be created)
└── ...                         # Other supporting files and directories
```

## Requirements

- **Python**: 3.10 to 3.13
- **CrewAI**: Latest version (0.70.1)
- **LangGraph**: Latest version (0.2.38)
- **QGroundControl**: Setup for simulation
- **ArduPilot**: Configured for use with MAVLink

Ensure all dependencies are installed as specified in the `requirements.txt` file.

## Disclaimer

This project uses simulated environments for demonstration purposes. These agents do not yet have control over the aircraft. They have control over the mission plan which feeds into the a python script that controls the simulation.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
