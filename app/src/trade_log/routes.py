from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.database.core import SessionLocal
from .services import TradeLogService
from .schemas import TradeLogMonthlyResponse, ErrorResponse
from app.logging import log_info

router = APIRouter()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@router.get("",
  response_model=TradeLogMonthlyResponse,
  responses={
    200: {"model": TradeLogMonthlyResponse, "description": "매매일지 일자 조회 성공"},
    400: {"model": ErrorResponse, "description": "잘못된 요청"},
    404: {"description": "사용자를 찾을 수 없음"},
    422: {"description": "유효성 검증 실패"}
  }
)
def get_monthly_trade_logs_by_user_id(
  userId: str,
  yearMonth: str,
  db: Session = Depends(get_db)
):
  """사용자의 매매일지 일자 조회"""
  try:
    user_id = userId.strip()
    year_month = yearMonth.strip()
    service = TradeLogService(db)
    result = service.get_monthly_trade_logs_by_user_id(user_id, year_month)

    return {"message": "매매일지 월간 조회 완료", "data" : result}
  except HTTPException:
    raise
  except Exception:
    raise HTTPException(status_code=400, detail="오류가 발생했습니다.")