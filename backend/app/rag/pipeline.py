"""
RAG Pipeline
------------
Orchestrates the full Retrieval-Augmented Generation flow:

  1. Embed the user query
  2. Retrieve top-k relevant chunks from ChromaDB
  3. Build a context-aware prompt (with conversation history)
  4. Send to Ollama LLM
  5. Return the answer + source citations

This module is intentionally kept thin — it delegates to the individual
services (embedding, chroma, ollama) so each can be tested independently.
"""

import logging
from typing import List, Optional, Dict, Any

from app.config import get_settings
from app.services.embedding_service import get_embedding_service
from app.services.ollama_service import get_ollama_service
from app.db.chroma_client import get_chroma_client
from app.models.schemas import ChatMessage, Source

logger = logging.getLogger(__name__)
settings = get_settings()

# ── System prompt template ────────────────────────────────────────────────────

RAG_SYSTEM_PROMPT = """You are an expert career guidance and learning advisor.
Your job is to help users with career planning, skill development, and learning paths.

Use ONLY the provided context to answer the question.
If the context does not contain enough information, say so honestly — do NOT make up facts.
Always be specific, actionable, and encouraging.

When citing information, mention the source document name.
Format your response clearly with bullet points or numbered lists where appropriate."""


class RAGPipeline:
    """
    End-to-end RAG pipeline that ties together embedding, retrieval, and generation.
    """

    def __init__(self):
        self.embedding_service = get_embedding_service()
        self.ollama_service = get_ollama_service()
        self.chroma_client = get_chroma_client()

    # ── Main entry point ──────────────────────────────────────────────────────

    async def query(
        self,
        user_query: str,
        conversation_history: Optional[List[ChatMessage]] = None,
        document_id: Optional[str] = None,
        top_k: int = settings.top_k_results,
        score_threshold: float = settings.score_threshold,
    ) -> Dict[str, Any]:
        """
        Run the full RAG pipeline for a user question.

        Args:
            user_query:           The question from the user.
            conversation_history: Previous chat turns for multi-turn context.
            document_id:          Restrict retrieval to a specific document.
            top_k:                Number of chunks to retrieve.
            score_threshold:      Minimum relevance score for retrieved chunks.

        Returns:
            Dict with keys: answer, sources, query, model_used
        """
        logger.info(f"RAG query: '{user_query[:80]}...'")

        # Step 1 — Embed the query
        query_embedding = self.embedding_service.embed_text(user_query)

        # Step 2 — Retrieve relevant chunks
        raw_results = self.chroma_client.query(
            query_embedding=query_embedding,
            top_k=top_k,
            document_id=document_id,
            score_threshold=score_threshold,
        )

        # Step 3 — Build sources list for the response
        sources = self._build_sources(raw_results)

        # Step 4 — Build the prompt
        prompt = self._build_prompt(user_query, raw_results, conversation_history)

        # Step 5 — Generate answer via Ollama
        answer = await self.ollama_service.generate(
            prompt=prompt,
            system_prompt=RAG_SYSTEM_PROMPT,
            temperature=0.7,
        )

        return {
            "answer": answer,
            "sources": sources,
            "query": user_query,
            "model_used": settings.ollama_model,
        }

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _build_sources(self, raw_results: List[Dict[str, Any]]) -> List[Source]:
        """Convert raw ChromaDB results into Source schema objects."""
        sources = []
        for result in raw_results:
            meta = result.get("metadata", {})
            content = result.get("document", "")
            sources.append(
                Source(
                    document_id=meta.get("document_id", ""),
                    source_file=meta.get("source_file", ""),
                    chunk_index=meta.get("chunk_index", 0),
                    content_preview=content[:200],
                    relevance_score=result.get("score", 0.0),
                )
            )
        return sources

    def _build_prompt(
        self,
        user_query: str,
        retrieved_chunks: List[Dict[str, Any]],
        conversation_history: Optional[List[ChatMessage]],
    ) -> str:
        """
        Assemble the final prompt sent to the LLM.

        Structure:
          [Conversation history]
          [Retrieved context]
          [User question]
        """
        parts = []

        # Add conversation history for multi-turn context
        if conversation_history:
            history_text = "\n".join(
                f"{msg.role.upper()}: {msg.content}"
                for msg in conversation_history[-6:]  # keep last 6 turns
            )
            parts.append(f"CONVERSATION HISTORY:\n{history_text}\n")

        # Add retrieved context
        if retrieved_chunks:
            context_parts = []
            for i, chunk in enumerate(retrieved_chunks, 1):
                meta = chunk.get("metadata", {})
                source = meta.get("source_file", "Unknown")
                score = chunk.get("score", 0.0)
                text = chunk.get("document", "")
                context_parts.append(
                    f"[Source {i}: {source} | Relevance: {score:.2f}]\n{text}"
                )
            context_text = "\n\n---\n\n".join(context_parts)
            parts.append(f"RELEVANT CONTEXT:\n{context_text}\n")
        else:
            parts.append(
                "RELEVANT CONTEXT:\nNo specific documents found. "
                "Answer based on general career guidance knowledge.\n"
            )

        # Add the actual question
        parts.append(f"USER QUESTION:\n{user_query}")

        return "\n\n".join(parts)


# ── Singleton ─────────────────────────────────────────────────────────────────

_rag_pipeline: RAGPipeline | None = None


def get_rag_pipeline() -> RAGPipeline:
    """Return the shared RAGPipeline instance."""
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline()
    return _rag_pipeline
