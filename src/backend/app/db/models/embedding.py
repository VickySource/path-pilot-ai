from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models._mixins import Timestamps, UUIDPrimaryKey

# pgvector is optional at import time so the module loads even when the
# extension package isn't installed yet (e.g. running unit tests).
try:
    from pgvector.sqlalchemy import Vector  # type: ignore
    _HAS_PGVECTOR = True
except Exception:  # pragma: no cover
    Vector = None  # type: ignore
    _HAS_PGVECTOR = False

VECTOR_DIM = 384  # all-MiniLM-L6-v2 default; override per embedding provider.


class DocumentChunk(Base, UUIDPrimaryKey, Timestamps):
    __tablename__ = "document_chunks"

    user_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    meta: Mapped[dict | None] = mapped_column(JSONB)
    if _HAS_PGVECTOR:
        embedding: Mapped[list[float] | None] = mapped_column(Vector(VECTOR_DIM))  # type: ignore