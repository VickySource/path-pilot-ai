from datetime import datetime, timezone
from uuid import uuid4

from app.graph.workflow import run_career_workflow


class RoadmapService:
    def __init__(self) -> None:
        self._store: dict[str, dict] = {}

    async def generate(self, goal: str, document_id: str | None) -> dict:
        result = await run_career_workflow(goal=goal, document_id=document_id)
        roadmap = {
            "id": str(uuid4()),
            "userId": "anonymous",  # TODO: derive from current user
            "goal": goal,
            "steps": result.get("steps", []),
            "createdAt": datetime.now(timezone.utc).isoformat(),
        }
        self._store[roadmap["id"]] = roadmap
        return roadmap

    async def get(self, roadmap_id: str) -> dict:
        return self._store.get(roadmap_id, {})

    async def list(self) -> list[dict]:
        return list(self._store.values())


roadmap_service = RoadmapService()
