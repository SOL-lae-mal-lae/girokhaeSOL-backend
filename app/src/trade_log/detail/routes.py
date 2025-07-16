from fastapi import APIRouter, Request, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database.core import get_db
from .schemas import TradeLogCreateSchema, TradeLogResponseSchema
from .services import create_trade_log_service

router = APIRouter()

@router.post("/detail", status_code=status.HTTP_201_CREATED)
def create_trade_log_api(
    body: TradeLogCreateSchema,
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = getattr(request.state, "user", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="인증 필요")
    result = create_trade_log_service(user_id, body, db)
    return {
        "message": "매매일지 생성 완료",
        "data": result
    }
