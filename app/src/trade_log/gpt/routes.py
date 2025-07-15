from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.core import SessionLocal
from .services import GPTAnalysisService
from .schemas import GPTAnalysisRequest, GPTAnalysisResponse, ErrorResponse

router = APIRouter()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/analyze",
    responses={
        200: {"description": "GPT 분석 성공"},
        400: {"model": ErrorResponse, "description": "잘못된 요청"},
        401: {"model": ErrorResponse, "description": "인증이 필요합니다"},
        404: {"model": ErrorResponse, "description": "거래 로그를 찾을 수 없습니다"},
        500: {"model": ErrorResponse, "description": "서버 내부 오류"}
    }
)
def analyze_trade_log(
    analysis_request: GPTAnalysisRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """거래 로그 GPT 분석"""
    try:
        # request.state에서 user_id 가져오기
        user_id = getattr(request.state, 'user', 'user123')  # 기본값 설정
        service = GPTAnalysisService(db)
        return service.analyze_trade_log(user_id, analysis_request)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="GPT 분석 중 오류가 발생했습니다.")

@router.get(
    "/analysis/{trade_log_id}",
    response_model=GPTAnalysisResponse,
    responses={
        200: {"model": GPTAnalysisResponse, "description": "분석 결과 조회 성공"},
        400: {"model": ErrorResponse, "description": "잘못된 요청"},
        401: {"model": ErrorResponse, "description": "인증이 필요합니다"},
        404: {"model": ErrorResponse, "description": "분석 결과를 찾을 수 없습니다"},
        500: {"model": ErrorResponse, "description": "서버 내부 오류"}
    }
)
def get_analysis(
    trade_log_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """저장된 GPT 분석 결과 조회"""
    try:
        # request.state에서 user_id 가져오기
        user_id = getattr(request.state, 'user', 'user123')  # 기본값 설정
        service = GPTAnalysisService(db)
        return service.get_analysis(user_id, trade_log_id)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="오류가 발생했습니다.")
