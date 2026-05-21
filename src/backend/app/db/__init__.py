"""Persistence layer — SQLAlchemy (async) + pgvector.

Activates only when `DATABASE_URL` is set. When unset, the app falls back to
in-memory repositories so it stays runnable in tests and quick demos.
"""