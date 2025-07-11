from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.database.core import SessionLocal, engine, Base
from app.src.account.routes import router as account_router
# from app.src.financial_statements.routes import router as financial_statements_router  # 임시 주석
from app.src.trade_log.routes import router as trade_log_router
from app.logging import log_info

# 모든 모델 import (테이블 생성을 위해)
from app.src.common_models.users import User
from app.src.account.model import Account
# from app.src.financial_statements.model import FinancialStatement  # 임시 주석

# 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="국내주식 계좌 관리 API",
    version="1.0.0"
)

# 라우터 등록
app.include_router(account_router, prefix="/api/v1/accounts", tags=["accounts"])
# app.include_router(financial_statements_router, prefix="/api/v1/financial-statements", tags=["financial-statements"])  # 임시 주석
app.include_router(trade_log_router, prefix="/api/v1/trade-logs", tags=["trade_logs"])
@app.get("/api/v1/")
def read_root():
    log_info("루트 엔드포인트 호출")
    return {"message": "국내주식 관리 API 서버가 정상 작동 중입니다", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
