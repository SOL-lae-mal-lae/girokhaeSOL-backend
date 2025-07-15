from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.core import get_db
from .schemas import TradeLogCreateSchema
from .services import create_trade_log_service

router = APIRouter()

@router.post("/detail")
def create_trade_log_api(
    body: TradeLogCreateSchema,
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = "user_2zceSsp2uVsMkLuh8AftIRulD4F"
    #user_id = getattr(request.state, "user", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="인증 필요")
    result = create_trade_log_service(user_id, body, db)
    return {"message": "매매일지 등록 성공", "data": result}
