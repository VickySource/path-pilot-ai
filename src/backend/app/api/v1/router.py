from fastapi import APIRouter

from app.api.v1.routes import analytics, auth, chat, health, roadmap, skills, upload

api_v1_router = APIRouter()
api_v1_router.include_router(health.router, tags=["health"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_v1_router.include_router(skills.router, prefix="/skills", tags=["skills"])
api_v1_router.include_router(roadmap.router, prefix="/roadmap", tags=["roadmap"])
api_v1_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_v1_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
