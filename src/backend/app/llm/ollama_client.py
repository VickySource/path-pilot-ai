"""Ollama provider — optional local fallback."""
from __future__ import annotations

from functools import lru_cache
from typing import Any

from langchain_ollama import ChatOllama

from app.config import get_settings


@lru_cache
def _client() -> ChatOllama:
    s = get_settings().llm
    return ChatOllama(base_url=s.ollama_base_url, model=s.ollama_model, temperature=s.temperature)


class OllamaProvider:
    name = "ollama"

    def __init__(self) -> None:
        self.model = get_settings().llm.ollama_model

    def as_runnable(self) -> ChatOllama:
        return _client()

    async def chat(self, prompt: str, **opts: Any) -> str:
        result = await _client().ainvoke(prompt, **opts)
        return getattr(result, "content", str(result))


# Back-compat alias for legacy imports.
def get_chat_llm() -> ChatOllama:
    return _client()
