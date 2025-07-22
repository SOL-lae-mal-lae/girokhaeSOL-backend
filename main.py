from fastapi import FastAPI, Request, Response
from app.core.config import settings
from app.database.core import engine, Base
from app.src.account.routes import router as account_router
from app.src.trade_log.month_trade_log.routes import router as trade_log_router
from app.src.trade_log.financial_statements.routes import router as financial_statements_router
from app.src.Home.trade_summary.routes import router as home_router
from app.logging import log_info
from app.core.middleware import JWTMiddleware, KiwoomOAuthMiddleware
from app.core.account_token_middleware import AccountTokenMiddleware
from app.src.stock_search.routes import router as stock_search_router
from app.src.trade_log.chart.routes import router as chart_router
from app.src.trade_log.routes import router as trade_log_post_router
from app.src.trade_log.ai.routes import router as ai_analysis_router
from app.src.community.posts.routes import router as posts_router
from app.src.community.comments.routes import router as comments_router

# 모든 모델 import (테이블 생성을 위해)
from app.src.common_models.users.model import User
from app.src.account.model import Account
# from app.src.financial_statements.model import FinancialStatement  # 임시 주석
from app.src.trade_log.financial_statements.repository import FinancialStatementRepository
from app.src.community.posts.model import Post
from app.src.community.comments.model import Comment

from fastapi.middleware.cors import CORSMiddleware

import os
import time
import requests
import json
from dotenv import load_dotenv
from app.database.core import get_db
from app.src.stock_search.model import Stock
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# .env에서 환경변수 읽기
load_dotenv()
APP_KEY = os.getenv("SCHEDULER_APP_KEY")
APP_SECRET = os.getenv("SCHEDULER_SECRET_KEY")

# 1. 키움 토큰 발급 함수
def get_kiwoom_token():
    url = "https://mockapi.kiwoom.com/oauth2/token"
    headers = {
        "Content-Type": "application/json;charset=UTF-8"
    }
    data = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "secretkey": APP_SECRET
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    token = response.json()["token"]
    return token

# 2. DB에서 종목코드 가져오기 (get_db 사용, ORM 방식)
# def get_stock_codes():
#     db_gen = get_db()
#     db = next(db_gen)
#     try:
#         codes = [row.stock_code for row in db.query(Stock).limit(10)]
#         return codes
#     finally:
#         db_gen.close()

# 3. 주식기본정보요청 함수
def fn_ka10001(token, stock_code):
    url = "https://mockapi.kiwoom.com/api/dostk/stkinfo"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "authorization": f"Bearer {token}",
        "cont-yn": "N",
        "next-key": "",
        "api-id": "ka10001",
    }
    data = {"stk_cd": stock_code}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        body = response.json()
        # 필요한 값만 추출
        filtered = {k: body.get(k) for k in ["stk_cd", "mac", "per", "eps", "pbr", "roe", "sale_amt", "bus_pro", "cup_nga"]}
        print(json.dumps(filtered, ensure_ascii=False, indent=2))
        return filtered
    else:
        print(f"Error({stock_code}):", response.status_code, response.text)
        return None

# 스케줄러에서 실행할 작업 함수
def run_stock_info_job():
    print("[스케줄러] 주식기본정보 수집 작업 시작!")
    token = get_kiwoom_token()
    db_gen = get_db()
    db = next(db_gen)
    try:
        codes = [row.stock_code for row in db.query(Stock).limit(200)]
        repo = FinancialStatementRepository(db)
        yyyymm = datetime.now().strftime("%Y%m")
        for code in codes:
            data = fn_ka10001(token, code)
            if data:
                data["yyyymm"] = yyyymm
                repo.insert_by_stock_code_and_yyyymm(data)
            time.sleep(1)
    finally:
        db_gen.close()
    print("[스케줄러] 주식기본정보 수집 작업 완료!")

# FastAPI 앱 생성 이후, 스케줄러 실행
scheduler = BackgroundScheduler(timezone="Asia/Seoul")
scheduler.add_job(run_stock_info_job, 'cron', day=21, hour=17, minute=12)
scheduler.start()

# FastAPI 앱 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="국내주식 계좌 관리 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 프론트엔드에서 요청을 허용할 주소
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용 (OPTIONS 포함)
    allow_headers=["*"],  # 모든 헤더를 허용
)

# 테이블 생성
Base.metadata.create_all(bind=engine)

# 리턴 시 예외처리 하고픈 부분이 있다면 아래에 넣어주세요~
EXCLUDE_PATH_PREFIXES = []



# 미들웨어 등록 (역순으로 실행되므로 의존성이 있는 미들웨어를 나중에 등록)
app.add_middleware(AccountTokenMiddleware)
app.add_middleware(KiwoomOAuthMiddleware)
app.add_middleware(JWTMiddleware)
# 라우터 등록
app.include_router(account_router, prefix="/api/v1/accounts", tags=["accounts"])
app.include_router(financial_statements_router, prefix="/api/v1/financial-statements", tags=["financial-statements"])
app.include_router(home_router, prefix="/api/v1/home", tags=["home"])
app.include_router(trade_log_router, prefix="/api/v1/trade-logs", tags=["trade_logs"])
app.include_router(stock_search_router, prefix="/api/v1/trade-logs", tags=["trade_logs"])
app.include_router(chart_router, prefix="/api/v1/trade-logs", tags=["trade_logs"])
app.include_router(trade_log_post_router, prefix="/api/v1/trade-logs", tags=["trade_logs"])
app.include_router(ai_analysis_router, prefix="/api/v1/trade-logs/ai", tags=["trade_logs"])
app.include_router(posts_router, prefix="/api/v1/community", tags=["community"])
app.include_router(comments_router, prefix="/api/v1/community", tags=["community"])

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
