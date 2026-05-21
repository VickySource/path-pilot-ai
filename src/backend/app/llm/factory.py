"""Provider factory — resolves `LLM_PROVIDER` env into a concrete provider.

Usage:
    from app.llm.factory import get_llm
    llm = get_llm()
    chain = prompt | llm.as_runnable() | parser
    text = await llm.chat("hello")
"""
from __future__ import annotations

from functools import lru_cache

from app.config import get_settings
from app.llm.base import LLMProvider
from app.utils.errors import AppError


@lru_cache
def get_llm() -> LLMProvider:
    provider = (get_settings().llm.provider or "lovable").lower()
    if provider == "lovable":
        from app.llm.lovable import LovableProvider
        return LovableProvider()
    if provider == "openai":
        from app.llm.openai_provider import OpenAIProvider
        return OpenAIProvider()
    if provider == "ollama":
        from app.llm.ollama_client import OllamaProvider
        return OllamaProvider()
    raise AppError(f"Unknown LLM_PROVIDER: {provider}", status_code=500, code="llm_unknown_provider")


def get_chat_runnable():
    """Convenience: returns a LangChain runnable for use in LCEL chains."""
    return get_llm().as_runnable()