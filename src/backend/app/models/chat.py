from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class ChatMessage(BaseModel):
    id: str
    role: Literal["user", "assistant", "system"]
    content: str
    createdAt: datetime
