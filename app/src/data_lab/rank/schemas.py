from pydantic import BaseModel

class StockRankSchema(BaseModel):
    stock_name: str
    stock_code: str
    order_count: int
