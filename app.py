import json
from google import genai
from PIL import Image

import asyncio
from telegram import Bot
from google.genai import types
import streamlit as st
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE, SUMMARY_REQUEST_PROMPT



GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)

 
def send_telegram(chat_id:str, text):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        asyncio.run(bot.send_message(chat_id=chat_id, text=text))
        return True, "Message sent successfully"
    except Exception as e:
        return False, str(e)

gemini_client = get_gemini_client()

def render_message(message:dict):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.markdown(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])

def add_message(role,kind, content):
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})    
    render_message(st.session_state.messages[-1])

def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as e:
            if '503' in str(e):
                return "Servers are busy right now. Please try again in a few minutes."
            return f"Error: {e}"


if 'onboarded' not in st.session_state:
    st.title("Welcome to CogniSnap!👋")
    st.caption("A friendly AI study assistant that helps you understand complex topics from a photo or text description.")
    with st.form("onboarding_form"):
        name=st.text_input("What is your name?")
        telegram_chat_id=st.text_input("What is your Telegram chat Id? You can obtain it by searching @userinfobot on Telegram and sending /start to get your chat Id.",
        placeholder="9xxxxxxxx",
        help="This is used to send you your study summaries via Telegram.Enter your telegram chat Id.Message @userinfobot on Telegram",
        )
        submitted = st.form_submit_button("Submit")
    if submitted:
        if not name.strip() or not telegram_chat_id.strip():
            st.warning("Please fill in all fields.")
        else:
            st.session_state.name = name.strip()
            st.session_state.telegram_chat_id = telegram_chat_id.strip()
            st.session_state.chat=gemini_client.chats.create(
                model="gemini-3.8-flash",
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            st.session_state.messages=[]
            st.session_state.onboarded = True
            st.rerun()
    st.stop()

 
# Step 2: chat interface
header_col, button_col = st.columns([5, 2], vertical_alignment="center")
 
with header_col:
    st.title("📚CogniSnap")
 
with button_col:
    send_disabled = len(st.session_state.messages) <= 2
    if st.button("📤 Send to Telegram", disabled=send_disabled, use_container_width=True):
        with st.spinner("Summarizing your day..."):
             summary = ask_gemini([SUMMARY_REQUEST_PROMPT])
             success, info = send_telegram(st.session_state.telegram_chat_id, summary)
        if success:
            st.success("Sent! Check your Telegram 📲")
        else:
            st.error(f"Couldn't send that: {info}")
 
st.caption(f"Logged in as {st.session_state.name} - updates go to Telegram Id: {st.session_state.telegram_chat_id}")
 
if not st.session_state.messages:
    add_message("assistant", "text", WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message)

user_input = st.chat_input("Send a message or upload an image...",
accept_file=True,
file_type=["png", "jpeg", "jpg", "gif", "pdf"],
)

if user_input:
    photo=user_input.files[0] if user_input.files else None
    text=user_input.text
    parts=[]

    if photo is not None:
        photo_bytes=photo.getvalue()
        add_message("user", "image", photo_bytes)
        parts.append(types.Part.from_bytes(data=photo_bytes, mime_type=photo.type))
    if text:
        add_message("user", "text", text)
        parts.append(text)
    elif photo is not None:
        parts.append("Please analyze the photo and explain the content in simple terms for study purposes.")
    with st.spinner("Analyzing..."):
        answer=ask_gemini(parts)
    add_message("assistant", "text", answer)

    st.rerun()


