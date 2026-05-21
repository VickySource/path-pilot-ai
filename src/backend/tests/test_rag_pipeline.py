import pytest


@pytest.mark.skip(reason="Requires running Ollama + populated vector store")
async def test_rag_answer():
    from app.rag.pipeline import rag_pipeline
    assert await rag_pipeline.answer("What is Python?")
