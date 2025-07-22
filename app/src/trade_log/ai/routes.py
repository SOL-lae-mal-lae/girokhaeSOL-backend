from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.database.core import get_db
from .services import analyze_trade_log, get_trade_log_by_date
from .schemas import AIAnalysisResponseSchema

router = APIRouter()

@router.get("", response_model=AIAnalysisResponseSchema)
def get_ai_analysis(date: str, request: Request, db: Session = Depends(get_db)):
    try:
        user_id = getattr(request.state, "user", None)
        date = date.strip()
        trade_log_id = get_trade_log_by_date(db, user_id ,date)
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
