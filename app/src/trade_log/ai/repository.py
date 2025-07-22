from sqlalchemy.orm import Session
from .model import AIAnalysis, AILink
from app.src.trade_log.model import TradeLog
from app.src.trade_log.model import TradeDetail
from app.src.trade_log.model import TradeSummary
from app.src.trade_log.model import Sentiment, TradeLogSentiment
from app.src.trade_log.model import NewsLink

class AIRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_trade_log_by_id(self, trade_log_id: int):
        return self.db.query(TradeLog).filter(TradeLog.id == trade_log_id).first()

    def get_trade_details_by_log_id(self, trade_log_id: int):
        return self.db.query(TradeDetail).filter(TradeDetail.trade_log_id == trade_log_id).all()

    def get_trade_summary_by_log_id(self, trade_log_id: int):
        return self.db.query(TradeSummary).filter(TradeSummary.trade_log_id == trade_log_id).first()

    def get_sentiments_by_trade_log_id(self, trade_log_id: int):
        return (
            self.db.query(Sentiment)
            .join(TradeLogSentiment, Sentiment.id == TradeLogSentiment.sentiment_id)
            .filter(TradeLogSentiment.trade_log_id == trade_log_id)
            .all()
        )

    def get_news_links_by_trade_log_id(self, trade_log_id: int):
        return self.db.query(NewsLink).filter(NewsLink.trade_log_id == trade_log_id).all()

    def get_ai_analysis_by_log_id(self, trade_log_id: int):
        return self.db.query(AIAnalysis).filter(AIAnalysis.trade_log_id == trade_log_id).first()

    def save_ai_analysis(self, trade_log_id: int, result: str):
        ai_analysis = AIAnalysis(trade_log_id=trade_log_id, result=result)
        self.db.add(ai_analysis)
        self.db.flush()
        return ai_analysis.id

    def get_ai_links_by_analysis_id(self, ai_analysis_id: int):
        return self.db.query(AILink).filter(AILink.ai_analysis_id == ai_analysis_id).all()

    def save_ai_links(self, ai_analysis_id: int, links: list[dict]):
        for link in links:
            ai_link = AILink(
                ai_analysis_id=ai_analysis_id,
                news_link=link["news_link"],
                sequence=link["sequence"]
            )
            self.db.add(ai_link)
