"""
Chat Router — POST /chat
-------------------------
Accepts a user question (with optional conversation history) and returns
an AI-generated answer grounded in the indexed documents via the RAG pipeline.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException

from app.models.schemas import ChatRequest, ChatResponse
from app.rag.pipeline import RAGPipeline, get_rag_pipeline

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse, summary="Ask a question using RAG")
async def chat(
    request: ChatRequest,
    rag: RAGPipeline = Depends(get_rag_pipeline),
) -> ChatResponse:
    """
    Send a question to the AI assistant.

    The assistant retrieves relevant context from indexed documents and
    generates a grounded answer. Optionally pass `conversation_history`
    for multi-turn conversations.

    - **query**: Your question (required)
    - **conversation_history**: Previous messages for context (optional)
    - **document_id**: Restrict retrieval to a specific document (optional)
    """
    try:
        result = await rag.query(
            user_query=request.query,
            conversation_history=request.conversation_history,
            document_id=request.document_id,
        )

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            query=result["query"],
            model_used=result["model_used"],
        )

    except RuntimeError as exc:
        # LLM / Ollama errors
        logger.error(f"Chat error: {exc}")
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        )
    except Exception as exc:
        logger.error(f"Unexpected chat error: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error.")
