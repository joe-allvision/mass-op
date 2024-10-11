
# Flight Crew Initiation and Early Capabilities Testing

This project uses the CrewAI framework to simulate early multi-agent collaboration in a flight environment. It demonstrates how different agents (Pilot, Co-Pilot, Ground Station Operator, Combat System Officer) work together in a simulated takeoff.

## Table of Contents
- [Overview](#overview)
- [Setup](#setup)
- [Running the Simulation](#running-the-simulation)
- [Project Structure](#project-structure)
- [Requirements](#requirements)

## Overview
The simulation involves multiple agents performing their roles to execute a successful takeoff and subsequent operations. The agents communicate and coordinate actions according to predefined rules and responsibilities.

## Setup

1. **Clone the Repository**
   Clone the repo and `cd` into `Flight Simulation/` folder

2. **Create a Virtual Environment and Install Requirements**
   ```bash
   python -m venv .venv
   source venv/bin/activate
   python install -r requirements.txt
   ```

3. **Update Environment Variables**
   - Ensure you have a `.env` file in the root directory with your API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   Optionally you can put the following for traces to be stored in LangSmith:
   ```
   export LANGCHAIN_API_KEY=your_api_key_here
   export LANGCHAIN_TRACING_V2=true
   ```

## Running the Simulation
To run the simulation, execute the main script from the terminal:

```bash
python uav/flight_sim.py
```
or
```bash
python maritime_rescue/flight_sim.py
```

The Chat agent uses GPT-4o but can use any LLM.

## Project Structure

```
├── README.md               # Project documentation
├── maritime_rescue
│   ├── flight_roles.py     # Defines the crew and their roles
│   ├── flight_sim.py       # Main script to run the simulation
│   └── flight_tools.py     # Tools that LangGraph nodes can call
├── requirements.txt        # Dependencies needed to run flight_sim.py
└── uav
│   ├── experimental_run_1.txt
│   ├── flight_roles.py     # Defines the crew and their roles
│   ├── flight_sim.py       # Main script to run the simulation
│   ├── flight_tools.py     # Tools that LangGraph nodes can call
│   ├── t.py
│   └── test.ipynb
└── .env                    # Environment variables file (not included, must be created)
```

## Requirements

- **Python**: 3.10+
- **GPT-4o Access**: Ensure you have access to OpenAI's GPT-4o or adjust the model settings as needed.
