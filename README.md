# Vision GUI Agent

## Overview
The Vision GUI Agent is a Python application that leverages the OpenAI GPT-4o model to assist users in automating GUI interactions based on natural language commands. The application captures the current screen, interprets user commands, and executes a sequence of actions to interact with the graphical user interface.

## Project Structure
```
agent
├── src
│   ├── agent.py       # Main interactive loop for the application
│   ├── brain.py       # Communicates with GPT-4o for action planning
│   ├── config.py      # Loads configuration settings and API keys
│   ├── eye.py         # Utilities for capturing the screen
│   ├── hand.py        # Functions to execute planned actions
├── .env.example        # Template for environment variables
├── requirements.txt    # Project dependencies
└── README.md           # Documentation for the project
```

## Requirements
To run this project, you need to have Python installed along with the following dependencies:

- openai>=1.13.3
- pyautogui>=0.9.54
- keyboard>=0.13.5
- pillow>=10.2.0
- python-dotenv>=1.0.1

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Setup
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd agent
   ```

2. **Create a `.env` file**:
   Rename the `.env.example` file to `.env` and fill in your OpenAI API key:
   ```
   OPENAI_API_KEY="sk-..."
   ```

3. **Run the application**:
   Execute the main script to start the interactive loop:
   ```
   python src/agent.py
   ```

## Usage
- Upon running the application, you will be prompted to enter a command.
- The application will capture the current screen and send the screenshot along with your command to the GPT-4o model for action planning.
- The planned actions will be displayed, and you will have the option to execute them.
- Type 'exit' or 'quit' to terminate the application.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.# Friday
# Friday
