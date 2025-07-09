# Account Schemas
# API 요청/응답을 위한 Pydantic 스키마를 정의합니다.

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AccountBase(BaseModel):
    """계좌 기본 스키마"""
    account_number: str
    account_name: str
    bank_name: str
    balance: float


class AccountCreate(AccountBase):
    """계좌 생성 요청 스키마"""
    user_id: int


class AccountUpdate(BaseModel):
    """계좌 업데이트 요청 스키마"""
    account_name: Optional[str] = None
    balance: Optional[float] = None


class AccountResponse(AccountBase):
    """계좌 응답 스키마"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AccountListResponse(BaseModel):
    """계좌 목록 응답 스키마"""
    accounts: list[AccountResponse]
    total_count: int
