"""
LangGraph RAG Workflow
----------------------
Defines a stateful multi-node graph that processes a user query through
clearly separated stages:

  query_understanding → retrieval → ranking → response_generation

Each node receives the shared WorkflowState TypedDict, enriches it,
and passes it to the next node. This makes the pipeline easy to debug,
extend, and test node by node.
"""

import logging
from typing import TypedDict, List, Optional, Dict, Any

from langgraph.graph import StateGraph, END

from app.config import get_settings
from app.services.embedding_service import get_embedding_service
from app.services.ollama_service import get_ollama_service
from app.db.chroma_client import get_chroma_client

logger = logging.getLogger(__name__)
settings = get_settings()


# ── Shared state ──────────────────────────────────────────────────────────────

class WorkflowState(TypedDict):
    """
    The state object that flows through every node in the graph.
    Each node reads from and writes to this dict.
    """
    # Input
    original_query: str
    document_id: Optional[str]
    top_k: int
    score_threshold: float

    # Set by query_understanding node
    refined_query: str
    query_intent: str          # e.g. "career_advice", "skill_gap", "general"

    # Set by retrieval node
    retrieved_chunks: List[Dict[str, Any]]

    # Set by ranking node
    ranked_chunks: List[Dict[str, Any]]

    # Set by response_generation node
    final_answer: str
    sources: List[Dict[str, Any]]

    # Error tracking
    error: Optional[str]


# ── Node implementations ──────────────────────────────────────────────────────

async def query_understanding_node(state: WorkflowState) -> WorkflowState:
    """
    Node 1 — Query Understanding
    Classifies the intent of the query and optionally refines it for
    better retrieval (e.g., expanding abbreviations, adding context).
    """
    query = state["original_query"]
    logger.info(f"[Node: query_understanding] Processing: '{query[:60]}'")

    # Simple rule-based intent classification
    # In production you could call the LLM here for richer classification
    query_lower = query.lower()
    if any(kw in query_lower for kw in ["skill gap", "missing skill", "what skills", "need to learn"]):
        intent = "skill_gap"
    elif any(kw in query_lower for kw in ["recommend", "suggest", "course", "learn", "roadmap"]):
        intent = "recommendation"
    elif any(kw in query_lower for kw in ["career", "job", "role", "position", "salary"]):
        intent = "career_advice"
    else:
        intent = "general"

    # Refine the query by appending intent context for better embedding match
    intent_context = {
        "skill_gap": "skill requirements gap analysis learning path",
        "recommendation": "course recommendation learning resources",
        "career_advice": "career guidance job role requirements",
        "general": "",
    }
    refined = f"{query} {intent_context.get(intent, '')}".strip()

    return {
        **state,
        "refined_query": refined,
        "query_intent": intent,
    }


async def retrieval_node(state: WorkflowState) -> WorkflowState:
    """
    Node 2 — Retrieval
    Embeds the refined query and fetches the top-k most relevant chunks
    from ChromaDB.
    """
    logger.info(f"[Node: retrieval] Intent='{state['query_intent']}'")

    try:
        embedding_service = get_embedding_service()
        chroma_client = get_chroma_client()

        query_embedding = embedding_service.embed_text(state["refined_query"])
        chunks = chroma_client.query(
            query_embedding=query_embedding,
            top_k=state["top_k"],
            document_id=state.get("document_id"),
            score_threshold=state["score_threshold"],
        )

        return {**state, "retrieved_chunks": chunks, "error": None}

    except Exception as exc:
        logger.error(f"[Node: retrieval] Error: {exc}")
        return {**state, "retrieved_chunks": [], "error": str(exc)}


async def ranking_node(state: WorkflowState) -> WorkflowState:
    """
    Node 3 — Ranking
    Re-ranks retrieved chunks by score and applies diversity filtering
    (avoids returning multiple chunks from the same document section).
    """
    logger.info(f"[Node: ranking] Ranking {len(state['retrieved_chunks'])} chunks")

    chunks = state["retrieved_chunks"]

    # Sort by relevance score descending
    sorted_chunks = sorted(chunks, key=lambda x: x.get("score", 0), reverse=True)

    # Diversity filter: keep at most 2 chunks per document to avoid repetition
    seen_docs: Dict[str, int] = {}
    diverse_chunks = []
    for chunk in sorted_chunks:
        doc_id = chunk.get("metadata", {}).get("document_id", "")
        count = seen_docs.get(doc_id, 0)
        if count < 2:
            diverse_chunks.append(chunk)
            seen_docs[doc_id] = count + 1

    return {**state, "ranked_chunks": diverse_chunks}


async def response_generation_node(state: WorkflowState) -> WorkflowState:
    """
    Node 4 — Response Generation
    Builds the final prompt from ranked context and calls the LLM.
    """
    logger.info(f"[Node: response_generation] Generating answer")

    ollama_service = get_ollama_service()
    chunks = state["ranked_chunks"]

    # Build context block
    if chunks:
        context_lines = []
        for i, chunk in enumerate(chunks, 1):
            meta = chunk.get("metadata", {})
            source = meta.get("source_file", "Unknown")
            score = chunk.get("score", 0.0)
            text = chunk.get("document", "")
            context_lines.append(f"[{i}] Source: {source} (score: {score:.2f})\n{text}")
        context = "\n\n".join(context_lines)
    else:
        context = "No relevant documents found in the knowledge base."

    system_prompt = (
        "You are an expert career guidance advisor. "
        "Answer the question using the provided context. "
        "Be specific, actionable, and cite sources when possible. "
        "If context is insufficient, say so clearly."
    )

    prompt = (
        f"Context:\n{context}\n\n"
        f"Question: {state['original_query']}\n\n"
        f"Provide a detailed, helpful answer:"
    )

    try:
        answer = await ollama_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
        )
    except Exception as exc:
        logger.error(f"[Node: response_generation] LLM error: {exc}")
        answer = (
            "I encountered an error generating a response. "
            "Please ensure Ollama is running and the model is available."
        )

    # Build sources list
    sources = [
        {
            "document_id": c.get("metadata", {}).get("document_id", ""),
            "source_file": c.get("metadata", {}).get("source_file", ""),
            "chunk_index": c.get("metadata", {}).get("chunk_index", 0),
            "score": c.get("score", 0.0),
            "preview": c.get("document", "")[:200],
        }
        for c in chunks
    ]

    return {**state, "final_answer": answer, "sources": sources}


# ── Graph assembly ────────────────────────────────────────────────────────────

def build_rag_graph() -> StateGraph:
    """
    Assemble and compile the LangGraph workflow.

    Graph topology:
      query_understanding → retrieval → ranking → response_generation → END
    """
    graph = StateGraph(WorkflowState)

    # Register nodes
    graph.add_node("query_understanding", query_understanding_node)
    graph.add_node("retrieval", retrieval_node)
    graph.add_node("ranking", ranking_node)
    graph.add_node("response_generation", response_generation_node)

    # Define edges (linear pipeline)
    graph.set_entry_point("query_understanding")
    graph.add_edge("query_understanding", "retrieval")
    graph.add_edge("retrieval", "ranking")
    graph.add_edge("ranking", "response_generation")
    graph.add_edge("response_generation", END)

    return graph.compile()


# ── Singleton ─────────────────────────────────────────────────────────────────

_rag_graph = None


def get_rag_graph():
    """Return the compiled LangGraph RAG workflow (built once)."""
    global _rag_graph
    if _rag_graph is None:
        _rag_graph = build_rag_graph()
        logger.info("LangGraph RAG workflow compiled successfully.")
    return _rag_graph
