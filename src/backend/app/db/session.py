"""Async SQLAlchemy engine + session factory.

Engine is lazily created on first use so importing this module without
`DATABASE_URL` is safe (the app must remain runnable in in-memory mode).
"""
from __future__ import annotations

from collections.abc import AsyncIterator
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings
from app.utils.errors import AppError


@lru_cache
def get_engine():
    url = get_settings().db.url
    if not url:
        raise AppError(
            "DATABASE_URL is not configured. Set it to enable persistent storage.",
            status_code=500,
            code="db_not_configured",
        )
    return create_async_engine(url, echo=get_settings().db.echo, pool_pre_ping=True)


@lru_cache
def _session_factory() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(get_engine(), class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency yielding an async session with auto-rollback on error."""
    session = _session_factory()()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


def is_configured() -> bool:
    return bool(get_settings().db.url)