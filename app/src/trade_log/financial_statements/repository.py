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
    
    def insert_by_stock_code_and_yyyymm(self, data: dict) -> FinancialStatement:
        """stock_code+yyyymm으로 재무제표 upsert (있으면 update, 없으면 insert)"""
        try:
            stock_code = data.get("stk_cd")
            yyyymm = data.get("yyyymm")
            if not stock_code or not yyyymm:
                raise ValueError("stock_code와 yyyymm은 필수입니다.")
            def to_float(val):
                return float(val) if val not in (None, "") else None
            def to_int(val):
                return int(val) if val not in (None, "") else None
            statement = self.db.query(FinancialStatement).filter(
                FinancialStatement.stock_code == stock_code,
                FinancialStatement.yyyymm == yyyymm
            ).first()
            if not statement:
                statement = FinancialStatement(
                    stock_code=stock_code,
                    mac=to_int(data.get("mac")),
                    per=to_float(data.get("per")),
                    eps=to_float(data.get("eps")),
                    pbr=to_float(data.get("pbr")),
                    roe=to_float(data.get("roe")),
                    sale_amt=to_int(data.get("sale_amt")),
                    bus_pro=to_int(data.get("bus_pro")),
                    cup_nga=to_int(data.get("cup_nga")),
                    yyyymm=yyyymm,
                )
                self.db.add(statement)
            else:
                statement.mac = to_int(data.get("mac"))
                statement.per = to_float(data.get("per"))
                statement.eps = to_float(data.get("eps"))
                statement.pbr = to_float(data.get("pbr"))
                statement.roe = to_float(data.get("roe"))
                statement.sale_amt = to_int(data.get("sale_amt"))
                statement.bus_pro = to_int(data.get("bus_pro"))
                statement.cup_nga = to_int(data.get("cup_nga"))
            self.db.commit()
            self.db.refresh(statement)
            return statement
        except Exception as e:
            log_error(f"재무제표 upsert 중 오류: {e}")
            self.db.rollback()
            raise
    
   
