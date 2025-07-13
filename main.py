from fastapi import FastAPI, Request, Response
from app.core.config import settings
from app.database.core import engine, Base
from app.src.account.routes import router as account_router
from app.src.trade_log.routes import router as trade_log_router
from app.src.trade_log.financial_statements.routes import router as financial_statements_router
from app.logging import log_info
from app.src.auth.routes import router as auth_router
from fastapi.responses import JSONResponse
from app.core.middleware import JWTMiddleware
import json
from app.src.stock_search.routes import router as stock_search_router
# 모든 모델 import (테이블 생성을 위해)
from app.src.common_models.users.model import User
from app.src.account.model import Account
from app.src.trade_log.financial_statements.model import FinancialStatement

# 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="국내주식 계좌 관리 API",
    version="1.0.0"
)

# 리턴 시 예외처리 하고픈 부분이 있다면 아래에 넣어주세요~
EXCLUDE_PATH_PREFIXES = []


# response 미들웨어 등록
@app.middleware("http")
async def wrap_response(request: Request, call_next):
    response: Response = await call_next(request)

    if response.media_type != 'application/json' or request.url.path in EXCLUDE_PATH_PREFIXES:
        return response

    # 이미 JSONResponse라면 body 꺼내오기
    if isinstance(response, JSONResponse):
        content = response.body
        # body가 bytes 이므로 decode 필요
        content_json = json.loads(content.decode())
    else:
        content_json = None

    wrapped = {
        "message": "Success",  # 필요하다면 커스텀 로직으로 message 채우기
        "data": content_json
    }

    return JSONResponse(content=wrapped)


# JWT 미들웨어 등록
app.add_middleware(JWTMiddleware)

# 라우터 등록
app.include_router(account_router, prefix="/api/v1/accounts", tags=["accounts"])
app.include_router(trade_log_router, prefix="/api/v1/trade-logs", tags=["trade_logs"])
app.include_router(auth_router,prefix="/api/v1/auth", tags=["auth"])
app.include_router(stock_search_router, prefix="/api/v1/stock-search", tags=["stock_search"])

app.include_router(financial_statements_router, prefix="/api/v1/financial-statements", tags=["financial_statements"])

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
