from sqlalchemy import Column, String
from app.database.core import Base

class Stock(Base):
    __tablename__ = "stocks"
    stock_code = Column(String(6), primary_key=True, index=True, comment="종목코드")
    stock_name = Column(String(50), nullable=False, comment="종목명")
