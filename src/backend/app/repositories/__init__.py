"""Repository layer — abstracts persistence from services.

Each repository has at least one implementation (in-memory by default) and
optionally a SQLAlchemy implementation activated when `DATABASE_URL` is set.
"""