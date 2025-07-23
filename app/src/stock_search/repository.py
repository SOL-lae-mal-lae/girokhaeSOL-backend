from sqlalchemy.orm import Session
from .model import Stock
from typing import List

class StockRepository:
    def __init__(self, db: Session):
        self.db = db

    def search_stocks_by_name(self, stock_name: str) -> List[Stock]:
        # 부분 일치 검색 (대소문자 구분 없음)
        return (
            self.db.query(Stock)
            .filter(Stock.stock_name.like(f"%{stock_name}%"))
            .all()
        )

    def get_all_stocks(self) -> List[Stock]:
        return self.db.query(Stock).order_by(Stock.stock_name.asc()).all()
