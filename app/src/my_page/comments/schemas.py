from pydantic import BaseModel
from typing import Optional

class CommentBase(BaseModel):
    content: str

class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: str
    created_at: str

    class Config:
        orm_mode = True
