from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.core import SessionLocal
from .schemas import StockSearchRequest, StockSearchResponse, ErrorResponse
from .service import StockSearchService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/search",
    response_model=StockSearchResponse,
    responses={
        200: {"model": StockSearchResponse, "description": "종목 검색 결과 반환 완료"},
        400: {"model": ErrorResponse, "description": "오류가 발생했습니다."}
    }
)
def search_stocks(
    request: StockSearchRequest,
    db: Session = Depends(get_db)
):
    try:
        service = StockSearchService(db)
        result = service.search_stocks(request.stock_name)
        return {"message": "종목 검색 결과 반환 완료", "data": result}
    except Exception:
        raise HTTPException(status_code=400, detail="오류가 발생했습니다.")
