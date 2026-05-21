# API Contract — v1

Base URL: `${API_PREFIX}` (default `/api/v1`).

| Method | Path                      | Description                                |
|--------|---------------------------|--------------------------------------------|
| GET    | `/health`                 | Service health probe                       |
| POST   | `/auth/register`          | Create user account                        |
| POST   | `/auth/login`             | Exchange credentials for JWT               |
| POST   | `/upload`                 | Upload a PDF resume/document               |
| POST   | `/skills/extract`         | Extract skills from a previously uploaded document |
| POST   | `/skills/gap-analysis`    | Compute gaps vs a target role              |
| POST   | `/roadmap/generate`       | Generate personalized learning roadmap (LangGraph) |
| GET    | `/roadmap/{id}`           | Fetch a roadmap by id                      |
| GET    | `/roadmap`                | List roadmaps for current user             |
| POST   | `/chat`                   | RAG chat                                   |
| GET    | `/chat/{sessionId}`       | Fetch chat history                         |
| GET    | `/analytics/summary`      | Dashboard summary metrics                  |

Auth: `Authorization: Bearer <jwt>` on protected routes. Errors return:

```json
{ "error": { "message": "...", "code": "app_error" } }
```
