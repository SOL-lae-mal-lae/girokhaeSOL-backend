from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    is_public: Optional[bool]

class PostResponse(PostBase):
    id: int
    post_type: bool
    user_id: str
    created_at: datetime  # Changed to datetime for proper validation

    class Config:
        from_attributes = True  # Enables ORM compatibility

class BaseResponse(BaseModel):
    message: str
    data: Optional[dict]

    class Config:
        from_attributes = True  # Ensures Pydantic can handle ORM models
