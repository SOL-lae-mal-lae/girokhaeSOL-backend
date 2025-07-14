from typing import Dict, Any
from .repository import TradedStockRepository
from .models import HomeSummaryData
from app.database.core import get_db
from app.logging import log_debug, log_info, log_error

import requests
import json


class KiwoomAPIClient:
    """키움 API 클라이언트 - 인증은 auth 서비스 사용"""

    BASE_URL = "https://mockapi.kiwoom.com"  # 실전투자용 URL

    def __init__(self):
        pass

    def get_account_summary(self, user_id: str, token: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """계좌 요약 정보 조회 - 실제 API 호출"""
        try:
            log_debug(f"🌐 계좌 요약 정보 조회: user_id={user_id}, params={params}")

            # 1. 요청할 API URL
            host = self.BASE_URL
            endpoint = '/api/dostk/acnt'
            url = host + endpoint

            # 2. 헤더 설정
            headers = {
                'Content-Type': 'application/json;charset=UTF-8', 
                'authorization': token,  # 접근토큰
                'api-id': 'ka10073',  # TR명
            }

            # 3. API 호출 (GET 요청으로 변경, params 사용)
            response = requests.get(url, headers=headers, params=params)

            # 4. 응답 상태 코드 확인
            if response.status_code == 200:
                # 성공적으로 데이터 받았을 경우
                log_info(f"✅ API 호출 성공: user_id={user_id}")
                return response.json()  # API 응답 데이터 반환
            else:
                log_error(f"❌ API 호출 실패: {response.status_code}")
                return {"error": "API 호출 실패"}

        except Exception as e:
            log_error(f"❌ 예상치 못한 오류: {e}")
            return {"error": "계좌 요약 정보 조회 중 오류가 발생했습니다"}


class HomeService:
    """홈 요약 정보 서비스"""
    
    def __init__(self):
        self.kiwoom_client = KiwoomAPIClient()
        log_debug("🏠 HomeService 초기화 완료")
    
    def get_user_summary(self, user_id: str, token: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """사용자 홈 요약 정보 조회"""
        log_info(f"🏠 사용자 홈 요약 정보 조회 시작: user_id={user_id}, start_date={start_date}, end_date={end_date}")
        
        try:
            # 데이터베이스 세션 생성
            db = next(get_db())
            repository = TradedStockRepository(db)
            
            log_debug(f"📊 Repository 초기화 완료")
            
            # 1. 데이터베이스에서 사용자 거래 내역 조회
            traded_stocks = repository.get_user_traded_stocks(user_id)
            
            log_debug(f"📊 DB 조회 결과 - 거래종목: {len(traded_stocks)}")
            
            # 2. 키움 API에서 계좌 요약 정보 조회 (사용자가 전달한 params 사용)
            params = {
                'user_id': user_id,
                'start_date': start_date,
                'end_date': end_date
            }
            api_result = self.kiwoom_client.get_account_summary(user_id, token, params)
            
            if "error" in api_result:
                log_error(f"❌ 키움 API 조회 실패: {api_result['error']}")
                return {"error": api_result["error"]}
            
            log_debug(f"🌐 키움 API 조회 결과: {api_result}")
            
            # 3. 데이터 통합 및 응답 생성
            api_data = api_result.get("data", {})
            summary_data = HomeSummaryData(
                Id=user_id,  # 사용자 고유 ID
                id=api_data.get("internal_id", 1),  # 내부 ID
                journal_count_year=api_data.get("journal_count", 55),  # 매매일지 개수
                cumulative_investment_principal=api_data.get("total_principal", 12000000),  # 투자 원금
                cumulative_profit_loss=api_data.get("total_profit_loss", 1800000),  # 투자 손익
                cumulative_profit_rate=api_data.get("profit_rate", 0.15)  # 손익률
            )
            
            return {
                "data": summary_data.dict(),
                "success": True
            }
        
        except Exception as e:
            log_error(f"❌ HomeService 오류: {e}")
            return {"error": f"홈 요약 정보 처리 중 오류가 발생했습니다: {str(e)}"}
        finally:
            if 'db' in locals():
                db.close()
                log_debug("🔒 DB 세션 종료")
