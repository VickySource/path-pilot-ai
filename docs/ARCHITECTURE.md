# Architecture

PathPilot AI is a monorepo with two independently-deployable services:

- **Frontend** (`/frontend`): Next.js 15 App Router, TypeScript, Tailwind. All backend calls go through `services/*.service.ts`, which use a shared `lib/api-client.ts` Axios instance.
- **Backend** (`/backend`): FastAPI on Python 3.11.7. Versioned under `/api/v1`. Layered as `routes → services → repositories → db` and `services → (rag | graph | embeddings | vectorstore) → llm.factory → provider`.
- **Database**: PostgreSQL 16 + pgvector. SQLAlchemy 2 (async), Alembic migrations. See [`DATABASE.md`](./DATABASE.md).
- **AI provider**: Lovable AI Gateway by default; OpenAI or Ollama selectable via `LLM_PROVIDER`. See [`AI_WORKFLOW.md`](./AI_WORKFLOW.md).

## High-level diagram

```
┌────────────────────┐                  ┌──────────────────────────────────────────────┐
│  Browser           │                  │  FastAPI (uvicorn)                           │
│  Next.js (App      │  HTTP /api/v1/*  │  ┌─────────┐  ┌──────────┐  ┌──────────────┐ │
│  Router) +         │ ───────────────▶ │  │ routes  │─▶│ services │─▶│ rag / graph  │ │
│  React Query       │ ◀─────────────── │  └─────────┘  └──────────┘  │ embeddings   │ │
│                    │      JSON        │                              │ vectorstore  │ │
└────────────────────┘                  │                              │ llm (Ollama) │ │
                                        │                              └──────┬───────┘ │
                                        │                                     │         │
                                        │             ChromaDB ◀──────────────┘         │
                                        │             (./data/chroma persisted)          │
                                        └──────────────────────────────────────────────┘
```

## Key flows

1. **Document ingestion**: `POST /upload` → save PDF → `pypdf` extract → `RecursiveCharacterTextSplitter` chunk → `sentence-transformers` embed → ChromaDB upsert under collection `resumes`.
2. **RAG chat**: `POST /chat` → `Retriever.retrieve(query)` against ChromaDB → prompt-stuff context → Ollama via `langchain-ollama` → answer.
3. **Roadmap workflow** (LangGraph): `retrieve → extract → gaps → roadmap → critique?`. Each node is a pure function operating on `CareerState`.

## Boundaries & scaling

- Frontend and backend share **no code**. The TypeScript `types/` mirror Pydantic models manually.
- ChromaDB is local/persistent for dev. For production, swap `vectorstore/chroma_client.py` for a hosted vector DB (Qdrant, Pinecone, Weaviate) without touching `embeddings/pipeline.py` or `rag/retriever.py`.
- Ollama is the default LLM provider. To swap to OpenAI/Anthropic, replace `llm/ollama_client.py` — chains and the graph remain unchanged.
- Auth uses JWT (HS256) in `utils/security.py`. Replace the in-memory `AuthService` with a database-backed user repository when ready.
