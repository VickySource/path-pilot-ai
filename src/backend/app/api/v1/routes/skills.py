from fastapi import APIRouter
from pydantic import BaseModel

from app.services.skills_service import skills_service

router = APIRouter()


class ExtractRequest(BaseModel):
    documentId: str


class GapRequest(BaseModel):
    targetRole: str


@router.post("/extract")
async def extract(req: ExtractRequest) -> dict:
    return {"skills": await skills_service.extract(req.documentId)}


@router.post("/gap-analysis")
async def gap_analysis(req: GapRequest) -> dict:
    return {"gaps": await skills_service.gap_analysis(req.targetRole)}
