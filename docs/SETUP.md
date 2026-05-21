# Setup

## Prerequisites

- Python 3.11.7, Node 20+, Docker (for Postgres).

## 1. Infra

```bash
docker compose up -d postgres
psql "postgresql://pathpilot:pathpilot@localhost:5432/pathpilot" \
  -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## 2. Backend

```bash
cd backend
cp .env.example .env             # set LOVABLE_API_KEY + DATABASE_URL
pip install -e ".[dev]"
alembic revision --autogenerate -m "init"    # first run only
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Skip the DB step entirely by leaving `DATABASE_URL` empty — the app falls
back to in-memory repositories (good for tests and quick demos).

## 3. Frontend

```bash
cd frontend
cp .env.local.example .env.local
bun install
bun dev
```

Visit http://localhost:3000.

## Optional: seed sample data

```bash
cd backend && python scripts/seed_vectorstore.py
```

## Optional: local Ollama instead of Lovable AI

Set `LLM_PROVIDER=ollama` in `backend/.env`, then:

```bash
ollama serve
ollama pull llama3.1:8b
```

## Live preview + local backend

The frontend is designed to run inside Lovable's live preview while the
FastAPI backend stays on your local machine.

1. Set `NEXT_PUBLIC_API_URL` in `frontend/.env.local` to a publicly reachable
   URL pointing at your local FastAPI (e.g. an `ngrok`/`cloudflared` tunnel
   to `http://localhost:8000`). The API client appends `/api/v1` automatically.
2. In `backend/.env`, keep `CORS_ORIGINS` for localhost and rely on
   `CORS_ORIGIN_REGEX` (default matches `*.lovable.app` / `*.lovable.dev`) to
   allow the live preview origin.
3. Start the backend (`uvicorn app.main:app --reload`) locally; the live
   preview frontend will call it through the tunnel.

## Smoke test

```bash
curl http://localhost:8000/api/v1/health
curl http://localhost:3000/api/health
```
