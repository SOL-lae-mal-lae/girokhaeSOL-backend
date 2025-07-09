# Data Lab Schemas
# 데이터 분석 관련 API 요청/응답을 위한 Pydantic 스키마를 정의합니다.

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class DataAnalysisBase(BaseModel):
    """데이터 분석 기본 스키마"""
    analysis_type: str
    title: str
    description: Optional[str] = None


class DataAnalysisCreate(DataAnalysisBase):
    """데이터 분석 생성 요청 스키마"""
    user_id: int
    parameters: Optional[Dict[str, Any]] = None


class DataAnalysisUpdate(BaseModel):
    """데이터 분석 업데이트 요청 스키마"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    result_data: Optional[str] = None


class DataAnalysisResponse(DataAnalysisBase):
    """데이터 분석 응답 스키마"""
    id: int
    user_id: int
    status: str
    result_data: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DataSourceBase(BaseModel):
    """데이터 소스 기본 스키마"""
    name: str
    source_type: str
    file_path: Optional[str] = None
    api_endpoint: Optional[str] = None
    connection_string: Optional[str] = None


class DataSourceCreate(DataSourceBase):
    """데이터 소스 생성 요청 스키마"""
    pass


class DataSourceResponse(DataSourceBase):
    """데이터 소스 응답 스키마"""
    id: int
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
