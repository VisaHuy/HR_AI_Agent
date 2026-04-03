from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from agent_core import conversation_manager

app = FastAPI(title="HR Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str = Field(default="default-session", min_length=1)
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    session_id: str
    answer: str


class ResetResponse(BaseModel):
    session_id: str
    status: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = conversation_manager.ask(request.session_id, request.message)
    return ChatResponse(session_id=request.session_id, answer=answer)


@app.post("/reset/{session_id}", response_model=ResetResponse)
def reset_session(session_id: str):
    conversation_manager.reset(session_id)
    return ResetResponse(session_id=session_id, status="reset")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
