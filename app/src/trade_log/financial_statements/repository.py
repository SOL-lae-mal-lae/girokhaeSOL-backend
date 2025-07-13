from sqlalchemy.orm import Session
from typing import Optional
from .model import FinancialStatement
from app.logging import log_debug, log_error

class FinancialStatementRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_stock_code(self, stock_code: str) -> Optional[FinancialStatement]:
        """종목코드로 재무제표 조회"""
        try:
            log_debug(f"종목코드 재무제표 조회 시작: 종목코드={stock_code}")
            statement = self.db.query(FinancialStatement).filter(
                FinancialStatement.stock_code == stock_code
            ).first()
            log_debug(f"종목코드 재무제표 조회 완료: {'발견' if statement else '없음'}")
            return statement
        except Exception as e:
            log_error(f"종목코드 재무제표 조회 중 오류: {e}")
            return None
    
   
