# AI Workflow

PathPilot AI uses a **provider-based** LLM architecture so the same chains,
RAG pipeline, and LangGraph workflows can run against any backend without
rewrites.

## Providers

| Provider | Module | When to use |
|---|---|---|
| **Lovable AI Gateway** (default) | `app/llm/lovable.py` | Hosted, fast, no local hardware. Recommended for prod and most dev. |
| OpenAI | `app/llm/openai_provider.py` | Bring your own OpenAI / compatible endpoint. |
| Ollama | `app/llm/ollama_client.py` | Local fallback / offline dev. |

Selection is driven by env:

```env
LLM_PROVIDER=lovable          # lovable | openai | ollama
LLM_MODEL=google/gemini-3-flash-preview
LLM_TEMPERATURE=0.2
LOVABLE_API_KEY=...           # required for lovable
```

The factory (`app/llm/factory.py`) returns an `LLMProvider` exposing:

- `as_runnable()` → a LangChain runnable for LCEL chains (`prompt | llm | parser`)
- `chat(prompt)` → one-shot async completion returning a string

## Layers

```text
routes → services → rag.pipeline / graph.workflow → llm.factory → provider
                                ↓
                          chains (LCEL) ← prompts/*
                                ↓
                          retriever ← vectorstore (chroma | pgvector)
```

- **`rag/chains.py`** — skills extraction, gap analysis, roadmap generation.
- **`rag/pipeline.py`** — RAG question answering (retrieve → stuff → answer).
- **`graph/workflow.py`** — LangGraph career workflow:
  `retrieve → extract → gaps → roadmap → critique?`.
- **`embeddings/pipeline.py`** — text → vectors, stored in Chroma (default)
  or pgvector once enabled.

## Swapping providers

No call sites need to change. Set `LLM_PROVIDER` and (if needed) provide the
matching API key. The factory is `lru_cache`d, so restart the process to pick
up a new provider during dev.