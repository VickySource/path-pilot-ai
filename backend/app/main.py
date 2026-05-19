"""
Career AI Backend — FastAPI Application Entry Point
----------------------------------------------------
Registers all routers, configures CORS, sets up startup/shutdown hooks,
and exposes a health-check endpoint.

Run with:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.utils.logger import setup_logging
from app.api import upload, chat, search, skill_gap, documents

# ── Bootstrap ─────────────────────────────────────────────────────────────────

settings = get_settings()
setup_logging(debug=settings.debug)
logger = logging.getLogger(__name__)


# ── Lifespan (startup / shutdown) ─────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Code inside the `async with` block runs at startup.
    Code after `yield` runs at shutdown.
    """
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")

    # Ensure required directories exist
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.chroma_persist_dir).mkdir(parents=True, exist_ok=True)

    # Pre-warm the embedding model (loads it into memory once)
    from app.services.embedding_service import get_embedding_service
    embed_service = get_embedding_service()
    logger.info(f"Embedding model ready. Dimension: {embed_service.dimension}")

    # Pre-warm ChromaDB connection
    from app.db.chroma_client import get_chroma_client
    chroma = get_chroma_client()
    logger.info(f"ChromaDB ready. Total chunks: {chroma.collection_count}")

    # Check Ollama connectivity (non-fatal — warn but don't crash)
    from app.services.ollama_service import get_ollama_service
    ollama = get_ollama_service()
    healthy = await ollama.health_check()
    if not healthy:
        logger.warning(
            "Ollama is not reachable or the model is not available. "
            f"Run: ollama pull {settings.ollama_model}"
        )
    else:
        logger.info(f"Ollama ready. Model: {settings.ollama_model}")

    # Pre-compile LangGraph workflows
    from app.workflows.rag_workflow import get_rag_graph
    from app.workflows.skill_gap_workflow import get_skill_gap_graph
    get_rag_graph()
    get_skill_gap_graph()

    logger.info("All services initialised. Server is ready.")
    yield

    # ── Shutdown ──────────────────────────────────────────────────────────────
    logger.info("Shutting down...")


# ── App factory ───────────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Production-ready AI/RAG backend for career guidance and learning platforms. "
        "Powered by LangChain, LangGraph, Ollama (llama3), ChromaDB, and Sentence Transformers."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────

app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(search.router)
app.include_router(skill_gap.router)
app.include_router(documents.router)

# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/health", tags=["Health"], summary="Health check")
async def health_check():
    """
    Returns the health status of all backend services.
    Use this to verify the server is running before making other requests.
    """
    from app.services.ollama_service import get_ollama_service
    from app.db.chroma_client import get_chroma_client

    ollama_ok = await get_ollama_service().health_check()
    chroma = get_chroma_client()

    return JSONResponse(
        content={
            "status": "ok",
            "app": settings.app_name,
            "version": settings.app_version,
            "services": {
                "ollama": "ok" if ollama_ok else "unavailable",
                "chromadb": "ok",
                "embedding_model": settings.embedding_model,
                "llm_model": settings.ollama_model,
                "total_chunks_indexed": chroma.collection_count,
            },
        }
    )


@app.get("/", tags=["Health"], summary="Root")
async def root():
    return {"message": f"Welcome to {settings.app_name}", "docs": "/docs"}
