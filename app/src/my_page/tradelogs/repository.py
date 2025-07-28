from sqlalchemy.orm import Session
from app.src.trade_log.model import TradeLog, TradeDetail

def get_trade_details_by_date(db: Session, date: str, user_id: str):
    # date와 user_id에 해당하는 trade_logs와 trade_details를 join하여 buy_quantity, sell_quantity 반환
    return db.query(
        TradeLog.id.label('trade_log_id'),
        TradeLog.date,
        TradeDetail.buy_quantity,
        TradeDetail.sell_quantity
    ).join(TradeDetail, TradeLog.id == TradeDetail.trade_log_id) \
     .filter(TradeLog.date == date, TradeLog.user_id == user_id) \
     .all()

def get_trade_details_by_user(db: Session, user_id: str):
    # user_id에 해당하는 모든 trade_logs와 trade_details를 join하여 buy_quantity, sell_quantity 반환
    return db.query(
        TradeLog.id.label('trade_log_id'),
        TradeLog.date,
        TradeDetail.buy_quantity,
        TradeDetail.sell_quantity
    ).join(TradeDetail, TradeLog.id == TradeDetail.trade_log_id) \
     .filter(TradeLog.user_id == user_id) \
     .all()
