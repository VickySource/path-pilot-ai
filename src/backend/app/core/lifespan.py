from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.vectorstore.chroma_client import get_chroma_client


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup: warm singletons
    get_chroma_client()
    yield
    # Shutdown: nothing yet
