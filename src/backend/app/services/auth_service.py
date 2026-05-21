from app.models.user import LoginRequest, RegisterRequest, TokenResponse, UserPublic
from app.repositories.users_repo import UserRepository, get_user_repository
from app.utils.errors import AppError
from app.utils.security import create_access_token, hash_password, verify_password


class AuthService:
    """Stateless service backed by a `UserRepository` (memory or SQL)."""

    def __init__(self, repo: UserRepository | None = None) -> None:
        self._repo = repo or get_user_repository()

    async def register(self, payload: RegisterRequest) -> UserPublic:
        if await self._repo.get_by_email(payload.email):
            raise AppError("Email already registered", status_code=409, code="email_exists")
        row = await self._repo.create(
            email=payload.email, name=payload.name,
            password_hash=hash_password(payload.password),
        )
        return _to_public(row)

    async def login(self, payload: LoginRequest) -> TokenResponse:
        row = await self._repo.get_by_email(payload.email)
        if not row or not verify_password(payload.password, row["password_hash"]):
            raise AppError("Invalid credentials", status_code=401, code="invalid_credentials")
        return TokenResponse(access_token=create_access_token(row["id"]), user=_to_public(row))

    async def me(self, user_id: str) -> UserPublic:
        row = await self._repo.get_by_id(user_id)
        if not row:
            raise AppError("User not found", status_code=404, code="user_not_found")
        return _to_public(row)


def _to_public(row: dict) -> UserPublic:
    return UserPublic(**{k: v for k, v in row.items() if k != "password_hash"})


auth_service = AuthService()
