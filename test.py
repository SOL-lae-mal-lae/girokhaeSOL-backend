import os
import time
import requests
import json
from dotenv import load_dotenv
from app.database.core import get_db
from app.src.stock_search.model import Stock

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
def get_stock_codes():
    db_gen = get_db()
    db = next(db_gen)
    try:
        codes = [row.stock_code for row in db.query(Stock).limit(10)]
        return codes
    finally:
        db_gen.close()

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
    else:
        print(f"Error({stock_code}):", response.status_code, response.text)

if __name__ == "__main__":
    token = get_kiwoom_token()
    codes = get_stock_codes()
    for code in codes:
        fn_ka10001(token, code)
        time.sleep(1)