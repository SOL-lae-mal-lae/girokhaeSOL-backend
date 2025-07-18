from sqlalchemy import Column, Integer, String, Boolean
from app.database.core import Base
from app.src.common_models.users.model import User  # 기존 User 모델 import

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), nullable=False)  # Foreign Key 제약조건 임시 제거
    account_number = Column(String(20), nullable=False)
    app_key = Column(String(255), nullable=False)  # 외부 API 인증을 위한 app_key
    secret_key = Column(String(255), nullable=False)  # 외부 API 인증을 위한 secret_key
    is_primary = Column(Boolean, default=False, nullable=False)  # 대표계좌 여부
    
   