from sqlalchemy.orm import Session
from typing import Optional
from .model import GPTAnalysis
from .schemas import GPTAnalysisCreate
from datetime import datetime

class GPTAnalysisRepository:
    """GPT 분석 데이터 접근 레이어"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_analysis_by_trade_log_id(self, trade_log_id: int) -> Optional[GPTAnalysis]:
        """거래 로그 ID로 GPT 분석 결과 조회"""
        return self.db.query(GPTAnalysis)\
            .filter(GPTAnalysis.trade_log_id == trade_log_id)\
            .first()
    
    def create_analysis(self, analysis_data: GPTAnalysisCreate) -> GPTAnalysis:
        """GPT 분석 결과 생성"""
        db_analysis = GPTAnalysis(
            trade_log_id=analysis_data.trade_log_id,
            result=analysis_data.result
        )
        self.db.add(db_analysis)
        self.db.commit()
        self.db.refresh(db_analysis)
        return db_analysis
    
    def update_analysis(self, trade_log_id: int, result: str) -> Optional[GPTAnalysis]:
        """GPT 분석 결과 업데이트"""
        analysis = self.db.query(GPTAnalysis)\
            .filter(GPTAnalysis.trade_log_id == trade_log_id)\
            .first()
        
        if analysis:
            analysis.result = result
            analysis.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(analysis)
        
        return analysis
    
    def delete_analysis(self, trade_log_id: int) -> bool:
        """GPT 분석 결과 삭제"""
        analysis = self.db.query(GPTAnalysis)\
            .filter(GPTAnalysis.trade_log_id == trade_log_id)\
            .first()
        
        if analysis:
            self.db.delete(analysis)
            self.db.commit()
            return True
        
        return False
