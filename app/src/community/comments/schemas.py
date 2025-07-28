from pydantic import BaseModel
from typing import List
from datetime import datetime

class CommentCreateRequest(BaseModel):
    content: str

class CommentUpdateRequest(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: str
    nickname: str
    content: str
    created_at: datetime

class CommentListResponse(BaseModel):
    id: int
    user_id: str
    nickname: str
    content: str
    created_at: datetime

class CommentCreateResponse(BaseModel):
    message: str
    data: dict

class CommentListResponseWrapper(BaseModel):
    message: str
    data: List[CommentListResponse]

class CommentDeleteResponse(BaseModel):
    message: str

class CommentUpdateResponse(BaseModel):
    message: str
    data: CommentResponse

class ErrorResponse(BaseModel):
    detail: str
