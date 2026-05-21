# Database migrations

Async Alembic, configured in `backend/alembic.ini` and `backend/migrations/env.py`.
The environment reads `DATABASE_URL` from app settings (`.env`).

Quickstart:

```bash
# 1. start Postgres + pgvector
docker compose up -d postgres

# 2. enable pgvector once per database
psql "$DATABASE_URL" -c "CREATE EXTENSION IF NOT EXISTS vector;"

# 3. generate the first migration from the ORM metadata
cd backend
alembic revision --autogenerate -m "init"

# 4. apply
alembic upgrade head
```