"""
Ollama LLM Service
------------------
Wraps the Ollama Python client (>=0.4.x) to provide:
  - Standard (blocking) text generation
  - Streaming text generation
  - Health check
  - Graceful error handling

The service is designed to be injected via FastAPI's dependency system.
"""

import logging
from typing import AsyncGenerator, List, Dict, Any

import ollama
from ollama import AsyncClient

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class OllamaService:
    """
    Reusable service for interacting with a locally running Ollama instance.
    Uses the async client so it plays nicely with FastAPI's event loop.
    """

    def __init__(
        self,
        base_url: str = settings.ollama_base_url,
        model: str = settings.ollama_model,
        timeout: int = settings.ollama_timeout,
    ):
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        # Async client for use inside async endpoints
        self._async_client = AsyncClient(host=base_url)

    # ── Health ────────────────────────────────────────────────────────────────

    async def health_check(self) -> bool:
        """
        Ping Ollama to verify it is running and the model is available.

        Returns:
            True if healthy, False otherwise.
        """
        try:
            response = await self._async_client.list()
            # ollama 0.4.x returns an object with a 'models' attribute
            available = [m.model for m in response.models]
            if not any(self.model in m for m in available):
                logger.warning(
                    f"Model '{self.model}' not found in Ollama. "
                    f"Available: {available}. Run: ollama pull {self.model}"
                )
                return False
            return True
        except Exception as exc:
            logger.error(f"Ollama health check failed: {exc}")
            return False

    # ── Standard generation ───────────────────────────────────────────────────

    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
    ) -> str:
        """
        Send a prompt to Ollama and return the full response as a string.

        Args:
            prompt:        The user prompt / question.
            system_prompt: Optional system-level instructions.
            temperature:   Sampling temperature (0 = deterministic, 1 = creative).

        Returns:
            The model's response text.

        Raises:
            RuntimeError: If Ollama returns an error or is unreachable.
        """
        messages: List[Dict[str, str]] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            response = await self._async_client.chat(
                model=self.model,
                messages=messages,
                options={"temperature": temperature},
            )
            return response.message.content
        except Exception as exc:
            logger.error(f"Ollama generation failed: {exc}")
            raise RuntimeError(f"LLM generation error: {exc}") from exc

    # ── Chat with history ─────────────────────────────────────────────────────

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
    ) -> str:
        """
        Multi-turn chat: pass the full conversation history.

        Args:
            messages:    List of {"role": "user"/"assistant"/"system", "content": "..."}.
            temperature: Sampling temperature.

        Returns:
            The model's response text.
        """
        try:
            response = await self._async_client.chat(
                model=self.model,
                messages=messages,
                options={"temperature": temperature},
            )
            return response.message.content
        except Exception as exc:
            logger.error(f"Ollama chat failed: {exc}")
            raise RuntimeError(f"LLM chat error: {exc}") from exc

    # ── Streaming generation ──────────────────────────────────────────────────

    async def stream_generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        """
        Stream the model's response token by token.

        In ollama 0.4.x, streaming is enabled by passing stream=True to chat().
        The result is an async iterator of ChatResponse objects.

        Yields:
            Individual text chunks as they arrive from Ollama.
        """
        messages: List[Dict[str, str]] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            # stream=True returns an async generator directly in ollama 0.4.x
            async for chunk in await self._async_client.chat(
                model=self.model,
                messages=messages,
                stream=True,
                options={"temperature": temperature},
            ):
                content = chunk.message.content if chunk.message else ""
                if content:
                    yield content
        except Exception as exc:
            logger.error(f"Ollama streaming failed: {exc}")
            raise RuntimeError(f"LLM streaming error: {exc}") from exc


# ── Dependency injection helper ───────────────────────────────────────────────

_ollama_service: OllamaService | None = None


def get_ollama_service() -> OllamaService:
    """Return the shared OllamaService instance (created once at startup)."""
    global _ollama_service
    if _ollama_service is None:
        _ollama_service = OllamaService()
    return _ollama_service
