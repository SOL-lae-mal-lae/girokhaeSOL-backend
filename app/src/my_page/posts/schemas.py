from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    is_public: Optional[bool]

class PostResponse(PostBase):
    id: int
    post_type: bool
    user_id: str
    created_at: str

    class Config:
        orm_mode = True

class BaseResponse(BaseModel):
    message: str
    data: Optional[dict]

    class Config:
        orm_mode = True
