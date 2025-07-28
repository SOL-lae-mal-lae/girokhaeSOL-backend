from pydantic import BaseModel, Field
from typing import Optional

# User 스키마
class UserBase(BaseModel):
    id: str
    nickname: str
    age: Optional[int]
    gender: Optional[str]
    email: Optional[str]
    posts_count: int
    comments_count: int
    profile_image: Optional[str]

class UserCreate(UserBase):
    id: str = Field(..., description="사용자 ID")

class UserResponse(UserBase):
    id: str = Field(..., description="사용자 ID")

    class Config:
        orm_mode = True

# 공통 응답 스키마
class BaseResponse(BaseModel):
    message: str = Field(..., description="응답 메시지")
    data: Optional[dict] = Field(None, description="응답 데이터")
