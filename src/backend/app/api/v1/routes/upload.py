from fastapi import APIRouter, UploadFile, File

from app.services.upload_service import upload_service

router = APIRouter()


@router.post("")
async def upload_document(file: UploadFile = File(...)) -> dict:
    document_id = await upload_service.handle_upload(file)
    return {"documentId": document_id}
