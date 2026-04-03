HR AI Agent
A simple HR assistant built with:

FastAPI backend for chat API
Streamlit frontend for chat UI
Google Gemini for response generation and context-aware follow-up handling
Project files:

main.py:1
agent_core.py:1
streamlit_app.py:1
requirements.txt:1
.env.example:1
Features
HR-only assistant behavior with policy context
Session-based memory and follow-up support
Conversation compression for long chats
Web UI with chat experience and typing indicator
REST API endpoints for health, chat, and session reset
Requirements
Python 3.10+
A Google AI API key
Setup
Open terminal in the ai-agent folder.

Create and activate virtual environment.

Windows PowerShell:
python -m venv .venv
Activate.ps1

Install dependencies.
pip install -r requirements.txt

Create environment file.
copy .env.example .env

Edit .env and set your key.
GOOGLE_API_KEY=your_google_api_key_here

Optional environment variables:
GEMINI_MODEL=models/gemini-2.5-flash
MAX_RECENT_TURNS=12

Run The Project
Run backend API first:
python main.py

The API starts at:
http://localhost:8000

Health check:
http://localhost:8000/health

Then run Streamlit app in another terminal:
streamlit run streamlit_app.py

Open browser:
http://localhost:8501

API Endpoints
GET /health
POST /chat
POST /reset/{session_id}
Example chat request:
POST /chat
{
"session_id": "demo-session",
"message": "How many annual leave days do I have?"
}

Quick Test For Gemini Access
You can check available models:
python test_api.py
