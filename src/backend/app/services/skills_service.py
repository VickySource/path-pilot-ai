import json

from app.rag.chains import gap_analysis_chain, skills_extraction_chain
from app.rag.retriever import Retriever
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _parse_json_list(raw: str) -> list[dict]:
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, TypeError):
        logger.warning("LLM returned non-JSON skills payload")
        return []


class SkillsService:
    """Skill extraction and gap analysis powered by RAG chains."""

    def __init__(self, retriever: Retriever | None = None) -> None:
        self._retriever = retriever or Retriever()

    async def extract(self, document_id: str) -> list[dict]:
        context = "\n\n".join(self._retriever.retrieve(document_id))
        raw = await skills_extraction_chain().ainvoke({"context": context})
        return _parse_json_list(raw)

    async def gap_analysis(self, target_role: str, current_skills: list[dict] | None = None) -> list[dict]:
        raw = await gap_analysis_chain().ainvoke({
            "current_skills": json.dumps(current_skills or []),
            "target_role": target_role,
        })
        return _parse_json_list(raw)


skills_service = SkillsService()
