"""User repository — in-memory + SQLAlchemy implementations behind one protocol."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Protocol
from uuid import uuid4


class UserRepository(Protocol):
    async def get_by_email(self, email: str) -> dict[str, Any] | None: ...
    async def get_by_id(self, user_id: str) -> dict[str, Any] | None: ...
    async def create(self, *, email: str, name: str, password_hash: str) -> dict[str, Any]: ...


class MemoryUserRepository:
    def __init__(self) -> None:
        self._users: dict[str, dict[str, Any]] = {}

    async def get_by_email(self, email: str) -> dict[str, Any] | None:
        return next((u for u in self._users.values() if u["email"] == email), None)

    async def get_by_id(self, user_id: str) -> dict[str, Any] | None:
        return self._users.get(user_id)

    async def create(self, *, email: str, name: str, password_hash: str) -> dict[str, Any]:
        uid = str(uuid4())
        row = {
            "id": uid,
            "email": email,
            "name": name,
            "password_hash": password_hash,
            "createdAt": datetime.now(timezone.utc),
        }
        self._users[uid] = row
        return row


class SqlUserRepository:
    """SQLAlchemy-backed implementation. Created lazily so importing this module
    without `DATABASE_URL` doesn't error."""

    async def _session(self):
        from app.db.session import _session_factory  # local import to defer DB init
        return _session_factory()()

    async def get_by_email(self, email: str) -> dict[str, Any] | None:
        from sqlalchemy import select
        from app.db.models.user import User
        async with await self._session() as s:
            res = await s.execute(select(User).where(User.email == email))
            u = res.scalar_one_or_none()
            return _to_dict(u) if u else None

    async def get_by_id(self, user_id: str) -> dict[str, Any] | None:
        from app.db.models.user import User
        async with await self._session() as s:
            u = await s.get(User, user_id)
            return _to_dict(u) if u else None

    async def create(self, *, email: str, name: str, password_hash: str) -> dict[str, Any]:
        from app.db.models.user import User
        async with await self._session() as s:
            u = User(email=email, name=name, password_hash=password_hash)
            s.add(u)
            await s.commit()
            await s.refresh(u)
            return _to_dict(u)


def _to_dict(u: Any) -> dict[str, Any]:
    return {
        "id": u.id,
        "email": u.email,
        "name": u.name,
        "password_hash": u.password_hash,
        "createdAt": u.created_at,
    }


def get_user_repository() -> UserRepository:
    """Picks SQL impl when DATABASE_URL is set, otherwise in-memory."""
    from app.db.session import is_configured
    if is_configured():
        return SqlUserRepository()
    return _memory_singleton


_memory_singleton: UserRepository = MemoryUserRepository()