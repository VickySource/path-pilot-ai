# Database

PathPilot AI persists data in **PostgreSQL 16** with the **pgvector**
extension for semantic search. ORM is **SQLAlchemy 2.x (async)** and
migrations are managed by **Alembic**.

## Tables

| Table | Purpose |
|---|---|
| `users` | Auth identities. Email + bcrypt password hash. |
| `profiles` | Per-user profile: education, experience, interests, goals, target roles. |
| `resumes` | Uploaded PDFs + AI-generated resumes (JSONB content). |
| `roadmaps`, `roadmap_steps` | Persisted roadmap output + step progress. |
| `skills`, `user_skills` | Skill catalog + per-user level/source. |
| `chat_sessions`, `chat_messages` | Persistent chat history. |
| `analytics_events` | Event log (uploads, generations, completions). |
| `document_chunks` | RAG chunks with `vector(384)` embeddings (pgvector). |

## Local setup

```bash
docker compose up -d postgres
psql "$DATABASE_URL" -c "CREATE EXTENSION IF NOT EXISTS vector;"

cd backend
alembic revision --autogenerate -m "init"   # one-time
alembic upgrade head
```

## In-memory fallback

When `DATABASE_URL` is unset, the app uses in-memory repositories so the
test suite and quick demos still work. The `UserRepository` interface
(`app/repositories/users_repo.py`) is implemented twice — `MemoryUserRepository`
and `SqlUserRepository` — selected by `get_user_repository()`.

## Naming convention

All constraint/index names follow the convention in `app/db/base.py`
(`ix_*`, `uq_*`, `fk_*`, `pk_*`) so Alembic autogenerate produces stable diffs.