"""
ChromaDB Client
---------------
Manages the persistent ChromaDB collection used to store document chunks
and their embeddings.

Responsibilities:
  - Initialize the persistent client and collection (once at startup)
  - Add chunks with embeddings and metadata
  - Query by embedding vector (similarity search)
  - Delete all chunks belonging to a document
  - List unique documents stored in the collection
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from functools import lru_cache

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class ChromaDBClient:
    """
    Thin wrapper around the ChromaDB persistent client.
    All methods are synchronous because ChromaDB's Python client is sync.
    Async endpoints call these methods in a thread pool via asyncio.to_thread().
    """

    def __init__(self):
        # PersistentClient stores data on disk so it survives restarts
        self._client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )

        # get_or_create_collection is idempotent — safe to call on every startup
        self._collection = self._client.get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={"hnsw:space": "cosine"},  # use cosine similarity
        )
        logger.info(
            f"ChromaDB ready. Collection '{settings.chroma_collection_name}' "
            f"has {self._collection.count()} chunks."
        )

    # ── Write ─────────────────────────────────────────────────────────────────

    def add_chunks(
        self,
        document_id: str,
        chunks: List[str],
        embeddings: List[List[float]],
        source_file: str,
        file_type: str,
    ) -> None:
        """
        Store a list of text chunks with their embeddings and metadata.

        Args:
            document_id: UUID of the parent document.
            chunks:      List of text strings (one per chunk).
            embeddings:  Corresponding embedding vectors.
            source_file: Original filename.
            file_type:   'pdf', 'docx', or 'txt'.
        """
        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings must have the same length.")

        ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
        uploaded_at = datetime.now(timezone.utc).isoformat()

        metadatas = [
            {
                "document_id": document_id,
                "source_file": source_file,
                "file_type": file_type,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "uploaded_at": uploaded_at,
            }
            for i in range(len(chunks))
        ]

        # ChromaDB accepts batches natively
        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )
        logger.info(f"Added {len(chunks)} chunks for document '{document_id}'.")

    # ── Query ─────────────────────────────────────────────────────────────────

    def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        document_id: Optional[str] = None,
        score_threshold: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """
        Perform a similarity search against stored embeddings.

        Args:
            query_embedding: The embedding of the user's query.
            top_k:           Maximum number of results to return.
            document_id:     If set, restrict results to this document.
            score_threshold: Minimum similarity score (0–1). Lower = more results.

        Returns:
            List of dicts with keys: id, document, metadata, score.
        """
        where_filter = {"document_id": document_id} if document_id else None

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, max(self._collection.count(), 1)),
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        # ChromaDB returns distances (lower = more similar for cosine).
        # Convert distance → similarity score: score = 1 - distance
        output = []
        if results["ids"] and results["ids"][0]:
            for idx, chunk_id in enumerate(results["ids"][0]):
                distance = results["distances"][0][idx]
                score = round(1.0 - distance, 4)

                if score < score_threshold:
                    continue  # skip results below the threshold

                output.append(
                    {
                        "id": chunk_id,
                        "document": results["documents"][0][idx],
                        "metadata": results["metadatas"][0][idx],
                        "score": score,
                    }
                )

        return output

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete_document(self, document_id: str) -> int:
        """
        Delete all chunks belonging to a document.

        Returns:
            Number of chunks deleted.
        """
        # Fetch IDs first so we know what to delete
        existing = self._collection.get(
            where={"document_id": document_id},
            include=[],
        )
        ids_to_delete = existing["ids"]

        if ids_to_delete:
            self._collection.delete(ids=ids_to_delete)
            logger.info(f"Deleted {len(ids_to_delete)} chunks for document '{document_id}'.")
        else:
            logger.warning(f"No chunks found for document '{document_id}'.")

        return len(ids_to_delete)

    # ── List ──────────────────────────────────────────────────────────────────

    def list_documents(self) -> List[Dict[str, Any]]:
        """
        Return a deduplicated list of documents stored in the collection.

        Returns:
            List of dicts with document-level metadata.
        """
        all_items = self._collection.get(include=["metadatas"])
        seen: Dict[str, Dict[str, Any]] = {}

        for meta in all_items.get("metadatas", []):
            doc_id = meta.get("document_id", "")
            if doc_id and doc_id not in seen:
                seen[doc_id] = {
                    "document_id": doc_id,
                    "source_file": meta.get("source_file", ""),
                    "file_type": meta.get("file_type", ""),
                    "total_chunks": meta.get("total_chunks", 0),
                    "uploaded_at": meta.get("uploaded_at", ""),
                }

        return list(seen.values())

    @property
    def collection_count(self) -> int:
        """Total number of chunks in the collection."""
        return self._collection.count()


@lru_cache()
def get_chroma_client() -> ChromaDBClient:
    """Return the cached (singleton) ChromaDBClient instance."""
    return ChromaDBClient()
