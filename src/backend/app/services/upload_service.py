from uuid import uuid4
from fastapi import UploadFile

from app.config import get_settings
from app.embeddings.pipeline import embeddings_pipeline
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.splitter import split_text
from app.utils.errors import AppError
from app.utils.files import save_upload


class UploadService:
    async def handle_upload(self, file: UploadFile) -> str:
        settings = get_settings()
        data = await file.read()
        size_mb = len(data) / (1024 * 1024)
        if size_mb > settings.max_upload_mb:
            raise AppError(f"File too large (>{settings.max_upload_mb}MB)", status_code=413)

        document_id = str(uuid4())
        filename = f"{document_id}_{file.filename or 'document.pdf'}"
        path = save_upload(filename, data)

        text = load_pdf(str(path))
        chunks = split_text(text)
        embeddings_pipeline.upsert(document_id, chunks)
        return document_id


upload_service = UploadService()
