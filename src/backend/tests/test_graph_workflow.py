import pytest


@pytest.mark.skip(reason="Requires Ollama; node implementations are stubs")
async def test_workflow_runs():
    from app.graph.workflow import run_career_workflow
    out = await run_career_workflow(goal="Become a senior ML engineer")
    assert "steps" in out
