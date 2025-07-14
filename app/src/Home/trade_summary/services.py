from typing import Dict, Any
from .repository import TradedStockRepository
from .models import HomeSummaryData
from app.database.core import get_db
from app.logging import log_debug, log_info, log_error
from app.src.auth.services import KiwoomAuthService
import requests
import json


class KiwoomAPIClient:
    """키움 API 클라이언트 - 인증은 auth 서비스 사용"""

    BASE_URL = "https://api.mockiwoom.com"  # 실전투자용

    def __init__(self):
        pass

    def get_account_summary(self, user_id: str) -> Dict[str, Any]:
        """계좌 요약 정보 조회 - 목 데이터 반환"""
        try:
            log_debug(f"🌐 계좌 요약 정보 조회: user_id={user_id}")

            # 목 데이터 반환 (실제 API 호출 대신)
            log_info(f"🔧 목 데이터 사용 - 실제 키움 API 호출 없음")
            
            mock_data = {
                "data": {
                    "user_id": user_id,
                    "internal_id": 1,
                    "total_principal": 12000000,
                    "total_profit_loss": 1800000,
                    "profit_rate": 0.15,
                    "journal_count": 55
                }
            }
            
            log_info(f"✅ 목 데이터 반환 완료: user_id={user_id}")
            return mock_data

        except Exception as e:
            log_error(f"❌ 예상치 못한 오류: {e}")
            return {"error": "계좌 요약 정보 조회 중 오류가 발생했습니다"}

    def get_realized_profit(
        self,
        user_id: str,
        data: Dict[str, Any],
        cont_yn: str = 'N',
        next_key: str = ''
    ) -> Dict[str, Any]:
        """
        일자별 종목별 실현손익 요청 (ka10073)
        """
        try:
            log_debug(f"🌐 실현손익 조회 요청 - data: {data}")

            token = KiwoomAuthService.get_token()
            if not token:
                log_error("❌ 키움 API 토큰 없음")
                return {"error": "키움 API 인증에 실패했습니다"}

            endpoint = '/api/dostk/acnt'
            url = self.BASE_URL + endpoint

            headers = {
                'Content-Type': 'application/json;charset=UTF-8',
                'authorization': f'Bearer {token}',
                'cont-yn': cont_yn,
                'next-key': next_key,
                'api-id': 'ka10073',
            }

            payload = {
                **data
            }

            log_debug(f"Request URL: {url}")
            log_debug(f"Request Headers: {headers}")
            log_debug(f"Request Payload: {payload}")

            response = requests.post(url, headers=headers, json=payload, timeout=30)

            log_debug(f"Response Status Code: {response.status_code}")
            log_debug(f"Response Body: {response.text}")

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API 호출 실패: {response.status_code}"}

        except requests.exceptions.RequestException as e:
            log_error(f"❌ 네트워크 오류: {e}")
            return {"error": "네트워크 연결 오류가 발생했습니다"}
        except Exception as e:
            log_error(f"❌ 예상치 못한 오류: {e}")
            return {"error": "실현손익 정보 조회 중 오류가 발생했습니다"}


class HomeService:
    """홈 요약 정보 서비스"""
    
    def __init__(self):
        self.kiwoom_client = KiwoomAPIClient()
        log_debug("🏠 HomeService 초기화 완료")
    
    def get_user_summary(self, user_id: str) -> Dict[str, Any]:
        """사용자 홈 요약 정보 조회"""
        log_info(f"🏠 사용자 홈 요약 정보 조회 시작: user_id={user_id}")
        
        try:
            # 데이터베이스 세션 생성
            db = next(get_db())
            repository = TradedStockRepository(db)
            
            log_debug(f"📊 Repository 초기화 완료")
            
            # 1. 데이터베이스에서 사용자 거래 내역 조회
            traded_stocks = repository.get_user_traded_stocks(user_id)
            
            log_debug(f"📊 DB 조회 결과 - 거래종목: {len(traded_stocks)}")
            
            # 2. 키움 API에서 계좌 요약 정보 조회
            api_result = self.kiwoom_client.get_account_summary(user_id)
            
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
            
            log_info(f"✅ 홈 요약 정보 조회 완료: user_id={user_id}")
            
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
