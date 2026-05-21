from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models._mixins import Timestamps, UUIDPrimaryKey


class Roadmap(Base, UUIDPrimaryKey, Timestamps):
    __tablename__ = "roadmaps"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    goal: Mapped[str] = mapped_column(String(255), nullable=False)
    meta: Mapped[dict | None] = mapped_column(JSONB)


class RoadmapStep(Base, UUIDPrimaryKey, Timestamps):
    __tablename__ = "roadmap_steps"

    roadmap_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("roadmaps.id", ondelete="CASCADE"), index=True, nullable=False
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000))
    estimated_hours: Mapped[int | None] = mapped_column(Integer)
    resources: Mapped[list[dict] | None] = mapped_column(JSONB)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)