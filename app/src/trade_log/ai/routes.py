from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.core import get_db
from .services import analyze_trade_log
from .schemas import AIAnalysisResponse

router = APIRouter()

@router.get("", response_model=AIAnalysisResponse)
def get_ai_analysis(trade_log_id: int, db: Session = Depends(get_db)):
    try:
        result = analyze_trade_log(db, trade_log_id)
        if not result:
            raise HTTPException(status_code=404, detail="분석 결과를 찾을 수 없습니다.")
        
        # 여기서 commit을 해줍니다.
        db.commit()
        
        return {
            "message": 'success',
            "data": result
        }
    except Exception as e:
        # 에러 발생 시 rollback
        db.rollback()
        raise HTTPException(status_code=500, detail=f"서버 오류: {e}")
