from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.core import get_db
from .service import fetch_trade_details_by_user
from .schemas import TradeDetailResponse
from typing import List

router = APIRouter()

@router.get("/my_page_tradelogs", response_model=List[TradeDetailResponse])
def get_trade_details(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user  # 미들웨어에서 user_id를 파싱
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    results = fetch_trade_details_by_user(db, user_id)
    if not results:
        raise HTTPException(status_code=404, detail="No trade details found for the user")
    return results

