from fastapi import FastAPI
import requests

app = FastAPI(title="AI Support Bot")

# Store conversation history
chat_history = []

@app.get("/")
def home():
    return {
        "message": "AI Support Bot is running!",
        "status": "success"
    }

@app.get("/chat")
def chat(message: str):
    global chat_history

    try:
        # Add the new user message
        chat_history.append(f"Customer: {message}")

        # Build the prompt with conversation history
        conversation = "\n".join(chat_history)

        prompt = (
            "You are a helpful customer support agent. "
            "Use the conversation history to understand context "
            "and remember information the customer shared. "
            "Reply politely and clearly.\n\n"
            + conversation
            + "\nAssistant:"
        )

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        result = response.json()
        answer = result["response"]

        # Save the assistant's reply
        chat_history.append(f"Assistant: {answer}")

        return {
            "user_message": message,
            "reply": answer
        }

    except requests.RequestException as error:
        return {
            "error": f"AI service error: {error}"
        }