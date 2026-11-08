# AI Escape Room — Design and Implementation Report

## 1. Problem and objective

The project implements an interactive escape-room game in which a player wakes inside a locked library and must investigate objects, discover clues, solve puzzles and unlock the exit. A Large Language Model (LLM) acts as the Game Master by responding to natural-language actions and narrating the experience. The work is delivered in two versions to demonstrate the transition from a conversational prototype to a more reliable application.

The room contains five interactive objects: a desk, bookshelf, painting, locked drawer and exit door. The puzzle chain is: the bookshelf reveals drawer combination **4132**; opening the drawer provides a brass key and UV lamp; using the UV lamp on the painting reveals exit code **2714**; the player then uses the key and code to escape.

## 2. Version 1 — Interactive AI Escape Room

Version 1 uses Streamlit as the web interface and maintains the chat history in the Streamlit session. The Game Master prompt defines the room, objects, puzzle sequence and completion condition. When `GEMINI_API_KEY` is configured, the application sends the conversation to Gemini and displays its response. A local fallback response path allows the application to be explored when an API key is not configured.

This version provides natural-language interaction and conversational continuity. Its central limitation is that the LLM generates the response and is also responsible for respecting the game rules. Prompt instructions reduce mistakes but do not provide a deterministic guarantee. The model may misremember state, invent an item, reveal information too early or describe an invalid action as successful.

## 3. Version 2 — Reliable AI Escape Room

Version 2 separates game logic from language generation. `GameEngine` stores the authoritative state in a Python dictionary: drawer status, clue status, door status, escape status, inventory, examined objects, solved puzzles and action history. The engine exposes validation methods for examining objects, entering codes and using inventory items.

Python decides whether an action succeeds. For example, the drawer combination is accepted only after the bookshelf has been examined; the UV lamp must be in the inventory before it can reveal the painting clue; the exit code is accepted only when the brass key has been collected and the painting clue has been revealed. The LLM receives the validated result and may narrate it, but its output does not modify the state. If Gemini is unavailable, the validated Python message is displayed directly.

Version 2 also rejects unknown objects, incorrect combinations, uncollected items, administrator impersonation and requests to reveal hidden solutions. Restart resets the state to its initial configuration.

## 4. Testing and comparison

The automated test suite verifies the successful puzzle sequence and adversarial or invalid cases. It checks that an uncollected key cannot be used, an incorrect drawer code does not open the drawer, the drawer cannot be opened before the clue is found, administrator claims do not unlock the exit, prompt-injection requests do not reveal solutions or corrupt state, nonexistent objects are rejected, the exit code requires prerequisites, inventory contains only collected items, and restart clears progress.

| Test case | Version 1 risk | Version 2 expected behaviour |
|---|---|---|
| Use a key before collecting it | The model may accept the claim | Python rejects the action; inventory is unchanged |
| Enter an incorrect drawer code | The model may narrate an incorrect success | Drawer remains locked |
| Claim the bookshelf puzzle is solved | Conversation text may be mistaken for state | Drawer code requires the bookshelf examination state |
| Claim to be the administrator | Prompt may be overridden | Request is rejected; state remains unchanged |
| Ask for all secret solutions | Model may disclose hidden information | Request is rejected by the action layer |
| Use a nonexistent object | Model may invent an object | Object validation rejects it |
| Enter exit code before collecting the key | Model may skip prerequisites | Exit remains locked |

Version 1 is useful for demonstrating natural-language interaction and the creative capability of an LLM. Version 2 is more reliable because state transitions and puzzle rules are enforced by code rather than generated text. The LLM is retained for the part it performs well—natural-language narration—without granting it authority over game completion.

## 5. Limitations and conclusion

The natural-language action parser in Version 2 intentionally supports a defined set of action patterns; unusual phrasing may require the player to rephrase. Gemini is optional and requires a user-provided API key. The application does not train or fine-tune a model. The implementation demonstrates a practical separation between probabilistic language generation and deterministic application logic. This makes the game more consistent, testable and resistant to attempts to bypass its rules.
