from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from typing import List
from app.logging import log_info, log_debug, log_error
from app.src.trade_log.model import TradeLog, TradeDetail
from app.src.account.model import User, Account


class TradedStockRepository:
    """거래 종목 DB 조회 - 조인 방식"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_traded_stocks(self, user_id: str) -> List[str]:
        """사용자의 거래 종목 코드 목록 조회 - TradeLog와 조인"""
        try:
            log_info(f"DB 조회 시작 - user_id: {user_id}")
            log_debug(f"TradeLog와 TradeDetail 조인으로 종목 조회")
            
            # TradeLog와 TradeDetail을 조인하여 종목 코드 조회
            stocks = self.db.query(distinct(TradeDetail.stock_code), TradeDetail.stock_name)\
                           .join(TradeLog)\
                           .filter(TradeLog.user_id == user_id)\
                           .order_by(TradeDetail.stock_code)\
                           .all()
            
            log_info(f"✅ DB 조회 성공 - 종목 수: {len(stocks)}개")
            
            if stocks:
                stock_codes = [stock[0] for stock in stocks]  # distinct 결과는 튜플
                log_debug(f"📋 조회된 종목들: {stock_codes}")
                return stock_codes
            else:
                log_info(f"📭 거래 내역 없음 - user_id: {user_id}")
                return []
                
        except Exception as e:
            log_error(f"❌ DB 조회 오류: {type(e).__name__}: {e}")
            import traceback
            log_error(f"Traceback: {traceback.format_exc()}")
            return []
