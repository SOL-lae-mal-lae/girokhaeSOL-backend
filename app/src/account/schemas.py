from pydantic import BaseModel
from typing import List, Optional

class AccountBase(BaseModel):
    account_number: str

class AccountCreate(AccountBase):
    user_id: Optional[str] = None  # Optional로 변경 (query param에서 설정)

class AccountUpdate(BaseModel):
    account_number: Optional[str] = None

class AccountResponse(AccountBase):
    id: int
    user_id: str  # VARCHAR(50)로 변경
    
    class Config:
        from_attributes = True

class AccountListResponse(BaseModel):
    message: str
    data: List[dict]

class ErrorResponse(BaseModel):
    message: str = "오류가 발생했습니다."

