"""Lovable AI Gateway provider (OpenAI-compatible).

Uses `langchain-openai`'s `ChatOpenAI` pointed at the Lovable gateway base URL.
The gateway expects the bearer token in `Authorization` and additionally
requires the `X-Lovable-AIG-SDK` header for telemetry/routing.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any

from langchain_openai import ChatOpenAI

from app.config import get_settings
from app.utils.errors import AppError


@lru_cache
def _client() -> ChatOpenAI:
    s = get_settings().llm
    if not s.lovable_api_key:
        raise AppError(
            "LOVABLE_API_KEY is not configured; set it or switch LLM_PROVIDER.",
            status_code=500,
            code="llm_not_configured",
        )
    return ChatOpenAI(
        model=s.model,
        temperature=s.temperature,
        base_url=s.lovable_base_url,
        api_key=s.lovable_api_key,
        default_headers={"X-Lovable-AIG-SDK": "langchain"},
    )


class LovableProvider:
    name = "lovable"

    def __init__(self) -> None:
        self.model = get_settings().llm.model

    def as_runnable(self) -> ChatOpenAI:
        return _client()

    async def chat(self, prompt: str, **opts: Any) -> str:
        result = await _client().ainvoke(prompt, **opts)
        return getattr(result, "content", str(result))