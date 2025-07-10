from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TradeLog(Base):
  __tablename__="trade_logs"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  user_id = Column(String(50), nullable=False)
  date = Column(DateTime, nullable=True)
  investment_type = Column(String(10), nullable=True)
  rationale = Column(Text, nullable=True)
  evaluation = Column(Text, nullable=True)
