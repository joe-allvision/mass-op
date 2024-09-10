
# Flight Crew Initiation and Early Capabilities Testing

This project uses the CrewAI framework to simulate early multi-agent collaboration in a flight environment. It demonstrates how different agents (Pilot, Co-Pilot, Ground Station Operator, Combat System Officer) work together in a simulated takeoff sequence from a dead stop at the end of the runway to being airborne and on course to the first search area.

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

The simulation involves multiple agents performing their roles to execute a successful takeoff and subsequent operations. The agents communicate and coordinate actions according to predefined rules and responsibilities.

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
   - Install `crewai` and other necessary tools:
   ```bash
   pip install crewai crewai-tools
   ```

4. **Create a Virtual Environment**
   - It’s recommended to use a virtual environment. You can create one using `venv`, `conda`, or any other tool:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scriptsctivate
   ```

## Running the Simulation

To run the simulation, execute the main script from the terminal:

```bash
python src/main.py
```

Ensure you have access to GPT-4o as the simulation uses it by default.

## Configuration

### `mission_input.yaml`

The `mission_input.yaml` file defines the mission, rules, responsibilities, and task standards for the simulation:

- **Mission**: Details the objective of the simulation, which is the takeoff and navigation to the first search area.
- **Rules**: Communication protocols and procedures between agents.
- **Responsibilities**: Defines the roles of the Pilot, Co-Pilot, Ground Station Operator, and Combat System Officer.
- **Task Standards**: Outlines how tasks should be logged, documented, delegated, and communicated.

You can modify the `mission_input.yaml` file to customize the mission parameters and agent behaviors.

## Project Structure

```
mass-op/
├── crews.py                # Defines the crew and their roles
├── main.py                 # Main script to run the simulation
├── mission_input.yaml      # Configuration file for mission parameters and rules
├── README.md               # Project documentation
├── .env                    # Environment variables file (not included, must be created)
└── ...                     # Other supporting files and directories
```

## Requirements

- **Python**: 3.10 to 3.13
- **CrewAI**: 0.51.1 (or the most up-to-date version)
- **GPT-4o Access**: Ensure you have access to OpenAI's GPT-4o or adjust the model settings as needed.

## Disclaimer

This project is configured to use GPT-4o by default, which may incur usage costs. You can change the model settings in `main.py` to use a different model if needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
