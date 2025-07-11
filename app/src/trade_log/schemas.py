from pydantic import BaseModel
from typing import List, Optional

class TradeLogBase(BaseModel):
    user_id: str
    date: Optional[str] = None
    investment_type: Optional[str] = None
    rationale: Optional[str] = None
    evaluation: Optional[str] = None

class TradeLogCreate(BaseModel):
    pass

class TradeLogUpdate(BaseModel):
    pass

class TradeLogMonthlyData(BaseModel):
    dates: List[str]
    total_buy_amount: float
    total_sell_amount: float
    profit_rate: float
    total_commission_and_tax: float
    sentiment: List[str]
    top_buy: List[str]


class TradeLogMonthlyResponse(BaseModel):
    message: str
    data: TradeLogMonthlyData

class ErrorResponse(BaseModel):
    message: str = "오류가 발생했습니다."
