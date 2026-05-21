from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.pipeline import rag_pipeline

router = APIRouter()


class ChatRequest(BaseModel):
    sessionId: str
    message: str


@router.post("")
async def chat(req: ChatRequest) -> dict:
    reply = await rag_pipeline.answer(req.message)
    return {"reply": {"id": "tmp", "role": "assistant", "content": reply, "createdAt": ""}}


@router.get("/{session_id}")
async def history(session_id: str) -> list[dict]:
    # TODO: persist sessions
    return []
