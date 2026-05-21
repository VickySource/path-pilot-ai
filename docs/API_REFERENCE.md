# API Reference (`/api/v1`)

All endpoints return JSON. Authenticated endpoints require
`Authorization: Bearer <jwt>` issued by `POST /auth/login`.

## Auth

| Method | Path | Body | Returns |
|---|---|---|---|
| POST | `/auth/register` | `{email, password, name}` | `UserPublic` |
| POST | `/auth/login` | `{email, password}` | `{access_token, user}` |
| GET  | `/auth/me` | — *(auth)* | `UserPublic` |

## Upload

| Method | Path | Body | Returns |
|---|---|---|---|
| POST | `/upload` | multipart `file=<pdf>` | `{document_id, filename, chunks}` |

## Skills

| Method | Path | Body | Returns |
|---|---|---|---|
| POST | `/skills/extract` | `{document_id}` | `Skill[]` |
| POST | `/skills/gaps` | `{skills, target_role}` | `Gap[]` |

## Roadmap

| Method | Path | Body | Returns |
|---|---|---|---|
| POST | `/roadmap/generate` | `{goal, skills?, document_id?}` | `Roadmap` |

## Chat

| Method | Path | Body | Returns |
|---|---|---|---|
| POST | `/chat` | `{sessionId, message}` | `{reply: ChatMessage}` |
| GET  | `/chat/{sessionId}` | — | `ChatMessage[]` |

## Analytics

| Method | Path | Body | Returns |
|---|---|---|---|
| GET | `/analytics/overview` | — *(auth)* | aggregate KPIs |

## Health

| Method | Path | Returns |
|---|---|---|
| GET | `/health` | `{status: "ok"}` |

## Errors

All errors follow:

```json
{ "error": { "message": "...", "code": "...", "details": {...} } }
```

Statuses: `400` validation, `401` unauthenticated, `403` forbidden,
`404` not found, `409` conflict, `500` server.