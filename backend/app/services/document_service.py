"""
Document Service
----------------
Handles everything related to uploaded files:
  - Validation (type, size)
  - Text extraction (PDF, DOCX, TXT)
  - Intelligent chunking via LangChain's RecursiveCharacterTextSplitter
  - Saving files to disk
"""

import os
import uuid
import logging
import aiofiles
from pathlib import Path
from typing import List, Tuple

from fastapi import UploadFile, HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class DocumentService:
    """
    Handles file I/O, text extraction, and chunking for uploaded documents.
    """

    def __init__(self):
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        # RecursiveCharacterTextSplitter tries to split on paragraphs → sentences
        # → words before falling back to characters, preserving semantic meaning.
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    # ── Validation ────────────────────────────────────────────────────────────

    def validate_file(self, file: UploadFile) -> None:
        """
        Raise HTTPException if the file fails validation checks.

        Checks:
          - Extension is in the allowed list
          - File size is within the configured limit
        """
        if not file.filename:
            raise HTTPException(status_code=400, detail="File has no name.")

        ext = Path(file.filename).suffix.lstrip(".").lower()
        if ext not in settings.allowed_extensions_list:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"File type '.{ext}' is not allowed. "
                    f"Allowed types: {settings.allowed_extensions_list}"
                ),
            )

    async def validate_file_size(self, file: UploadFile) -> bytes:
        """
        Read the file content and validate its size.

        Returns:
            The raw file bytes (so we don't read twice).

        Raises:
            HTTPException: If the file exceeds the size limit.
        """
        content = await file.read()
        if len(content) > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=413,
                detail=(
                    f"File size {len(content) / 1024 / 1024:.1f} MB exceeds "
                    f"the {settings.max_file_size_mb} MB limit."
                ),
            )
        return content

    # ── Persistence ───────────────────────────────────────────────────────────

    async def save_file(self, content: bytes, filename: str) -> Tuple[str, Path]:
        """
        Save raw bytes to the uploads directory with a unique document ID prefix.

        Returns:
            (document_id, saved_path)
        """
        document_id = str(uuid.uuid4())
        safe_name = Path(filename).name  # strip any path traversal attempts
        save_path = self.upload_dir / f"{document_id}_{safe_name}"

        async with aiofiles.open(save_path, "wb") as f:
            await f.write(content)

        logger.info(f"Saved file: {save_path}")
        return document_id, save_path

    # ── Text extraction ───────────────────────────────────────────────────────

    def extract_text(self, file_path: Path, file_type: str) -> str:
        """
        Extract plain text from a file based on its type.

        Args:
            file_path: Path to the saved file.
            file_type: 'pdf', 'docx', or 'txt'.

        Returns:
            Extracted text as a single string.
        """
        if file_type == "pdf":
            return self._extract_pdf(file_path)
        elif file_type == "docx":
            return self._extract_docx(file_path)
        elif file_type == "txt":
            return self._extract_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    def _extract_pdf(self, file_path: Path) -> str:
        """Extract text from a PDF using pypdf."""
        try:
            from pypdf import PdfReader

            reader = PdfReader(str(file_path))
            pages = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
            return "\n\n".join(pages)
        except Exception as exc:
            logger.error(f"PDF extraction failed for {file_path}: {exc}")
            raise RuntimeError(f"Could not extract text from PDF: {exc}") from exc

    def _extract_docx(self, file_path: Path) -> str:
        """Extract text from a DOCX file using python-docx."""
        try:
            from docx import Document

            doc = Document(str(file_path))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n\n".join(paragraphs)
        except Exception as exc:
            logger.error(f"DOCX extraction failed for {file_path}: {exc}")
            raise RuntimeError(f"Could not extract text from DOCX: {exc}") from exc

    def _extract_txt(self, file_path: Path) -> str:
        """Read a plain text file, trying UTF-8 then latin-1 as fallback."""
        try:
            return file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return file_path.read_text(encoding="latin-1")

    # ── Chunking ──────────────────────────────────────────────────────────────

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks using RecursiveCharacterTextSplitter.

        Args:
            text: The full document text.

        Returns:
            List of text chunks.
        """
        if not text.strip():
            raise ValueError("Cannot chunk empty text.")

        chunks = self.text_splitter.split_text(text)
        logger.info(f"Split document into {len(chunks)} chunks.")
        return chunks

    # ── Cleanup ───────────────────────────────────────────────────────────────

    def delete_file(self, document_id: str) -> None:
        """Remove all files in the upload directory that start with document_id."""
        for f in self.upload_dir.glob(f"{document_id}_*"):
            f.unlink()
            logger.info(f"Deleted file: {f}")


def get_document_service() -> DocumentService:
    """FastAPI dependency that returns a DocumentService instance."""
    return DocumentService()
