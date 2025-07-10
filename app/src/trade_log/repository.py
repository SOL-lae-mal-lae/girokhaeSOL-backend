from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.logging import log_info, log_debug, log_error
from .model import TradeLog
from .schemas import TradeLogCreate, TradeLogUpdate

class TradeLogRepository:
    def __init__(self, db: Session):
        self.db = db
    
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