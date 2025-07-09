# My Page Schemas
# 마이페이지 관련 API 요청/응답을 위한 Pydantic 스키마를 정의합니다.

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserProfileBase(BaseModel):
    """사용자 프로필 기본 스키마"""
    full_name: Optional[str] = None
    bio: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[datetime] = None


class UserProfileUpdate(UserProfileBase):
    """사용자 프로필 업데이트 요청 스키마"""
    pass


class UserProfileResponse(UserProfileBase):
    """사용자 프로필 응답 스키마"""
    id: int
    user_id: int
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserSettingsBase(BaseModel):
    """사용자 설정 기본 스키마"""
    notifications_enabled: bool = True
    email_notifications: bool = True
    theme: str = "light"
    language: str = "ko"


class UserSettingsUpdate(UserSettingsBase):
    """사용자 설정 업데이트 요청 스키마"""
    pass


class UserSettingsResponse(UserSettingsBase):
    """사용자 설정 응답 스키마"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PasswordChangeRequest(BaseModel):
    """비밀번호 변경 요청 스키마"""
    current_password: str
    new_password: str
    confirm_password: str


class UserActivityResponse(BaseModel):
    """사용자 활동 로그 응답 스키마"""
    id: int
    user_id: int
    activity_type: str
    description: str
    timestamp: datetime

    class Config:
        from_attributes = True


class MyPageDashboardResponse(BaseModel):
    """마이페이지 대시보드 응답 스키마"""
    profile: UserProfileResponse
    settings: UserSettingsResponse
    recent_activities: List[UserActivityResponse]
    account_summary: dict
