"""
Application configuration loaded from .env file.
All settings are validated by Pydantic at startup.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    # ── App ──────────────────────────────────────────────────────
    app_name: str = Field(default="Career AI Backend")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)

    # ── Ollama ───────────────────────────────────────────────────
    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="llama3")
    ollama_timeout: int = Field(default=120)

    # ── ChromaDB ─────────────────────────────────────────────────
    chroma_persist_dir: str = Field(default="./chroma_db")
    chroma_collection_name: str = Field(default="career_docs")

    # ── Embeddings ───────────────────────────────────────────────
    embedding_model: str = Field(default="all-MiniLM-L6-v2")

    # ── Chunking ─────────────────────────────────────────────────
    chunk_size: int = Field(default=1000)
    chunk_overlap: int = Field(default=200)

    # ── File Upload ──────────────────────────────────────────────
    upload_dir: str = Field(default="./uploads")
    max_file_size_mb: int = Field(default=20)
    allowed_extensions: str = Field(default="pdf,docx,txt")

    # ── Retrieval ────────────────────────────────────────────────
    top_k_results: int = Field(default=5)
    score_threshold: float = Field(default=0.3)

    @property
    def allowed_extensions_list(self) -> list[str]:
        return [ext.strip().lower() for ext in self.allowed_extensions.split(",")]

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance (loaded once at startup)."""
    return Settings()
