"""
Embedding Service
-----------------
Wraps sentence-transformers to produce dense vector embeddings.
The model is loaded once and reused across all requests (singleton pattern).
Supports single text and batch embedding.
"""

import logging
from typing import List
from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class EmbeddingService:
    """
    Singleton service that loads the sentence-transformer model once
    and exposes methods to embed single texts or batches.
    """

    def __init__(self, model_name: str = settings.embedding_model):
        logger.info(f"Loading embedding model: {model_name}")
        self.model_name = model_name
        # SentenceTransformer downloads the model on first use and caches it locally
        self._model = SentenceTransformer(model_name)
        logger.info("Embedding model loaded successfully.")

    def embed_text(self, text: str) -> List[float]:
        """
        Embed a single string and return a list of floats.

        Args:
            text: The text to embed.

        Returns:
            A list of floats representing the embedding vector.
        """
        if not text or not text.strip():
            raise ValueError("Cannot embed empty text.")
        embedding = self._model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of strings in one forward pass (more efficient than looping).

        Args:
            texts: List of strings to embed.

        Returns:
            List of embedding vectors (each is a list of floats).
        """
        if not texts:
            return []
        # Filter out empty strings to avoid errors
        clean_texts = [t if t.strip() else " " for t in texts]
        embeddings = self._model.encode(clean_texts, convert_to_numpy=True, batch_size=32)
        return [emb.tolist() for emb in embeddings]

    @property
    def dimension(self) -> int:
        """Return the embedding dimension for the loaded model."""
        return self._model.get_sentence_embedding_dimension()


@lru_cache()
def get_embedding_service() -> EmbeddingService:
    """Return the cached (singleton) EmbeddingService instance."""
    return EmbeddingService()
