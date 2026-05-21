# Backend conventions

Layered architecture:

```
api/v1/routes  ──▶  services  ──▶  rag / graph / embeddings / vectorstore / llm / ingestion
```

- **Routes** are thin: parse input, call a service, return a model.
- **Services** hold business logic. They orchestrate AI modules.
- **AI modules** are reusable primitives, independent of FastAPI.

## Adding a new endpoint

1. Add Pydantic models in `app/models/<feature>.py`.
2. Add a service in `app/services/<feature>_service.py`.
3. Add a route module in `app/api/v1/routes/<feature>.py` and register it in `app/api/v1/router.py`.
4. Add tests in `backend/tests/test_<feature>.py`.

## Configuration

All settings live in `app/config.py` (Pydantic Settings, reads `backend/.env`). Use `get_settings()` to access them.
