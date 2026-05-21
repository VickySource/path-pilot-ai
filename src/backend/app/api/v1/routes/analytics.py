from fastapi import APIRouter

from app.services.analytics_service import analytics_service

router = APIRouter()


@router.get("/summary")
async def summary() -> dict:
    return await analytics_service.summary()
