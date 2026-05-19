"""
Upload Router — POST /upload
-----------------------------
Accepts a document file, extracts text, chunks it, generates embeddings,
and stores everything in ChromaDB.
"""

import asyncio
import logging
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from app.config import get_settings
from app.models.schemas import UploadResponse
from app.services.document_service import DocumentService, get_document_service
from app.services.embedding_service import EmbeddingService, get_embedding_service
from app.db.chroma_client import ChromaDBClient, get_chroma_client

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/upload", tags=["Documents"])


@router.post("", response_model=UploadResponse, summary="Upload a document for RAG indexing")
async def upload_document(
    file: UploadFile = File(..., description="PDF, DOCX, or TXT file"),
    doc_service: DocumentService = Depends(get_document_service),
    embed_service: EmbeddingService = Depends(get_embedding_service),
    chroma: ChromaDBClient = Depends(get_chroma_client),
) -> UploadResponse:
    """
    Upload and index a document.

    Steps:
    1. Validate file type and size
    2. Save to disk
    3. Extract text
    4. Chunk text
    5. Generate embeddings (batch)
    6. Store in ChromaDB

    Returns the document ID and chunk count.
    """
    # ── 1. Validate ───────────────────────────────────────────────────────────
    doc_service.validate_file(file)
    content = await doc_service.validate_file_size(file)

    file_ext = Path(file.filename).suffix.lstrip(".").lower()

    # ── 2. Save to disk ───────────────────────────────────────────────────────
    document_id, save_path = await doc_service.save_file(content, file.filename)

    try:
        # ── 3. Extract text ───────────────────────────────────────────────────
        text = doc_service.extract_text(save_path, file_ext)
        if not text.strip():
            raise HTTPException(
                status_code=422,
                detail="Could not extract any text from the uploaded file.",
            )

        # ── 4. Chunk text ─────────────────────────────────────────────────────
        chunks = doc_service.chunk_text(text)

        # ── 5. Generate embeddings (run in thread pool — CPU-bound) ───────────
        embeddings = await asyncio.to_thread(embed_service.embed_batch, chunks)

        # ── 6. Store in ChromaDB (run in thread pool — sync client) ───────────
        await asyncio.to_thread(
            chroma.add_chunks,
            document_id=document_id,
            chunks=chunks,
            embeddings=embeddings,
            source_file=file.filename,
            file_type=file_ext,
        )

        logger.info(
            f"Document '{file.filename}' indexed as '{document_id}' "
            f"with {len(chunks)} chunks."
        )

        return UploadResponse(
            success=True,
            document_id=document_id,
            filename=file.filename,
            total_chunks=len(chunks),
            message=f"Document indexed successfully with {len(chunks)} chunks.",
        )

    except HTTPException:
        raise
    except Exception as exc:
        # Clean up the saved file if indexing fails
        doc_service.delete_file(document_id)
        logger.error(f"Upload failed for '{file.filename}': {exc}")
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(exc)}")
