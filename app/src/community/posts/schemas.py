# Community Schemas
# 커뮤니티 관련 API 요청/응답을 위한 Pydantic 스키마를 정의합니다.

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PostBase(BaseModel):
    """게시글 기본 스키마"""
    title: str
    content: str
    category: Optional[str] = None


class PostCreate(PostBase):
    """게시글 생성 요청 스키마"""
    author_id: int


class PostUpdate(BaseModel):
    """게시글 업데이트 요청 스키마"""
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None


class CommentBase(BaseModel):
    """댓글 기본 스키마"""
    content: str


class CommentCreate(CommentBase):
    """댓글 생성 요청 스키마"""
    post_id: int
    author_id: int


class CommentResponse(CommentBase):
    """댓글 응답 스키마"""
    id: int
    post_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostResponse(PostBase):
    """게시글 응답 스키마"""
    id: int
    author_id: int
    view_count: int
    like_count: int
    created_at: datetime
    updated_at: datetime
    comments: List[CommentResponse] = []

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    """게시글 목록 응답 스키마"""
    posts: List[PostResponse]
    total_count: int
