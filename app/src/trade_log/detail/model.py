from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from app.database.core import Base

class TradeLog(Base):
    __tablename__ = "trade_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    date = Column(Date)
    investment_type = Column(String(10))
    rationale = Column(Text)
    evaluation = Column(Text)

class TradeSummary(Base):
    __tablename__ = "trade_summaries"
    trade_log_id = Column(Integer, ForeignKey("trade_logs.id"), primary_key=True)
    total_buy_amount = Column(Integer)
    total_sell_amount = Column(Integer)
    settlement_amount = Column(Integer)
    profit_rate = Column(Float)
    total_cmsn_tax = Column(Float)

class TradeDetail(Base):
    __tablename__ = "trade_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_log_id = Column(Integer, ForeignKey("trade_logs.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    stock_name = Column(String(25))
    stock_code = Column(String(6))
    avg_buy_price = Column(Float)
    buy_quantity = Column(Integer)
    avg_sell_price = Column(Float)
    sell_quantity = Column(Integer)
    cmsn_alm_tax = Column(Float)
    profit_amount = Column(Integer)
    profit_rate = Column(Float)

class Chart(Base):
    __tablename__ = "charts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_log_id = Column(Integer, ForeignKey("trade_logs.id"), nullable=False)
    stock_code = Column(String(6))
    start_date = Column(Date)
    end_date = Column(Date)
    sequence = Column(Integer)

class NewsLink(Base):
    __tablename__ = "news_links"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_log_id = Column(Integer, ForeignKey("trade_logs.id"), nullable=False)
    url = Column(String(500), nullable=False)

class TradeLogAccount(Base):
    __tablename__ = "trade_log_accounts"
    trade_log_id = Column(Integer, ForeignKey("trade_logs.id"), primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), primary_key=True)

class Sentiment(Base):
    __tablename__ = "sentiments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), unique=True, nullable=False)

class TradeLogSentiment(Base):
    __tablename__ = "trade_log_sentiments"
    trade_log_id = Column(Integer, ForeignKey("trade_logs.id"), primary_key=True)
    sentiment_id = Column(Integer, ForeignKey("sentiments.id"), primary_key=True)
