from fastapi import APIRouter, Request, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session
from app.database.core import get_db
from .schemas import RecentLogsResponseSchema, TradeLogByIdResponseSchema, TradeLogCreateSchema, TradeLogRequestByIdSchema, TradeLogResponseSchema
from .services import create_trade_log_service, get_recent_logs, get_trade_log_service_by_date, get_trade_log_service_by_id

router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_trade_log_api(
    body: TradeLogCreateSchema,
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = getattr(request.state, "user", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="인증 필요")
    try:
      create_trade_log_service(user_id, body, db)

      return {
          "message": "success",
          "data": None,
      }
    except Exception as e:
      raise HTTPException(status_code=500, detail="매매일지 저장에 실패하였습니다.")

@router.get('/detail',
             response_model=TradeLogResponseSchema)
def get_trade_log(date: str, request: Request, db: Session = Depends(get_db)):

    try:
        user_id = getattr(request.state, "user", None)
        if not user_id:
            raise HTTPException(status_code=401, detail="인증 필요")
        
        date = date.strip()

        result = get_trade_log_service_by_date(date, user_id, db)
        return {
            "message": 'success',
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail="매매일지 조회에 실패하였습니다.")

    return

@router.get('/recentlogs',
            response_model=RecentLogsResponseSchema)
def get_recent_trade_log(request: Request, db: Session = Depends(get_db)):
    try:
        user_id = getattr(request.state, "user", None)
        if not user_id:
            raise HTTPException(status_code=401, detail="인증 필요")
        
        result = get_recent_logs(user_id, db)
        return {
            "message": 'success',
            "data": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="날짜 조회에 실패하였습니다.")
    return

@router.post('/byid')
def get_trade_log_by_id( body: TradeLogRequestByIdSchema,request: Request,  db: Session = Depends(get_db)):
    try:
        isUser = getattr(request.state, "user", None)
        if not isUser:
            raise HTTPException(status_code=401, detail="인증 필요")
        if not body.trade_log_id or not body.user_id:
            raise HTTPException(status_code=400, detail="trade_log_id, user_id가 필요합니다.")
        result = get_trade_log_service_by_id(body.user_id, body.trade_log_id, db)

        return {
            "message": 'success',
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="매매일지 조회에 실패하였습니다.")
    return
    