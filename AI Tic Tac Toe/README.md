
# AI Tic-Tac-Toe

## Table of Contents
- [Overview](#overview)
- [Setup](#setup)
- [Running the Simulation](#running-the-simulation)
- [Project Structure](#project-structure)
- [Requirements](#requirements)

## Overview
Have LLMs play tic-tae-toe against an opponent! The opponent simply puts markers in random spots on the board. The opponent starts first, and then the LLM places a marker on the board. Repeat until the game is over.

## Setup

1. **Clone the Repository**
   Clone the repo and `cd` into `AI Tic Tac Toe/` folder

2. **Create a Virtual Environment and Install Requirements**
   ```bash
   python -m venv .venv
   source venv/bin/activate
   python install -r requirements.txt
   ```

3. **Update Environment Variables**
   - Ensure you have a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   Optionally you can change the code to use Anthropic models, which you would want to add your Anthropic API key
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```
   Optionally you can put the following for traces to be stored in LangSmith:
   ```
   export LANGCHAIN_API_KEY=your_api_key_here
   export LANGCHAIN_TRACING_V2=true
   ```

## Running the tic-tac-toe game
Execute the main script from the terminal:

```bash
python ai_tic_tac_toe.py
```
The LLM agent uses GPT-4 but can use any LLM.

## Requirements

- **Python**: 3.10+
- **GPT-4 Access**: Ensure you have access to OpenAI's GPT-4 or adjust the model settings as needed.
