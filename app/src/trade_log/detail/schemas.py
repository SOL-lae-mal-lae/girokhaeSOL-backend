from pydantic import BaseModel
from typing import List
from datetime import date

class TradeSummarySchema(BaseModel):
    total_buy_amount: int
    total_sell_amount: int
    total_cmsn_tax: float
    settlement_amount: int
    profit_rate: float

class TradeDetailSchema(BaseModel):
    account_id: int
    stock_name: str
    stock_code: str
    avg_buy_price: float
    buy_quantity: int
    avg_sell_price: float
    sell_quantity: int
    cmsn_alm_tax: float
    profit_amount: int
    profit_rate: float

class ChartSchema(BaseModel):
    stock_code: str
    start_date: date
    end_date: date
    sequence: int

class NewsLinkSchema(BaseModel):
    url: str
      
class TradeLogCreateSchema(BaseModel):
    date: date
    summaries: TradeSummarySchema
    trade_details: List[TradeDetailSchema]
    charts: List[ChartSchema]
    investment_type: str
    sentiments: List[str]
    rationale: str
    evaluation: str
    news_links: List[NewsLinkSchema]

class TradeLogResponseSchema(BaseModel):
    id: int
    user_id: str
    date: date
    investment_type: str
    rationale: str
    evaluation: str
    summary: TradeSummarySchema
    details: List[TradeDetailSchema]
    charts: List[ChartSchema]
    news_links: List[NewsLinkSchema]
    sentiments: List[str]
