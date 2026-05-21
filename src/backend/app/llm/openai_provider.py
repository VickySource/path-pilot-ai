"""Generic OpenAI (or OpenAI-compatible) provider."""
from __future__ import annotations

from functools import lru_cache
from typing import Any

from langchain_openai import ChatOpenAI

from app.config import get_settings
from app.utils.errors import AppError


@lru_cache
def _client() -> ChatOpenAI:
    s = get_settings().llm
    if not s.openai_api_key:
        raise AppError(
            "OPENAI_API_KEY is not configured.",
            status_code=500,
            code="llm_not_configured",
        )
    return ChatOpenAI(
        model=s.model,
        temperature=s.temperature,
        base_url=s.openai_base_url,
        api_key=s.openai_api_key,
    )


class OpenAIProvider:
    name = "openai"

    def __init__(self) -> None:
        self.model = get_settings().llm.model

    def as_runnable(self) -> ChatOpenAI:
        return _client()

    async def chat(self, prompt: str, **opts: Any) -> str:
        result = await _client().ainvoke(prompt, **opts)
        return getattr(result, "content", str(result))