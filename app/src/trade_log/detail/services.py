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

    # 전체 정보 직렬화
    trade_log = db.query(TradeLog).filter_by(id=trade_log_id).first()
    summary = db.query(TradeSummary).filter_by(trade_log_id=trade_log_id).first()
    details = db.query(TradeDetail).filter_by(trade_log_id=trade_log_id).all()
    charts = db.query(Chart).filter_by(trade_log_id=trade_log_id).all()
    news_links = db.query(NewsLink).filter_by(trade_log_id=trade_log_id).all()
    sentiments = db.query(TradeLogSentiment).filter_by(trade_log_id=trade_log_id).all()
    sentiment_names = [
        db.query(Sentiment).filter_by(id=s.sentiment_id).first().name
        for s in sentiments
    ]
    return TradeLogResponseSchema(
        id=trade_log.id,
        user_id=trade_log.user_id,
        date=trade_log.date,
        summary=TradeSummarySchema(**summary.__dict__),
        trade_details=[TradeDetailSchema(**d.__dict__) for d in details],
        charts=[ChartSchema(**c.__dict__) for c in charts],
        investment_type=trade_log.investment_type,
        sentiments=sentiment_names
        rationale=trade_log.rationale,
        evaluation=trade_log.evaluation,
        news_links=[NewsLinkSchema(**n.__dict__) for n in news_links],
    )
