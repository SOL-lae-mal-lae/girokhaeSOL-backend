from pydantic import BaseModel
from typing import Optional

# User 스키마 추가
class UserBase(BaseModel):
    nickname: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None  # 'male', 'female'

class UserCreate(UserBase):
    id: str  # VARCHAR(50)

class UserResponse(UserBase):
    id: str
    
    class Config:
        from_attributes = True
