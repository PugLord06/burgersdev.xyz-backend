from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    query: Optional[str] = None
    message: Optional[str] = None

    def get_text(self) -> str:
        return (self.query or self.message or "").strip()

class ChatResponse(BaseModel):
    response: str
