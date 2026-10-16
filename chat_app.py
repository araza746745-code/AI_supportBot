import streamlit as st
import requests

st.set_page_config(
    page_title="AI Support Bot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Customer Support Bot")
st.caption("Powered by FastAPI and Ollama")

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

API_URL = "http://127.0.0.1:8000/chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("How can I help you today?")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    try:
        response = requests.get(
            API_URL,
            params={"message": user_input},
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        answer = result.get("reply", "No reply received.")

    except requests.RequestException as error:
        answer = f"API connection error: {error}"

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })