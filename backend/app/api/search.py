"""
Search Router — POST /search
------------------------------
Performs semantic similarity search over indexed documents.
Returns the top-k most relevant chunks with scores and metadata.
"""

import asyncio
import logging

from fastapi import APIRouter, Depends, HTTPException

from app.models.schemas import SearchRequest, SearchResponse, SearchResult
from app.services.embedding_service import EmbeddingService, get_embedding_service
from app.db.chroma_client import ChromaDBClient, get_chroma_client
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("", response_model=SearchResponse, summary="Semantic search over indexed documents")
async def semantic_search(
    request: SearchRequest,
    embed_service: EmbeddingService = Depends(get_embedding_service),
    chroma: ChromaDBClient = Depends(get_chroma_client),
) -> SearchResponse:
    """
    Perform a semantic similarity search.

    Returns the most relevant document chunks for the given query,
    ranked by cosine similarity score.

    - **query**: Search query text
    - **top_k**: Number of results (1–20, default 5)
    - **score_threshold**: Minimum similarity score (0–1, default 0.3)
    - **document_id**: Restrict search to a specific document (optional)
    """
    try:
        # Embed the query (CPU-bound, run in thread pool)
        query_embedding = await asyncio.to_thread(
            embed_service.embed_text, request.query
        )

        # Query ChromaDB (sync client, run in thread pool)
        raw_results = await asyncio.to_thread(
            chroma.query,
            query_embedding=query_embedding,
            top_k=request.top_k or settings.top_k_results,
            document_id=request.document_id,
            score_threshold=request.score_threshold or settings.score_threshold,
        )

        # Map to response schema
        results = [
            SearchResult(
                document_id=r["metadata"].get("document_id", ""),
                source_file=r["metadata"].get("source_file", ""),
                chunk_index=r["metadata"].get("chunk_index", 0),
                content=r["document"],
                score=r["score"],
                metadata=r["metadata"],
            )
            for r in raw_results
        ]

        return SearchResponse(
            query=request.query,
            results=results,
            total_found=len(results),
        )

    except Exception as exc:
        logger.error(f"Search error: {exc}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(exc)}")
