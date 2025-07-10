from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from app.logging import log_debug, log_info, log_error
from .repository import TradeLogRepository
from .model import TradeLog

class TradeLogService:
  def __init__(self, db: Session):
    self.repository = TradeLogRepository(db)

  def get_monthly_trade_logs_by_user_id(self, user_id: str, year_month: str) -> List[TradeLog]:
    try:
      log_info(f"Service 시작: user_id = {user_id}, year_month = {year_month}")

      # Repository 호출
      log_debug("Repository 호출 시작")
      trade_logs = self.repository.get_monthly_trade_logs_by_user_id(user_id, year_month)
      log_debug(f"Repository 결과: {len(trade_logs)}개의 레코드")

      # 날짜 추출
      dates = []
      for trade_log in trade_logs:
        if trade_log.date:
          dates.append(trade_log.date.strftime('%Y-%m-%d'))

      log_info(f"최종 결과: {len(dates)}개의 날짜")

      return {
        "message": '매매일지 일자 조회 완료', 
        "data": {
          "dates": dates
        }
      }
    except Exception as e:
      log_error(f"get_monthly_trade_logs_by_user_id 실패: {str(e)}")
      log_error(f"Exception 타입: {type(e)}")
      import traceback
      log_error(f"Traceback: {traceback.format_exc()}")
      raise HTTPException(status_code=400, detail=f"오류가 발생했습니다: {str(e)}")