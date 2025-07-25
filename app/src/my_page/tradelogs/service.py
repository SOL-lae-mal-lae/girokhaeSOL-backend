from sqlalchemy.orm import Session
from .repository import get_trade_details_by_date, get_trade_details_by_user
from .schemas import TradeDetailResponse

def fetch_trade_details_by_date(db: Session, date: str, user_id: str):
    results = get_trade_details_by_date(db, date, user_id)
    return [
        TradeDetailResponse(
            trade_log_id=row.trade_log_id,
            date=str(row.date),
            buy_quantity=row.buy_quantity,
            sell_quantity=row.sell_quantity
        ) for row in results
    ]

def fetch_trade_details_by_user(db: Session, user_id: str):
    results = get_trade_details_by_user(db, user_id)
    return [
        TradeDetailResponse(
            trade_log_id=row.trade_log_id,
            date=str(row.date),
            buy_quantity=row.buy_quantity,
            sell_quantity=row.sell_quantity
        ) for row in results
    ]
