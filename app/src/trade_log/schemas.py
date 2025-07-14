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

class Summaries(BaseModel):
    total_buy_amount: int
    total_sell_amount: int
    total_cmsn_tax: float
    settlement_amount: int
    profit_rate: float

class TradeDetails(BaseModel):
    stock_name: str
    stock_code: str
    avg_buy_price: float
    buy_quantity: int
    avg_sell_price: float
    sell_quantity: int
    cmsn_alm_tax: float
    profit_amount: int
    profit_rate: float

class TradeTransaction(BaseModel):
    summaries: Summaries
    trade_details: List[TradeDetails]

class TradeLogTransactionResponse(BaseModel):
    message: str
    data: TradeTransaction