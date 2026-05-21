"""Seed the ChromaDB store with sample learning-resource snippets."""
from app.embeddings.pipeline import embeddings_pipeline

SAMPLES = [
    "Python is a high-level interpreted programming language.",
    "FastAPI is a modern Python web framework for building APIs.",
    "LangGraph orchestrates multi-step LLM workflows as stateful graphs.",
]

if __name__ == "__main__":
    embeddings_pipeline.upsert(document_id="seed", chunks=SAMPLES, collection="learning")
    print(f"Seeded {len(SAMPLES)} chunks into 'learning' collection.")
