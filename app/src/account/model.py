from sqlalchemy import Column, Integer, String
from app.database.core import Base
from app.src.common_models.users.model import User


class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), nullable=False)  # Foreign Key 제약조건 임시 제거
    account_number = Column(String(20), nullable=False)
    
   