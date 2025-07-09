from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.core import SessionLocal
from .services import get_stock_rank

router = APIRouter(prefix="/data_lab", tags=["data_lab"])

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/rank")
def read_rank(db: Session = Depends(get_db)):
    rank_data = get_stock_rank(db)
    return {
        "message": "주문 수 기준 랭킹 조회 성공!",
        "data": rank_data
    }
