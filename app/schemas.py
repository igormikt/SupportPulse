from pydantic import BaseModel, Field, field_validator
from typing import Literal

class TriageRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=2000, description="Текст обращения (5-2000 символов)")
    channel: Literal["email", "form", "chat"] = "email"
    client_id: str = Field(..., min_length=1, max_length=50, description="Уникальный идентификатор клиента")
    
    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Текст обращения не может быть пустым или состоящим только из пробелов")
        return v.strip()
    
    @field_validator("client_id")
    @classmethod
    def client_id_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("client_id не может быть пустым")
        return v.strip()

class TriageResponse(BaseModel):
    category: Literal["billing", "support", "complaint", "other"]
    draft_reply: str = Field(..., min_length=1, max_length=500, description="Черновик ответа (1-500 символов)")
    confidence: Literal["high", "medium", "low"]
    escalate: bool