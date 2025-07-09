# Auth Schemas
# 인증 관련 API 요청/응답을 위한 Pydantic 스키마를 정의합니다.

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """사용자 기본 스키마"""
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """사용자 생성 요청 스키마"""
    password: str


class UserLogin(BaseModel):
    """로그인 요청 스키마"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """사용자 업데이트 요청 스키마"""
    username: Optional[str] = None
    full_name: Optional[str] = None


class UserResponse(UserBase):
    """사용자 응답 스키마"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """토큰 응답 스키마"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """토큰 데이터 스키마"""
    email: Optional[str] = None
