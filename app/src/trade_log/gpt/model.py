from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class GPTAnalysis(Base):
    """GPT 거래 로그 분석 결과 모델"""
    __tablename__ = "gpt_analysis"
    
    trade_log_id = Column(Integer, ForeignKey("trade_logs.id"), primary_key=True, nullable=False)
    result = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 설정 (trade_logs 테이블과 연결)
    # trade_log = relationship("TradeLog", back_populates="gpt_analysis")
