from fastapi import APIRouter
from pydantic import BaseModel

from app.services.roadmap_service import roadmap_service

router = APIRouter()


class GenerateRequest(BaseModel):
    goal: str
    documentId: str | None = None


@router.post("/generate")
async def generate(req: GenerateRequest) -> dict:
    return await roadmap_service.generate(req.goal, req.documentId)


@router.get("/{roadmap_id}")
async def get_one(roadmap_id: str) -> dict:
    return await roadmap_service.get(roadmap_id)


@router.get("")
async def list_all() -> list[dict]:
    return await roadmap_service.list()
