from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from .services import FinancialStatementService
from .schemas import FinancialStatementResponse, ErrorResponse
from app.database.core import get_db
from app.logging import log_info, log_error

router = APIRouter()

@router.get(
    "",
    response_model=FinancialStatementResponse,
    summary="종목코드로 재무제표 조회",
    description="종목코드로 해당 종목의 재무제표를 조회합니다",
    responses={
        200: {"description": "재무제표 조회 성공"},
        400: {"model": ErrorResponse, "description": "잘못된 종목코드"},
        404: {"model": ErrorResponse, "description": "재무제표를 찾을 수 없음"},
        500: {"model": ErrorResponse, "description": "서버 내부 오류"}
    }
)
async def get_statement_by_stock_code(
    stock_code: str = Query(..., min_length=6, max_length=6, description="종목코드 (6자리, 예: 005930)"),
    db: Session = Depends(get_db)
):
    """종목코드로 재무제표를 조회합니다"""
    log_info(f"종목코드 재무제표 조회 요청: 종목코드={stock_code}")
    
    service = FinancialStatementService(db)
    result = service.get_statement_by_stock_code(stock_code)
    
    if "error" in result:
        log_error(f"종목코드 재무제표 조회 실패: {result['error']}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["error"]
        )
    
    return result["data"]

