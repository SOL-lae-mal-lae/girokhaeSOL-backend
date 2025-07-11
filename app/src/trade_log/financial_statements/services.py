from sqlalchemy.orm import Session
from typing import Dict, Any
from .repository import FinancialStatementRepository
from .schemas import FinancialStatementResponse
from app.logging import log_debug, log_info, log_error


class FinancialStatementService:
    """재무제표 비즈니스 로직 서비스"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = FinancialStatementRepository(db)
    
    def get_statement_by_stock_code(self, stock_code: str) -> Dict[str, Any]:
        """종목코드로 재무제표 조회"""
        try:
            log_debug(f"종목코드 재무제표 조회: {stock_code}")
            statement = self.repository.get_by_stock_code(stock_code)
            
            if not statement:
                log_error(f"재무제표를 찾을 수 없음: {stock_code}")
                return {"error": f"종목코드 {stock_code}에 해당하는 재무제표를 찾을 수 없습니다"}
            
            response_data = FinancialStatementResponse.model_validate(statement)
            
            log_info(f"종목코드 재무제표 조회 성공: {stock_code}")
            return {"data": response_data}
            
        except Exception as e:
            log_error(f"종목코드 재무제표 조회 중 오류: {e}")
            return {"error": "재무제표 조회 중 서버 오류가 발생했습니다"}
    
   
