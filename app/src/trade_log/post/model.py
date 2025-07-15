from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.core import Base

class TradeSummary(Base):
    __tablename__ = 'trade_summaries'
    trade_log_id = Column(Integer, ForeignKey('trade_logs.id'), primary_key=True)
    total_buy_amount = Column(Integer)
    total_sell_amount = Column(Integer)
    settlement_amount = Column(Integer)
    profit_rate = Column(Float)
    total_cmsn_tax = Column(Float)

class Chart(Base):
    __tablename__ = 'charts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_log_id = Column(Integer, ForeignKey('trade_logs.id'), nullable=False)
    stock_code = Column(String(6))
    start_date = Column(Date)
    end_date = Column(Date)
    sequence = Column(Integer)

class NewsLink(Base):
    __tablename__ = 'news_links'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_log_id = Column(Integer, ForeignKey('trade_logs.id'), nullable=False)
    url = Column(String(500), nullable=False)

class TradeLogAccount(Base):
    __tablename__ = 'trade_log_accounts'
    trade_log_id = Column(Integer, ForeignKey('trade_logs.id'), primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)
