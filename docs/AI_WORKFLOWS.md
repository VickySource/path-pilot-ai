# AI Workflows

## RAG pipeline (`app/rag/pipeline.py`)

```
question ──▶ Retriever (ChromaDB top-k) ──▶ prompt with context ──▶ ChatOllama ──▶ answer
```

Independently callable — used by `/chat` and as a primitive inside the LangGraph workflow.

## LangGraph career workflow (`app/graph/workflow.py`)

```
       ┌──────────┐
       │ retrieve │  context from vector store
       └────┬─────┘
            ▼
       ┌──────────┐
       │ extract  │  skills extraction LLM chain
       └────┬─────┘
            ▼
       ┌──────────┐
       │  gaps    │  gap analysis vs target role/goal
       └────┬─────┘
            ▼
       ┌──────────┐
       │ roadmap  │  step-by-step roadmap generation
       └────┬─────┘
            ▼
     ┌──────────────┐
     │  critique?   │  conditional reflection
     └──────┬───────┘
            ▼
           END
```

State is a `TypedDict` (`app/graph/state.py`) so each node returns a partial state that LangGraph merges.

## Extending

- Add a new node: create a function in `app/graph/nodes.py`, register it in `workflow.py`, and wire edges.
- Swap LLM provider: replace `app/llm/ollama_client.py`.
- Swap vector store: replace `app/vectorstore/chroma_client.py` — `Retriever` and `EmbeddingsPipeline` use the collection abstraction.
