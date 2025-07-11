from sqlalchemy import Column, Integer, String
from app.database.core import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(50), primary_key=True, index=True)
    nickname = Column(String(25))
    age = Column(Integer)
    gender = Column(String(10))  # ex: 'male', 'female'