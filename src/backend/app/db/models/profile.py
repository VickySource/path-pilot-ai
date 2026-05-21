from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models._mixins import Timestamps, UUIDPrimaryKey


class Profile(Base, UUIDPrimaryKey, Timestamps):
    __tablename__ = "profiles"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False
    )
    headline: Mapped[str | None] = mapped_column(String(255))
    summary: Mapped[str | None] = mapped_column(String(2000))
    # Free-form structured fields stored as JSONB for flexibility.
    education: Mapped[list[dict] | None] = mapped_column(JSONB)
    experience: Mapped[list[dict] | None] = mapped_column(JSONB)
    interests: Mapped[list[str] | None] = mapped_column(JSONB)
    goals: Mapped[list[str] | None] = mapped_column(JSONB)
    target_roles: Mapped[list[str] | None] = mapped_column(JSONB)