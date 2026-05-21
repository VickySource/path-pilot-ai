from datetime import datetime, timezone
from uuid import uuid4

from app.models.chat import ChatMessage
from app.rag.pipeline import rag_pipeline


class ChatService:
    """Thin orchestrator over the RAG pipeline. Holds in-memory session
    history; swap `_sessions` for a persistent store when needed."""

    def __init__(self) -> None:
        self._sessions: dict[str, list[ChatMessage]] = {}

    async def send(self, session_id: str, content: str) -> ChatMessage:
        history = self._sessions.setdefault(session_id, [])
        history.append(ChatMessage(
            id=str(uuid4()), role="user", content=content,
            createdAt=datetime.now(timezone.utc),
        ))
        answer = await rag_pipeline.answer(content)
        reply = ChatMessage(
            id=str(uuid4()), role="assistant", content=answer,
            createdAt=datetime.now(timezone.utc),
        )
        history.append(reply)
        return reply

    async def history(self, session_id: str) -> list[ChatMessage]:
        return list(self._sessions.get(session_id, []))


chat_service = ChatService()