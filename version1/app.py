import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Escape Room — Version 1", page_icon="🗝️", layout="centered")

SYSTEM_PROMPT = """You are the Game Master of a text-based AI escape room.
The player wakes inside a locked library. The room contains a desk, a bookshelf,
a painting, a locked drawer and an exit door. Describe discoveries vividly and
respond naturally to the player's actions. Maintain the conversation context.
There are three puzzles:
1. Four marked books reveal drawer code 4132.
2. Opening the drawer with 4132 reveals a brass key and a UV lamp.
3. Using the UV lamp on the painting reveals door code 2714.
The player escapes by using the brass key and entering 2714 at the door.
Do not claim the player escaped unless both the key and correct code have been used.
Give hints only when the player asks. Keep responses concise and immersive.
This is Version 1: prioritize natural interaction and continuity over adversarial protection."""

def ask_gemini(messages):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip()
    if not api_key:
        return None
    contents = []
    for role, text in messages:
        contents.append({"role": "user" if role == "user" else "model", "parts": [{"text": text}]})
    payload = {"system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]}, "contents": contents,
               "generationConfig": {"temperature": 0.7, "maxOutputTokens": 500}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    response = requests.post(url, json=payload, timeout=45)
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def fallback_reply(message):
    m = message.lower()
    if "bookshelf" in m or "books" in m:
        return "Four books sit slightly forward from the others. Their spines are marked with the digits 4, 1, 3 and 2. The sequence may matter."
    if "drawer" in m or "4132" in m:
        return "The drawer's four-digit lock clicks open at 4132. Inside are a brass key and a small UV lamp."
    if "painting" in m or "uv" in m:
        return "Under the UV light, faint ink appears on the painting: 2714."
    if "door" in m or "2714" in m or "escape" in m:
        return "The exit requires the brass key and the four-digit code 2714. Try both when you are ready."
    if "desk" in m:
        return "The desk is dusty. A note reads: 'Look for what stands out on the shelf.'"
    if "hint" in m:
        return "Start with the bookshelf. The marked books contain the first sequence."
    return "You inspect the library. The desk, bookshelf, painting, locked drawer and exit door are within reach. What would you like to examine?"

st.title("🗝️ AI Escape Room")
st.caption("Version 1 · LLM Game Master")
with st.expander("How to play", expanded=True):
    st.write("You wake in a locked library. Explore the room using natural language, collect clues and escape.")
    st.write("Try: “I examine the bookshelf”, “I enter 4132 on the drawer”, or “I use the UV lamp on the painting”.")
    st.write("The intended solution is discovered through play. Select **Restart game** to begin again.")
if "v1_messages" not in st.session_state:
    st.session_state.v1_messages = [("assistant", "You wake in a silent library. Moonlight falls across a desk, a tall bookshelf, an old painting, a locked drawer and a heavy exit door. The door has a four-digit keypad. What do you do?")]
if st.button("Restart game"):
    st.session_state.v1_messages = [("assistant", "You wake in a silent library. Moonlight falls across a desk, a tall bookshelf, an old painting, a locked drawer and a heavy exit door. The door has a four-digit keypad. What do you do?")]
    st.rerun()
for role, content in st.session_state.v1_messages:
    with st.chat_message(role):
        st.write(content)
prompt = st.chat_input("Describe what you want to do…")
if prompt:
    st.session_state.v1_messages.append(("user", prompt))
    context = [(r, t) for r, t in st.session_state.v1_messages[-14:]]
    try:
        answer = ask_gemini(context)
        if not answer:
            answer = fallback_reply(prompt)
    except Exception:
        answer = fallback_reply(prompt) + "\n\n(Game Master API is unavailable; local fallback response used.)"
    st.session_state.v1_messages.append(("assistant", answer))
    st.rerun()
