# Roadmap

Near-term:
- Replace in-memory `AuthService` with a real DB (Postgres + SQLAlchemy / SQLModel).
- Persist chat sessions and roadmaps.
- Add TanStack Query on the frontend for caching/invalidations.
- Implement the LangGraph node bodies (currently stubs).
- Add Alembic migrations once a DB is wired in.

Scaling:
- Swap ChromaDB for a hosted vector DB (Qdrant Cloud, Pinecone, Weaviate).
- Swap Ollama for a hosted LLM (OpenAI/Anthropic) via the same `llm/` interface.
- Containerize both services (Dockerfile included for backend) and run behind a reverse proxy.
- Add observability: OpenTelemetry for FastAPI, frontend RUM.
