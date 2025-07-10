from pydantic import BaseModel
from typing import List, Optional

class TradeLogBase(BaseModel):
    user_id: str
    date: Optional[str] = None
    investment_type: Optional[str] = None
    rationale: Optional[str] = None
    evaluation: Optional[str] = None

class TradeLogCreate(TradeLogBase):
    pass

class TradeLogUpdate(BaseModel):
    pass

class TradeLogMonthlyData(BaseModel):
    dates: List[str]

class TradeLogMonthlyResponse(BaseModel):
    message: str
    data: TradeLogMonthlyData

class ErrorResponse(BaseModel):
    message: str = "오류가 발생했습니다."
