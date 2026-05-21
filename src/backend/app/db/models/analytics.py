from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models._mixins import Timestamps, UUIDPrimaryKey


class AnalyticsEvent(Base, UUIDPrimaryKey, Timestamps):
    __tablename__ = "analytics_events"

    user_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    type: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    payload: Mapped[dict | None] = mapped_column(JSONB)