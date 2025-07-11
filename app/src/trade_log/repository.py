from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.logging import log_info, log_debug, log_error
from .model import TradeLog, TradeLogSentiment, Sentiment, TradeDetail


class TradeLogRepository:
    def __init__(self, db: Session):
        self.db = db
    # 월에 작성한 매매일지 개수
    def get_monthly_trade_logs_by_user_id(self, user_id: str, year_month: str) -> List[TradeLog]:
        try:
            log_info("Repository : get_monthly_trade_logs_by_user_id 시작")
            log_debug(f"user_id = {user_id}, year_month = {year_month}")
            
            # 쿼리 실행
            query = self.db.query(TradeLog).filter(
                TradeLog.user_id == user_id,
                func.date_format(TradeLog.date, '%Y%m') == year_month
            )
            
            result = query.all()
            log_debug(f"쿼리 결과: {len(result)}개의 레코드")
            
            return result
        except Exception as e:
            log_error(f"Repository 오류: {str(e)}")
            log_error(f"Exception 타입: {type(e)}")
            import traceback
            log_error(f"Traceback: {traceback.format_exc()}")
            raise

    # 월별 투자 성과 지표
    def get_monthly_trade_stat_by_user_id(self, user_id: str, year_month: str) -> dict[str, float]:
        try:
            log_info("Repository : get_monthly_trade_stat_by_user_id 시작")
            log_debug(f"user_id = {user_id}, year_month = {year_month}")
            
            # SQLAlchemy ORM을 사용한 쿼리
            result = self.db.query(
                func.sum(TradeDetail.avg_buy_price * TradeDetail.buy_quantity).label('total_buy_amount'),
                func.sum(TradeDetail.avg_sell_price * TradeDetail.sell_quantity).label('total_sell_amount'),
                func.sum(TradeDetail.cmsn_alm_tax).label('total_commission_and_tax'),
                ((func.sum(TradeDetail.avg_sell_price * TradeDetail.sell_quantity) - 
                  func.sum(TradeDetail.avg_buy_price * TradeDetail.buy_quantity) - 
                  func.sum(TradeDetail.cmsn_alm_tax)) / 
                 func.sum(TradeDetail.avg_buy_price * TradeDetail.buy_quantity) * 100).label('profit_rate')
            ).join(TradeLog).filter(
                TradeLog.user_id == user_id,
                func.date_format(TradeLog.date, '%Y%m') == year_month
            ).first()
            log_debug(f'{result}')
            if result:
                return {
                    'total_buy_amount': float(result.total_buy_amount or 0),
                    'total_sell_amount': float(result.total_sell_amount or 0),
                    'total_commission_and_tax': float(result.total_commission_and_tax or 0),
                    'profit_rate': float(result.profit_rate or 0)
                }
            else:
                return {
                    'total_buy_amount': 0.0,
                    'total_sell_amount': 0.0,
                    'total_commission_and_tax': 0.0,
                    'profit_rate': 0.0
                }
                
        except Exception as e:
            log_error(f"Repository 오류: {str(e)}")
            log_error(f"Exception 타입: {type(e)}")
            import traceback
            log_error(f"Traceback: {traceback.format_exc()}")
            raise

    # 가장 많이 선택한 감정 유형
    def get_monthly_trade_log_sentiments_by_user_id(self, user_id: str, year_month: str) -> List[tuple]:
        try:
            log_info("Repository : get_monthly_trade_log_sentiments_by_user_id 시작")
            log_debug(f"user_id = {user_id}, year_month = {year_month}")

            # 감정별 카운트를 함께 반환
            result = self.db.query(
                Sentiment.name,
                func.count().label('count')
            ).join(TradeLogSentiment).join(TradeLog).filter(
                TradeLog.user_id == user_id,
                func.date_format(TradeLog.date, '%Y%m') == year_month
            ).group_by(Sentiment.name).order_by(func.count().desc()).all()
            
            log_debug(f"쿼리 결과: {len(result)}개의 레코드")
            
            return result
        except Exception as e:
            log_error(f"Repository 오류: {str(e)}")
            log_error(f"Exception 타입: {type(e)}")
            import traceback
            log_error(f"Traceback: {traceback.format_exc()}")
            raise
    # 가장 많이 투자한 종목
    def get_monthly_top_invested_stocks_by_user_id(self, user_id: str, year_month: str) -> List[TradeDetail]:
        try:
            log_info("Repository : get_monthly_top_invested_stocks_by_user_id 시작")
            log_debug(f"user_id = {user_id}, year_month = {year_month}")
            
            query = self.db.query(TradeDetail).join(TradeLog).filter(
                TradeLog.user_id == user_id,
                func.date_format(TradeLog.date, '%Y%m') == year_month
            ).group_by(TradeDetail.stock_name).order_by(func.count().desc()).limit(3)

            result = query.all()
            log_debug(f"쿼리 결과: {len(result)}개의 레코드")
            
            return result
        except Exception as e:
            log_error(f"Repository 오류: {str(e)}")
            log_error(f"Exception 타입: {type(e)}")
            import traceback