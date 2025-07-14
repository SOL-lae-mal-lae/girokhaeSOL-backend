from sqlalchemy.orm import Session
from .repository import StockRepository
from .schemas import StockItem
from typing import List

class StockSearchService:
    def __init__(self, db: Session):
        self.repo = StockRepository(db)

    def search_stocks(self, stock_name: str) -> List[StockItem]:
        stocks = self.repo.search_stocks_by_name(stock_name)
        return [StockItem(stock_name=s.stock_name, stock_code=s.stock_code) for s in stocks]
