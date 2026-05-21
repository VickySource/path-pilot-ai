# Folder structure

```text
pathpilot/
├── frontend/                 # Next.js 15 app (App Router, TS, Tailwind)
│   ├── app/                  # routes (auth, dashboard, api)
│   ├── components/           # ui, layout, common, feature widgets
│   ├── hooks/                # useAuth, useChat, useUpload, useRoadmap
│   ├── lib/                  # api-client, auth, env, constants
│   ├── providers/            # AuthProvider, QueryProvider
│   ├── services/             # *.service.ts thin wrappers over apiClient
│   ├── types/                # shared TS types mirroring backend models
│   └── middleware.ts         # cookie-based route protection
│
├── backend/                  # FastAPI service
│   ├── app/
│   │   ├── api/v1/routes/    # thin HTTP handlers
│   │   ├── services/         # business logic
│   │   ├── repositories/     # persistence abstraction (memory + SQL)
│   │   ├── db/
│   │   │   ├── base.py       # Declarative Base + naming convention
│   │   │   ├── session.py    # async engine, AsyncSessionLocal, get_db
│   │   │   └── models/       # ORM models per domain
│   │   ├── llm/              # provider abstraction (lovable | openai | ollama)
│   │   ├── rag/              # chains, pipeline, retriever, prompts
│   │   ├── graph/            # LangGraph nodes, edges, workflow, state
│   │   ├── embeddings/       # embedding pipeline + provider
│   │   ├── ingestion/        # pdf_loader, splitter, normalizer
│   │   ├── vectorstore/      # chroma_client, collections
│   │   ├── models/           # Pydantic request/response models
│   │   ├── core/             # lifespan, middleware
│   │   └── utils/            # errors, logger, security, responses, files
│   ├── migrations/           # Alembic (env.py, versions/, script.py.mako)
│   ├── tests/                # pytest
│   ├── alembic.ini
│   ├── pyproject.toml
│   └── .env.example
│
├── docs/                     # architecture, AI, DB, API, setup
├── docker-compose.yml        # local Postgres + pgvector
└── README.md
```

## Layered backend

```text
routes/  → services/  → repositories/ → db/models
                     ↘ rag | graph | embeddings | vectorstore
                                       ↘ llm.factory → provider
```

Routes never touch the DB or LLM directly — they always go through a service.