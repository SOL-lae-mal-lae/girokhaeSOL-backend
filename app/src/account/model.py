from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(50), primary_key=True, index=True)
    nickname = Column(String(25))
    age = Column(Integer)
    gender = Column(String(10))  # ex: 'male', 'female'

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), nullable=False)  # Foreign Key 제약조건 임시 제거
    account_number = Column(String(20), nullable=False)
    
   