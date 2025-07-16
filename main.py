from fastapi import FastAPI, Request, Response
from app.core.config import settings
from app.database.core import engine, Base
from app.src.account.routes import router as account_router
from app.src.trade_log.month_trade_log.routes import router as trade_log_router
from app.src.trade_log.financial_statements.routes import router as financial_statements_router
from app.src.Home.trade_summary.routes import router as home_router
from app.logging import log_info
from fastapi.responses import JSONResponse
from app.core.middleware import JWTMiddleware, KiwoomOAuthMiddleware
import json
from app.src.stock_search.routes import router as stock_search_router
from app.src.trade_log.chart.routes import router as chart_router
from app.src.trade_log.routes import router as trade_log_post_router

# 모든 모델 import (테이블 생성을 위해)
from app.src.common_models.users.model import User
from app.src.account.model import Account
# from app.src.financial_statements.model import FinancialStatement  # 임시 주석

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # 프론트엔드에서 요청을 허용할 주소
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용
    allow_headers=["*"],  # 모든 헤더를 허용
)
# 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="국내주식 계좌 관리 API",
    version="1.0.0"
)

# 리턴 시 예외처리 하고픈 부분이 있다면 아래에 넣어주세요~
EXCLUDE_PATH_PREFIXES = []



# JWT 미들웨어 등록
app.add_middleware(JWTMiddleware)
app.add_middleware(KiwoomOAuthMiddleware)
# 라우터 등록
app.include_router(account_router, prefix="/api/v1/accounts", tags=["accounts"])
app.include_router(financial_statements_router, prefix="/api/v1/financial-statements", tags=["financial-statements"])
app.include_router(home_router, prefix="/api/v1/home", tags=["home"])
app.include_router(trade_log_router, prefix="/api/v1/trade-logs", tags=["trade_logs"])
app.include_router(stock_search_router, prefix="/api/v1/stock-search", tags=["stock_search"])
app.include_router(stock_search_router, prefix="/api/v1/trade-logs", tags=["trade_logs"])
app.include_router(chart_router, prefix="/api/v1/trade-logs", tags=["trade_logs"])
app.include_router(trade_log_post_router, prefix="/api/v1/trade-logs", tags=["trade_logs"])

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
