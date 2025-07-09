from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database.core import Base

class TradeDetail(Base):
    __tablename__ = "trade_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_log_id = Column(Integer, ForeignKey("trade_logs.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))
    stock_name = Column(String(25))
    stock_code = Column(String(6))
    avg_buy_price = Column(Float)
    buy_quantity = Column(Integer)
    avg_sell_price = Column(Float)
    sell_quantity = Column(Integer)
    profit_amount = Column(Integer)

