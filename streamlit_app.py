import uuid

import requests
import streamlit as st

st.set_page_config(
    page_title="HR Assistant",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            --bg: #f4efe8;
            --panel: rgba(255, 255, 255, 0.82);
            --panel-strong: #ffffff;
            --text: #1f2a27;
            --muted: #5f6f69;
            --accent: #c46f2f;
            --accent-2: #204c45;
            --border: rgba(31, 42, 39, 0.12);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(196, 111, 47, 0.16), transparent 28%),
                radial-gradient(circle at top right, rgba(32, 76, 69, 0.14), transparent 24%),
                linear-gradient(180deg, #fcfbf8 0%, #f4efe8 58%, #ece6dc 100%);
            color: var(--text);
        }

        .hero {
            padding: 1.25rem 1.35rem;
            border: 1px solid var(--border);
            border-radius: 20px;
            background: var(--panel);
            box-shadow: 0 20px 60px rgba(20, 28, 26, 0.08);
            backdrop-filter: blur(14px);
            margin-bottom: 1rem;
        }

        .hero h1 {
            margin: 0;
            font-size: 2rem;
            line-height: 1.1;
            color: var(--text);
        }

        .hero p {
            margin: 0.45rem 0 0;
            color: var(--muted);
            font-size: 0.98rem;
        }

        .stChatMessage {
            border-radius: 18px;
        }

        .stChatMessage[data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.75);
            border: 1px solid var(--border);
            box-shadow: 0 10px 30px rgba(20, 28, 26, 0.04);
        }

        .stChatMessage[data-testid="stChatMessage"] * {
            color: var(--text) !important;
        }

        .stChatMessage[data-testid="stChatMessage"] p,
        .stChatMessage[data-testid="stChatMessage"] li,
        .stChatMessage[data-testid="stChatMessage"] span,
        .stChatMessage[data-testid="stChatMessage"] div {
            color: var(--text) !important;
        }

        .typing-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.55rem 0.8rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.8);
            border: 1px solid var(--border);
            box-shadow: 0 8px 24px rgba(20, 28, 26, 0.05);
            font-weight: 600;
            color: var(--accent-2) !important;
        }

        .typing-dots {
            display: inline-flex;
            gap: 0.18rem;
        }

        .typing-dots span {
            width: 0.45rem;
            height: 0.45rem;
            border-radius: 999px;
            background: var(--accent);
            animation: typingPulse 1s infinite ease-in-out;
        }

        .typing-dots span:nth-child(2) {
            animation-delay: 0.15s;
        }

        .typing-dots span:nth-child(3) {
            animation-delay: 0.3s;
        }

        @keyframes typingPulse {
            0%, 80%, 100% { transform: scale(0.65); opacity: 0.45; }
            40% { transform: scale(1); opacity: 1; }
        }

        section[data-testid="stSidebar"] {
            display: none;
        }

        .block-container {
            padding-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "backend_url" not in st.session_state:
    st.session_state.backend_url = "http://localhost:8000"

st.markdown(
    """
    <div class="hero">
        <h1>HR Assistant</h1>
        <p>Ask about leave, payroll, attendance, policy, or follow-up questions. The assistant keeps track of your conversation so you can continue naturally.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.session_state.backend_url = st.session_state.backend_url.rstrip("/")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input("Ask a question about HR policy...")

if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown(
            """
            <div class="typing-indicator">
                <span>Bot is thinking</span>
                <span class="typing-dots"><span></span><span></span><span></span></span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            response = requests.post(
                f"{st.session_state.backend_url}/chat",
                json={
                    "session_id": st.session_state.session_id,
                    "message": user_message,
                },
                timeout=120,
            )
            response.raise_for_status()
            answer = response.json().get("answer", "")
        except requests.RequestException as exc:
            answer = f"Could not reach the backend: {exc}"

        typing_placeholder.empty()
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
