import os
from dataclasses import dataclass, field
from pathlib import Path
from threading import RLock
from typing import Dict, List, Tuple

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

def load_local_dotenv() -> None:
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue

        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_local_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")
MAX_RECENT_TURNS = int(os.getenv("MAX_RECENT_TURNS", "12"))

SYSTEM_INSTRUCTION = """
You are an HR AI Assistant for CheckinMe.

Your responsibilities:
- Answer ONLY HR-related questions
- Be polite and professional
- Use the provided HR policy and the conversation context
- If the question is unrelated, say:
  "I can only assist with HR-related questions."
""".strip()

HR_CONTEXT = """
Company HR Policy:
- Working hours: 9 AM - 6 PM
- Annual leave: 18 days per year
- Sick leave: 10 days per year
- Employees can work remotely 2 days per week
- Attendance and lateness rules
- Overtime and time-off approvals
- Payroll and salary date questions
- Probation and performance review guidance
- Resignation, notice period, and exit process
- Benefits, holidays, and company-wide HR announcements
""".strip()


@dataclass
class ConversationState:
    summary: str = ""
    history: List[Tuple[str, str]] = field(default_factory=list)


class ConversationManager:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction=SYSTEM_INSTRUCTION,
        )
        self.sessions: Dict[str, ConversationState] = {}
        self._lock = RLock()

    def _get_state(self, session_id: str) -> ConversationState:
        with self._lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = ConversationState()
            return self.sessions[session_id]

    @staticmethod
    def _format_turns(turns: List[Tuple[str, str]]) -> str:
        return "\n".join(
            f"{role.capitalize()}: {message}" for role, message in turns
        )

    def _summarize_old_context(
        self,
        existing_summary: str,
        old_turns: List[Tuple[str, str]],
    ) -> str:
        summary_source = []
        if existing_summary:
            summary_source.append(f"Existing summary:\n{existing_summary}")
        summary_source.append(
            f"New conversation to merge:\n{self._format_turns(old_turns)}"
        )

        summary_prompt = f"""
Summarize the HR conversation below in a compact way.
Keep only important facts, decisions, preferences, and unresolved questions.
Do not add new information.

{chr(10).join(summary_source)}
""".strip()

        try:
            response = self.model.generate_content(summary_prompt)
            return response.text.strip()
        except Exception:
            snippets = []
            for role, message in old_turns:
                text = " ".join(message.split())
                if len(text) > 180:
                    text = text[:177] + "..."
                snippets.append(f"{role.capitalize()}: {text}")
            fallback = " | ".join(snippets)
            if existing_summary:
                combined = f"{existing_summary}\n{fallback}".strip()
            else:
                combined = fallback
            return combined[:2000]

    def _compress_history_if_needed(self, session_id: str) -> None:
        with self._lock:
            state = self._get_state(session_id)
            if len(state.history) <= MAX_RECENT_TURNS:
                return
            overflow = state.history[:-MAX_RECENT_TURNS]
            state.history = state.history[-MAX_RECENT_TURNS:]
            existing_summary = state.summary

        new_summary = self._summarize_old_context(existing_summary, overflow)

        with self._lock:
            state = self._get_state(session_id)
            state.summary = new_summary

    def _build_prompt(self, session_id: str, user_input: str) -> str:
        state = self._get_state(session_id)
        recent_turns = self._format_turns(state.history)
        summary_block = state.summary or "No prior context yet."
        recent_block = recent_turns or "No recent conversation yet."

        return f"""
{HR_CONTEXT}

Conversation summary:
{summary_block}

Recent conversation:
{recent_block}

Current user question:
{user_input}

Answer using the HR policy and the stored conversation context.
If the user asks a follow-up, connect it to the earlier discussion.
""".strip()

    def ask(self, session_id: str, user_input: str) -> str:
        prompt = self._build_prompt(session_id, user_input)

        try:
            response = self.model.generate_content(prompt)
            answer = response.text
        except ResourceExhausted:
            return (
                "Gemini free-tier quota is exhausted; try again later or upgrade your plan."
            )
        except Exception as exc:
            return f"Sorry, I could not generate a response: {exc}"

        with self._lock:
            state = self._get_state(session_id)
            state.history.append(("user", user_input))
            state.history.append(("assistant", answer))

        self._compress_history_if_needed(session_id)
        return answer

    def reset(self, session_id: str) -> None:
        with self._lock:
            self.sessions.pop(session_id, None)

    def get_snapshot(self, session_id: str) -> ConversationState:
        state = self._get_state(session_id)
        return ConversationState(summary=state.summary, history=list(state.history))


conversation_manager = ConversationManager()
