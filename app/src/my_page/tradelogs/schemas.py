from pydantic import BaseModel
from typing import List

class TradeDetailResponse(BaseModel):
    trade_log_id: int
    date: str
    buy_quantity: int
    sell_quantity: int

    class Config:
        orm_mode = True
