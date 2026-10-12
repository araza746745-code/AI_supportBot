🤖 AI Support Bot

An AI-powered customer support chatbot built using Python, FastAPI, Streamlit, and Ollama.

📌 Project Overview

This project provides a chat interface where users can ask questions and receive AI-generated responses using the Qwen 2.5 language model running locally through Ollama.

✨ Features

- AI-powered chatbot responses
- FastAPI backend and REST API
- Streamlit chat interface
- Ollama integration with Qwen 2.5 (3B)
- Dockerfile for containerizing the backend
- Git and GitHub version control

🛠️ Technologies Used

- Python
- FastAPI
- Streamlit
- Ollama
- Qwen 2.5 (3B model)
- Uvicorn
- Docker
- Git and GitHub

⚙️ How It Works

1. The user enters a question in the Streamlit interface.
2. Streamlit sends the message to the FastAPI backend.
3. The backend sends the prompt to Ollama.
4. The Qwen 2.5 model generates a response.
5. The response is returned to the chat interface.

🚀 Setup Instructions

1. Clone the repository

git clone https://github.com/araza746745-code/AI_supportBot.git
cd AI_supportBot

2. Install dependencies

pip install -r requirements.txt

3. Download the AI model

Install Ollama from https://ollama.com/ and run:

ollama pull qwen2.5:3b

Make sure Ollama is running.

4. Start the FastAPI backend

uvicorn main:app --reload

Open http://127.0.0.1:8000/docs to view the API documentation.

5. Start the Streamlit frontend

Open another terminal and run:

streamlit run chat_app.py

Open the local URL shown in your terminal.

🐳 Docker

Build the backend image:

docker build -t ai-support-bot .

Run the container:

docker run -p 8000:8000 ai-support-bot

Note: Ollama must be reachable from inside the container for AI responses to work. The Ollama API address may need configuration for Docker.

📚 What I Learned

- Integrating a local Large Language Model (LLM)
- Building REST APIs with FastAPI
- Creating chat interfaces with Streamlit
- Connecting frontend and backend components
- Using Ollama to run an AI model locally
- Containerizing an application with Docker
- Managing source code using Git and GitHub

👨‍💻 Author

Ahmed Raza

GitHub: https://github.com/araza746745-code

📂 Repository

https://github.com/araza746745-code/AI_supportBot