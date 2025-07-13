from pydantic import BaseModel, Field
from typing import Optional
from .models import HomeSummaryData


# 응답 스키마
class HomeSummaryResponse(BaseModel):
    """홈 요약 정보 응답 스키마"""
    message: str = Field(..., description="응답 메시지")
    data: HomeSummaryData = Field(..., description="요약 정보 데이터")

# 에러 응답 스키마
class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    error: str
    detail: Optional[str] = None

# 성공 응답 스키마
class SuccessResponse(BaseModel):
    """성공 응답 스키마"""
    message: str
    data: Optional[dict] = None
