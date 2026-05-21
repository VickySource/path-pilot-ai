from fastapi import APIRouter, Depends

from app.models.user import LoginRequest, RegisterRequest, TokenResponse, UserPublic
from app.api.deps import get_current_user_id
from app.services.auth_service import auth_service

router = APIRouter()


@router.post("/register", response_model=UserPublic)
async def register(payload: RegisterRequest) -> UserPublic:
    return await auth_service.register(payload)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    return await auth_service.login(payload)


@router.get("/me", response_model=UserPublic)
async def me(user_id: str = Depends(get_current_user_id)) -> UserPublic:
    return await auth_service.me(user_id)
