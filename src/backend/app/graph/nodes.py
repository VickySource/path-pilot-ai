"""LangGraph nodes for the career-navigation workflow.

Each node is a thin adapter that maps `CareerState` -> chain input -> partial
state update. Business logic lives in `app.rag.chains`."""
from __future__ import annotations

import json
from typing import Any

from app.graph.state import CareerState
from app.rag.chains import (
    gap_analysis_chain,
    roadmap_generation_chain,
    skills_extraction_chain,
)
from app.rag.retriever import Retriever
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _safe_json(raw: str, fallback: Any) -> Any:
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        logger.warning("Chain returned non-JSON output; using fallback")
        return fallback


async def node_retrieve_context(state: CareerState) -> CareerState:
    chunks = Retriever().retrieve(state.get("goal", ""))
    return {"context": "\n\n".join(chunks)}


async def node_extract_skills(state: CareerState) -> CareerState:
    raw = await skills_extraction_chain().ainvoke({"context": state.get("context", "")})
    return {"skills": _safe_json(raw, [])}


async def node_gap_analysis(state: CareerState) -> CareerState:
    raw = await gap_analysis_chain().ainvoke({
        "current_skills": json.dumps(state.get("skills", [])),
        "target_role": state.get("goal", ""),
    })
    return {"gaps": _safe_json(raw, [])}


async def node_generate_roadmap(state: CareerState) -> CareerState:
    raw = await roadmap_generation_chain().ainvoke({
        "goal": state.get("goal", ""),
        "gaps": json.dumps(state.get("gaps", [])),
        "context": state.get("context", ""),
    })
    return {"steps": _safe_json(raw, [])}


async def node_critique(state: CareerState) -> CareerState:
    # Reflection hook — extend with a critique chain when needed.
    return {"critique": ""}
