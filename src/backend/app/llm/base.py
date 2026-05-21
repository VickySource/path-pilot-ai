"""LLM provider protocol.

Every provider exposes the same minimal surface used by the rest of the app:

- `chat(prompt|messages)` for one-shot completion
- a LangChain-compatible runnable via `as_runnable()` so existing LCEL chains
  (`prompt | llm | parser`) keep working without rewrites.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from langchain_core.language_models.chat_models import BaseChatModel


@runtime_checkable
class LLMProvider(Protocol):
    name: str
    model: str

    def as_runnable(self) -> BaseChatModel:  # LangChain runnable
        ...

    async def chat(self, prompt: str, **opts: Any) -> str:
        ...