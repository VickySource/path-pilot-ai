"""
Documents Router
-----------------
GET  /documents          — List all indexed documents
DELETE /document/{id}    — Delete a document and all its chunks
"""

import asyncio
import logging

from fastapi import APIRouter, Depends, HTTPException

from app.models.schemas import DocumentInfo, DeleteResponse
from app.db.chroma_client import ChromaDBClient, get_chroma_client
from app.services.document_service import DocumentService, get_document_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Documents"])


@router.get("/documents", response_model=list[DocumentInfo], summary="List all indexed documents")
async def list_documents(
    chroma: ChromaDBClient = Depends(get_chroma_client),
) -> list[DocumentInfo]:
    """
    Return a list of all documents currently indexed in ChromaDB.
    Each entry includes the document ID, filename, type, chunk count, and upload time.
    """
    try:
        docs = await asyncio.to_thread(chroma.list_documents)
        return [DocumentInfo(**d) for d in docs]
    except Exception as exc:
        logger.error(f"List documents error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete(
    "/document/{document_id}",
    response_model=DeleteResponse,
    summary="Delete a document and all its chunks",
)
async def delete_document(
    document_id: str,
    chroma: ChromaDBClient = Depends(get_chroma_client),
    doc_service: DocumentService = Depends(get_document_service),
) -> DeleteResponse:
    """
    Permanently delete a document from ChromaDB and the uploads directory.

    This removes all chunks and embeddings associated with the document.
    The action is irreversible — the document must be re-uploaded to restore it.
    """
    try:
        # Delete from ChromaDB
        deleted_count = await asyncio.to_thread(chroma.delete_document, document_id)

        if deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Document '{document_id}' not found.",
            )

        # Delete the physical file from disk
        await asyncio.to_thread(doc_service.delete_file, document_id)

        return DeleteResponse(
            success=True,
            document_id=document_id,
            message=f"Document deleted. Removed {deleted_count} chunks.",
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Delete document error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))
