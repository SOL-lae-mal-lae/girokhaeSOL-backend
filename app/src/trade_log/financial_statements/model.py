from sqlalchemy import Column, Integer, String, Float
from app.database.core import Base

class FinancialStatement(Base):
    """
    국내주식 재무제표 모델 (키움 주식기본정보 기반)
    """
    __tablename__ = "financial_statements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    stock_code = Column(String(6), nullable=False, index=True)
    mac = Column(Integer, nullable=True)
    per = Column(Float, nullable=True)
    eps = Column(Float, nullable=True)
    pbr = Column(Float, nullable=True)
    roe = Column(Float, nullable=True)
    sale_amt = Column(Integer, nullable=True)
    bus_pro = Column(Integer, nullable=True)
    cup_nga = Column(Integer, nullable=True)
    yyyymm = Column(String(6), nullable=False, index=True, comment="기준 년월 (예: 202406)")
    
   