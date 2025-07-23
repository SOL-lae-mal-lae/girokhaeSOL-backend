from pydantic import BaseModel, Field
from typing import Optional




# 응답 스키마
class FinancialStatementResponse(BaseModel):
    """재무제표 응답 스키마"""
    id: int
    stock_code: str
    pbr: Optional[float]
    per: Optional[float]
    eps: Optional[float]
    roe: Optional[float]
    mac: Optional[int]
    sale_amt: Optional[int]
    bus_pro: Optional[int]
    cup_nga: Optional[int]
    yyyymm: Optional[str]
    
    class Config:
        from_attributes = True

class FinancialStatementListResponse(BaseModel):
    """재무제표 목록 응답 스키마"""
    message: str
    data: list[FinancialStatementResponse]
    count: Optional[int] = None

# 에러 응답 스키마
class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    error: str
    detail: Optional[str] = None

class SuccessResponse(BaseModel):
    """성공 응답 스키마"""
    message: str
    data: Optional[dict] = None
