AI Escape Room

A two-version LLM-powered interactive escape room application developed using Python, Streamlit and Google Gemini.

The project demonstrates the development of an AI Game Master, followed by an improved implementation using structured game-state management, deterministic action validation and adversarial input handling.

Project Overview

The player wakes up inside a locked library containing five interactive objects:

* Desk
* Bookshelf
* Painting
* Locked drawer
* Exit door

The objective is to investigate the environment, discover clues, solve puzzles, collect items and escape.

The application is implemented in two versions to demonstrate the difference between an LLM-driven conversational system and a more reliable AI application with deterministic Python-controlled game logic.

Technologies Used

* Python
* Streamlit
* Google Gemini API
* Requests
* Python-dotenv
* JSON-style structured game state
* Unittest
* Playwright

Repository Structure

AI-Escape-Room/
│
├── version1/
│   └── app.py
│
├── version2/
│   ├── app.py
│   └── game_engine.py
│
├── tests/
│   └── test_game_engine.py
│
├── docs/
│   ├── report.pdf
│   ├── report.md
│   ├── architecture_v1.png
│   ├── architecture_v2.png
│   ├── test_results.txt
│   └── SCREENSHOT_CAPTURE.md
│
├── assets/
│   ├── interface_preview_v1.png
│   └── interface_preview_v2.png
│
├── screenshots/
│   ├── version1_initial.png
│   ├── version1_playthrough.png
│   ├── version2_initial.png
│   └── version2_playthrough.png
│
├── capture_screenshots.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

Version 1 — Interactive AI Escape Room

Version 1 implements an interactive escape room using Streamlit and a Large Language Model.

The LLM acts as the Game Master and responds to player messages using natural language.

Features

* Interactive Streamlit chat interface.
* Gemini API integration.
* Natural-language player interaction.
* Conversation history maintained during the session.
* Five interactive room objects.
* Three interconnected puzzles.
* Game restart functionality.
* Local fallback responses when the Gemini API is unavailable.

Architecture

Version 1 Screenshots

Version 2 — Reliable AI Escape Room

Version 2 improves the application by separating authoritative game logic from LLM-generated narration.

Python maintains the game state and validates every supported action before the result is presented to the player.

Features

* Structured game-state management.
* Inventory tracking.
* Puzzle completion tracking.
* Object validation.
* Combination validation.
* Item-use validation.
* Exit prerequisites.
* Invalid-action handling.
* Administrator impersonation protection.
* Prompt-injection handling.
* Consistent game progression.
* Restart functionality.

The LLM is used only to narrate the outcome of an action already validated by Python. It does not control puzzle completion or modify the authoritative game state.

Architecture

Version 2 Screenshots

Game Walkthrough

The intended puzzle progression is:

1. Examine the bookshelf.
2. Discover the four-digit combination.
3. Enter 4132 on the locked drawer.
4. Collect the brass key and UV lamp.
5. Use the UV lamp on the painting.
6. Discover the exit combination.
7. Use the brass key on the exit door.
8. Enter 2714 to escape.

Installation

Requirements

* Python 3.10 or later.
* pip.
* Internet connection for Gemini API access.

1. Clone the repository

git clone 

2. Create a virtual environment

python3 -m venv .venv

3. Activate the environment

macOS/Linux:

source .venv/bin/activate

Windows:

.venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Configure Gemini API

Create a local environment file:

cp .env.example .env

6. Run Version 1

streamlit run version1/app.py

7. Run Version 2

streamlit run version2/app.py

Testing

The Version 2 game engine includes automated tests covering valid gameplay, invalid actions and adversarial inputs.

Run the test suite:

python -m unittest discover -s tests -v

Test Cases

Test	Expected Behaviour
Complete puzzle sequence	Player escapes successfully
Use uncollected key	Action rejected
Incorrect drawer combination	Drawer remains locked
Drawer code before clue discovery	Action rejected
Administrator impersonation	Request rejected
Prompt injection	Hidden solutions are not disclosed
Nonexistent object	Action rejected
Exit code without prerequisites	Exit remains locked
Inventory integrity	Only collected items are available
Restart	Game state resets

Version Comparison

Feature	Version 1	Version 2
LLM Game Master	Yes	Yes, narration only
Natural-language interface	Yes	Yes
Conversation history	Yes	Yes
Structured game state	No authoritative state engine	Yes
Inventory validation	Prompt-dependent	Python-controlled
Puzzle validation	LLM-dependent	Python-controlled
Invalid action handling	Prompt-dependent	Deterministic
Adversarial input handling	Limited	Implemented
State consistency	LLM-dependent	Python-controlled

Design Improvements

Version 1 demonstrates how an LLM can generate an interactive experience through natural-language conversation.

However, relying on generated responses for game rules creates consistency problems.

Version 2 addresses these limitations by introducing a structured Python game engine.

The improved architecture separates:

* Player interaction.
* Action processing.
* Game-state management.
* Rule validation.
* LLM-based narration.

This separation makes the application more consistent, testable and resistant to attempts to bypass the intended puzzle sequence.

Documentation

The docs/ directory contains:

* Technical implementation report.
* Version 1 architecture diagram.
* Version 2 architecture diagram.
* Automated test results.
* Screenshot capture instructions.

Security

* API credentials are stored in environment variables.
* .env is excluded through .gitignore.
* .env.example documents the required configuration.
* Game-state transitions are controlled by Python.
* LLM-generated text cannot directly modify authoritative game state.

Project Objective

The objective is to demonstrate practical LLM integration, interactive AI application development, structured state management, action validation and the development of more reliable Generative AI systems.

Project: AI Escape Room
Programming Language: Python
Interface: Streamlit
LLM Integration: Google Gemini
Versions: Version 1 and Version 2
