from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class GPTAnalysisRequest(BaseModel):
    """GPT 분석 요청 스키마"""
    trade_log_id: int = Field(..., description="분석할 거래 로그 ID")

class GPTAnalysisResponse(BaseModel):
    """GPT 분석 응답 스키마"""
    trade_log_id: int
    result: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class GPTAnalysisCreate(BaseModel):
    """GPT 분석 생성 스키마"""
    trade_log_id: int
    result: str

class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    error: str
    detail: Optional[str] = None
