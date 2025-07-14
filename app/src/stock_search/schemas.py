from pydantic import BaseModel
from typing import List, Optional

class StockSearchRequest(BaseModel):
    stock_name: str

class StockItem(BaseModel):
    stock_name: str
    stock_code: str

class StockSearchResponse(BaseModel):
    message: str
    data: List[StockItem]

class ErrorResponse(BaseModel):
    detail: str
