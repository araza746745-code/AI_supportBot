import streamlit as st
import requests

st.set_page_config(
    page_title="AI Support Bot",
    page_icon="🤖"
)

st.title("🤖 AI Customer Support")
st.write("Ask me anything about your customer support issue.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            try:
                response = requests.get(
                    "http://127.0.0.1:8000/chat",
                    params={"message": user_input},
                    timeout=120
                )
                response.raise_for_status()
                answer = response.json().get(
                    "reply",
                    response.json().get("error", "No reply received.")
                )
            except requests.RequestException as error:
                answer = f"Could not connect to the AI server: {error}"

            st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })