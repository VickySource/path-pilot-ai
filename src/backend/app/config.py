from functools import lru_cache
from pydantic import BaseModel, AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseModel):
    provider: str = "lovable"  # lovable | openai | ollama
    model: str = "google/gemini-3-flash-preview"
    temperature: float = 0.2
    # Lovable AI Gateway
    lovable_api_key: str | None = None
    lovable_base_url: str = "https://ai.gateway.lovable.dev/v1"
    # OpenAI (optional)
    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    # Ollama (fallback / local)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"


class VectorStoreSettings(BaseModel):
    chroma_dir: str = "./data/chroma"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    default_collection: str = "resumes"
    top_k: int = 5


class AuthSettings(BaseModel):
    jwt_secret: str = "change-me"
    jwt_alg: str = "HS256"
    jwt_expires_min: int = 60


class UploadSettings(BaseModel):
    upload_dir: str = "./data/uploads"
    max_upload_mb: int = 20


class DatabaseSettings(BaseModel):
    url: str | None = None  # e.g. postgresql+asyncpg://user:pass@host:5432/pathpilot
    echo: bool = False


class Settings(BaseSettings):
    """Centralized application settings, loaded from env (flat keys like
    OLLAMA_MODEL, CHROMA_DIR, JWT_SECRET) and grouped into sub-models for
    readability."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    api_prefix: str = "/api/v1"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    cors_origin_regex: str = r"^https://([a-z0-9-]+\.)*lovable\.(app|dev)$"

    # ---- LLM provider (flat env keys) ----
    llm_provider: str = "lovable"
    llm_model: str = "google/gemini-3-flash-preview"
    llm_temperature: float = 0.2
    lovable_api_key: str | None = None
    lovable_base_url: str = "https://ai.gateway.lovable.dev/v1"
    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"

    # ---- Database ----
    database_url: str | None = None
    database_echo: bool = False

    # Accept either CHROMA_DIR (legacy) or CHROMA_DB_DIR (current) from env.
    chroma_dir: str = Field(
        default="./chroma_db",
        validation_alias=AliasChoices("CHROMA_DB_DIR", "CHROMA_DIR", "chroma_dir"),
    )
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    jwt_secret: str = "change-me"
    jwt_alg: str = "HS256"
    jwt_expires_min: int = 60
    upload_dir: str = "./data/uploads"
    max_upload_mb: int = 20

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def llm(self) -> LLMSettings:
        return LLMSettings(
            provider=self.llm_provider,
            model=self.llm_model,
            temperature=self.llm_temperature,
            lovable_api_key=self.lovable_api_key,
            lovable_base_url=self.lovable_base_url,
            openai_api_key=self.openai_api_key,
            openai_base_url=self.openai_base_url,
            ollama_base_url=self.ollama_base_url,
            ollama_model=self.ollama_model,
        )

    @property
    def vector(self) -> VectorStoreSettings:
        return VectorStoreSettings(chroma_dir=self.chroma_dir, embedding_model=self.embedding_model)

    @property
    def auth(self) -> AuthSettings:
        return AuthSettings(
            jwt_secret=self.jwt_secret,
            jwt_alg=self.jwt_alg,
            jwt_expires_min=self.jwt_expires_min,
        )

    @property
    def upload(self) -> UploadSettings:
        return UploadSettings(upload_dir=self.upload_dir, max_upload_mb=self.max_upload_mb)

    @property
    def db(self) -> DatabaseSettings:
        return DatabaseSettings(url=self.database_url, echo=self.database_echo)


@lru_cache
def get_settings() -> Settings:
    return Settings()
