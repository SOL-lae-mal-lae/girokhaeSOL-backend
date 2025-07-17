from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.src.common_models.users.model import User
from .repository import TradeLogDetailRepository
from .model import TradeLog, TradeSummary, TradeDetail, Chart, NewsLink, TradeLogSentiment, Sentiment
from .schemas import TradeLogResponseSchema, TradeSummarySchema, TradeDetailSchema, ChartSchema, NewsLinkSchema
from ..stock_search.model import Stock
from ...logging import log_info


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

def get_trade_log_service_by_date(date: str, user_id: str, db: Session):
    """
    특정 날짜의 매매일지 상세 정보를 조회합니다.
    """
    try:
        # 1. 해당 날짜와 사용자의 trade_log 조회
        trade_log = db.query(TradeLog).filter(
            TradeLog.date == date,
            TradeLog.user_id == user_id
        ).first()
        
        if not trade_log:
            raise HTTPException(status_code=404, detail="해당 날짜의 매매일지를 찾을 수 없습니다.")
        
        trade_log_id = trade_log.id
        
        # 2. trade_details 조회
        trade_details = db.query(TradeDetail).filter(
            TradeDetail.trade_log_id == trade_log_id
        ).all()
        
        # 3. trade_summaries 조회
        trade_summary = db.query(TradeSummary).filter(
            TradeSummary.trade_log_id == trade_log_id
        ).first()
        
        # 4. charts 조회 (sequence 순으로 정렬) - stocks 테이블과 LEFT JOIN
        charts = db.query(Chart, Stock.stock_name).outerjoin(
            Stock, Chart.stock_code == Stock.stock_code
        ).filter(
            Chart.trade_log_id == trade_log_id
        ).order_by(Chart.sequence.asc()).all()
        
        # 5. sentiments 조회
        sentiments = db.query(Sentiment.name).join(
            TradeLogSentiment, Sentiment.id == TradeLogSentiment.sentiment_id
        ).filter(
            TradeLogSentiment.trade_log_id == trade_log_id
        ).all()
        
        # 결과 데이터 구성
        result = {
            "date": trade_log.date,
            "summaries": {
                "total_buy_amount": trade_summary.total_buy_amount if trade_summary else 0,
                "total_sell_amount": trade_summary.total_sell_amount if trade_summary else 0,
                "total_cmsn_tax": trade_summary.total_cmsn_tax if trade_summary else 0.0,
                "settlement_amount": trade_summary.settlement_amount if trade_summary else 0,
                "profit_rate": trade_summary.profit_rate if trade_summary else 0.0
            },
            "trade_details": [
                {
                    "account_id": detail.account_id,
                    "stock_name": detail.stock_name,
                    "stock_code": detail.stock_code,
                    "avg_buy_price": detail.avg_buy_price,
                    "avg_sell_price": detail.avg_sell_price,
                    "buy_quantity": detail.buy_quantity,
                    "sell_quantity": detail.sell_quantity,
                    "cmsn_alm_tax": detail.cmsn_alm_tax,
                    "profit_amount": detail.profit_amount,
                    "profit_rate": detail.profit_rate
                }
                for detail in trade_details
            ],
            "charts": [
                {
                    "stock_name": chart_tuple[1] if chart_tuple[1] else "",  # Stock.stock_name (LEFT JOIN이므로 None일 수 있음)
                    "stock_code": chart_tuple[0].stock_code,
                    "start_date": chart_tuple[0].start_date,
                    "end_date": chart_tuple[0].end_date,
                    "sequence": chart_tuple[0].sequence
                }
                for chart_tuple in charts
            ],
            "investment_type": trade_log.investment_type,
            "sentiments": [sentiment.name for sentiment in sentiments],
            "rationale": trade_log.rationale,
            "evaluation": trade_log.evaluation,
            "news_links": []  # news_links는 현재 구현되지 않았으므로 빈 배열
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"매매일지 조회 중 오류가 발생했습니다: {str(e)}")