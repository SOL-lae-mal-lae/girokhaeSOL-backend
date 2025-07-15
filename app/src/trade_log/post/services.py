from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.core import get_db
from .repository import (
    insert_trade_log, insert_trade_summary, insert_trade_details,
    insert_charts, insert_news_links, insert_sentiments
)
from app.src.trade_log.model import TradeLog, TradeDetail, TradeLogSentiment, Sentiment
from .model import TradeSummary, Chart, NewsLink, TradeLogAccount

def create_trade_log_service(user_id: str, body, db: Session):
    # 1. trade_logs 등록
    trade_log_id = insert_trade_log(db, user_id, body)
    # 2. trade_summaries 등록
    insert_trade_summary(db, trade_log_id, body.summaries)
    # 3. trade_details 등록
    insert_trade_details(db, trade_log_id, body.trade_details)
    # 4. charts 등록
    insert_charts(db, trade_log_id, body.charts)
    # 5. news_links 등록
    insert_news_links(db, trade_log_id, body.news_links)
    # 6. sentiments 등록
    insert_sentiments(db, trade_log_id, body.sentiments)
    db.commit()
    # 등록된 trade_log 전체 정보 반환
    trade_log = db.query(TradeLog).filter_by(id=trade_log_id).first()
    summary = db.query(TradeSummary).filter_by(trade_log_id=trade_log_id).first()
    details = db.query(TradeDetail).filter_by(trade_log_id=trade_log_id).all()
    charts = db.query(Chart).filter_by(trade_log_id=trade_log_id).all()
    news_links = db.query(NewsLink).filter_by(trade_log_id=trade_log_id).all()
    sentiments = db.query(TradeLogSentiment).filter_by(trade_log_id=trade_log_id).all()
    return {
        "trade_log": trade_log,
        "summary": summary,
        "details": details,
        "charts": charts,
        "news_links": news_links,
        "sentiments": sentiments
    }
