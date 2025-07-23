from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    content: str

class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: str
    created_at: datetime  # Changed to datetime for proper validation

    class Config:
        orm_mode = True  # Ensures Pydantic can handle ORM models
        from_attributes = True
