# Data Lab Routes
# 데이터 분석 관련 API 엔드포인트를 정의합니다.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .services import DataLabService
from .schemas import DataAnalysisCreate, DataAnalysisResponse, DataSourceResponse
from app.database.core import get_db

router = APIRouter(prefix="/data_lab", tags=["data_lab"])


@router.get("/analyses", response_model=List[DataAnalysisResponse])
async def get_user_analyses(
    user_id: int,
    db: Session = Depends(get_db)
):
    """사용자별 분석 결과 조회"""
    service = DataLabService(db)
    return service.get_user_analyses(user_id)


@router.get("/analyses/{analysis_id}", response_model=DataAnalysisResponse)
async def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """분석 결과 상세 조회"""
    service = DataLabService(db)
    analysis = service.get_analysis_by_id(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


@router.post("/analyses", response_model=DataAnalysisResponse)
async def create_analysis(
    analysis_data: DataAnalysisCreate,
    db: Session = Depends(get_db)
):
    """새 분석 작업 생성"""
    service = DataLabService(db)
    return service.create_analysis(analysis_data)


@router.get("/data-sources", response_model=List[DataSourceResponse])
async def get_data_sources(db: Session = Depends(get_db)):
    """사용 가능한 데이터 소스 목록 조회"""
    service = DataLabService(db)
    return service.get_available_data_sources()


@router.post("/analyses/{analysis_id}/execute")
async def execute_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """분석 실행"""
    service = DataLabService(db)
    result = service.execute_analysis(analysis_id)
    return {"message": "Analysis execution started", "analysis_id": analysis_id}
