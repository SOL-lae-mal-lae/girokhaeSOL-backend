from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from app.src.trade_log.model import TradeLog
from app.database.core import Base

class AIAnalysis(Base):
    __tablename__ = "ai_analysis"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_log_id = Column(Integer, ForeignKey("trade_logs.id"), nullable=False)
    result = Column(Text)

class AILink(Base):
    __tablename__ = "ai_links"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ai_analysis_id = Column(Integer, ForeignKey("ai_analysis.id"))
    news_link = Column(Text)
    sequence = Column(Integer)
