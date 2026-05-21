# PathPilot AI

AI-powered Career Copilot SaaS. Monorepo with a Next.js frontend and a FastAPI
backend. AI calls go through a **provider abstraction** (Lovable AI Gateway by
default, OpenAI or Ollama optional) so the same RAG + LangGraph workflows run
against any backend. Persistence is **PostgreSQL + pgvector** via SQLAlchemy
(async) and Alembic, with an in-memory fallback for tests.

> **Production app**: `/frontend` (Next.js) + `/backend` (FastAPI) — run locally.
>
> The repo root still contains a TanStack Start scaffold (`src/`, `vite.config.ts`,
> `wrangler.jsonc`). It is **not** part of the product and is kept only so the
> Lovable build/preview infrastructure keeps working. Do not add product code
> there — everything ships from `/frontend`.

## Layout

```
/
├── frontend/   # Next.js 15 + TypeScript + Tailwind
├── backend/    # FastAPI + Python 3.11.7 + LangChain/LangGraph/ChromaDB/Ollama
├── docs/       # Architecture, setup, API contract, AI workflow docs
└── README.md
```

## Quickstart

```bash
# 1. Infra (Postgres + pgvector)
docker compose up -d postgres

# 2. Backend
cd backend
cp .env.example .env             # set LOVABLE_API_KEY and DATABASE_URL
pip install -e ".[dev]"
alembic upgrade head             # after the first `alembic revision --autogenerate`
uvicorn app.main:app --reload --port 8000

# 3. Frontend (new terminal)
cd frontend
cp .env.local.example .env.local
bun install && bun dev
```

Open http://localhost:3000. See [`docs/SETUP.md`](docs/SETUP.md) for full instructions.

## Docs

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/AI_WORKFLOW.md`](docs/AI_WORKFLOW.md) — provider abstraction, RAG, LangGraph
- [`docs/DATABASE.md`](docs/DATABASE.md) — schema, migrations, pgvector
- [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md)
- [`docs/FOLDER_STRUCTURE.md`](docs/FOLDER_STRUCTURE.md)
- [`docs/SETUP.md`](docs/SETUP.md)

## Application flow

```
/login  →  /dashboard  →  /upload  →  /skills  →  /roadmap  →  /chat  →  /analytics
            (auth gate)   (PDF→Chroma) (RAG)     (LangGraph) (RAG)     (metrics)
```

Auth is enforced two ways:

1. **`frontend/middleware.ts`** redirects unauthenticated traffic away from
   protected routes (cookie-based).
2. **`AuthGate`** in `app/(dashboard)/layout.tsx` runs a client-side session
   check via `GET /auth/me` and bounces to `/login?next=…` on 401.

## Architecture highlights

- `frontend/providers/` — `AuthProvider`, `QueryProvider`, shared `Providers` shell.
- `frontend/services/` — typed Axios services, one per backend domain.
- `frontend/hooks/` — thin React hooks layered on services (`useChat`, `useUpload`, `useRoadmap`).
- `frontend/components/{layout,common,chat,upload,roadmap,dashboard,ui}/` — feature folders + design-system primitives.
- `backend/app/{api,services,rag,graph,embeddings,vectorstore,llm}/` — clean layering between transport, domain services, and AI workflows.
