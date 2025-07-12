from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
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


class TradeDetail(Base):
  __tablename__ = 'trade_details' # 데이터베이스 테이블 이름 지정

  # id 컬럼 정의: 정수형, 기본 키, 자동 증가
  id = Column(Integer, primary_key=True, autoincrement=True)

  # trade_log_id 컬럼 정의: 정수형, NULL 허용 안함, trade_logs 테이블의 id를 참조하는 외래 키
  trade_log_id = Column(Integer, ForeignKey('trade_logs.id'), nullable=False)
  # account_id 컬럼 정의: 정수형, NULL 허용 안함, accounts 테이블의 id를 참조하는 외래 키
  account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)

  # 나머지 컬럼 정의
  stock_name = Column(String(25), nullable=True)
  stock_code = Column(String(6), nullable=True)
  avg_buy_price = Column(Float, nullable=True)
  buy_quantity = Column(Integer, nullable=True)
  avg_sell_price = Column(Float, nullable=True)
  sell_quantity = Column(Integer, nullable=True)
  cmsn_alm_tax = Column(Float, nullable=True)
  profit_amount = Column(Integer, nullable=True)
  profit_rate = Column(Float, nullable=True)


class TradeLogSentiment(Base):
  __tablename__ = 'trade_log_sentiments'

  # 복합 기본 키 정의
  trade_log_id = Column(Integer, ForeignKey('trade_logs.id'), primary_key=True)
  sentiment_id = Column(Integer, ForeignKey('sentiments.id'), primary_key=True)


class Sentiment(Base):
  __tablename__ = 'sentiments' # 데이터베이스 테이블 이름 지정

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(10), nullable=False, unique=True)