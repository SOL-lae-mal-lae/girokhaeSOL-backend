from sqlalchemy import Column, Integer, String
from app.database.core import Base

class User(Base):
    """
    사용자 모델
    """
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, index=True, comment="사용자 ID")
    nickname = Column(String(25), nullable=True, comment="사용자 닉네임")
    age = Column(Integer, nullable=True, comment="사용자 나이")
    gender = Column(String(10), nullable=True, comment="사용자 성별 (male, female)")

