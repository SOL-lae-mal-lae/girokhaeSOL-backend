from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PostCreateRequest(BaseModel):
    post_type: bool
    title: str
    content: str
    trade_log_id: Optional[int] = None
    is_public: bool = True

class PostUpdateRequest(BaseModel):
    post_type: Optional[bool] = None
    title: Optional[str] = None
    content: Optional[str] = None
    trade_log_id: Optional[int] = None
    is_public: Optional[bool] = None

class PostResponse(BaseModel):
    id: int
    post_type: bool
    user_id: str
    nickname: str
    created_at: datetime
    title: str
    content: str
    trade_log_id: Optional[int]
    is_public: bool

class PostListResponse(BaseModel):
    id: int
    post_type: bool
    user_id: str
    nickname: str
    created_at: datetime
    title: str
    content: str
    comment_count: int

class PostCreateResponse(BaseModel):
    message: str
    data: dict

class PostDetailResponse(BaseModel):
    message: str
    data: PostResponse

class PostListResponseWrapper(BaseModel):
    message: str
    data: List[PostListResponse]

class PostDeleteResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    detail: str
