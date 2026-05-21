from datetime import datetime
from pydantic import BaseModel


class Document(BaseModel):
    id: str
    filename: str
    sizeBytes: int
    uploadedAt: datetime
