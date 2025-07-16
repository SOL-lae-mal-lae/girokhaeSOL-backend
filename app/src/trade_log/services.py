from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.src.common_models.users.model import User
from .repository import TradeLogDetailRepository
from .model import TradeLog, TradeSummary, TradeDetail, Chart, NewsLink, TradeLogSentiment, Sentiment
from .schemas import TradeLogResponseSchema, TradeSummarySchema, TradeDetailSchema, ChartSchema, NewsLinkSchema

def create_trade_log_service(user_id: str, body, db: Session):
    # user_id 존재 확인
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="존재하지 않는 user_id입니다.")

    repo = TradeLogDetailRepository(db)
    trade_log_id = repo.insert_trade_log(user_id, body)
    repo.insert_trade_summary(trade_log_id, body.summaries)
    repo.insert_trade_details(trade_log_id, body.trade_details)
    repo.insert_charts(trade_log_id, body.charts)
    repo.insert_news_links(trade_log_id, body.news_links)
    repo.insert_sentiments(trade_log_id, body.sentiments)
    db.commit()

    return True