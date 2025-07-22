from typing import Dict, Any
from .models import HomeSummaryData
from app.database.core import get_db
from app.logging import log_debug, log_info, log_error
from app.core.oauth_token import get_oauth_token

import requests
import json


class KiwoomAPIClient:
    """키움 API 클라이언트 - 인증은 auth 서비스 사용"""

    def __init__(self):
        pass

    def get_account_summary(self, token: str, params: Dict[str, Any]):
        """계좌 요약 정보 조회 - 실제 API 호출"""
        try:
            # 토큰 값 로깅
            log_debug(f"🔑 전달받은 토큰: {token}")
            
            # 1. 요청할 API URL
            host = "https://mockapi.kiwoom.com"
            endpoint = '/api/dostk/acnt'
            url = host + endpoint

            # 2. 헤더 설정
            headers = {
                'Content-Type': 'application/json;charset=UTF-8', 
                'authorization': token,  # 대문자 Authorization으로 변경
                'api-id': 'ka10074',  # TR명
            }
            
            # 헤더 로깅
            log_debug(f"📤 요청 헤더: {headers}")
            log_debug(f"📤 요청 파라미터: {params}")

            # 3. API 호출 (POST 요청)
            response = requests.post(url, headers=headers, json=params)

            # 4. 응답 상태 코드 확인
            if response.status_code == 200:
                # 성공적으로 데이터 받았을 경우
                log_debug(f"✅ API 호출 성공: {response.json()}")
                return response.json()  # API 응답 데이터 반환
            else:
                log_error(f"❌ API 호출 실패: {response.status_code}, Response: {response.text}")
           

        except Exception as e:
            log_error(f"❌ 예상치 못한 오류: {e}")
            return {"error": "계좌 요약 정보 조회 중 오류가 발생했습니다"}


class HomeService:
    """홈 요약 정보 서비스"""
    
    def __init__(self):
        self.kiwoom_client = KiwoomAPIClient()
        log_debug("🏠 HomeService 초기화 완료")
    
    
    def get_user_summary(self, token: str, params: Dict[str, Any]):
        """사용자 홈 요약 정보 조회"""
        
        try:
            log_debug(f"📊 Repository 초기화 완료")
      
            # 2. 키움 API에서 계좌 요약 정보 조회 (사용자가 전달한 params 사용)
            api_params = {
                "strt_dt": params.get("start_date", "20250715"),
                "end_dt": params.get("end_date", "20250715")
            }
            api_result = self.kiwoom_client.get_account_summary(token, api_params)
            
            if "error" in api_result:
                log_error(f"❌ 키움 API 조회 실패: {api_result['error']}")
                return {"error": api_result["error"]}
            
            log_debug(f"🌐 키움 API 조회 결과: {api_result}")
            
            # 3. 데이터 통합 및 응답 생성 - 실제 API 응답 구조 사용
            # 총 매수금액을 투자원금으로, 실현손익을 누적손익으로 사용
            total_buy_amt = int(api_result.get("tot_buy_amt", "0"))
            realized_pl = int(api_result.get("rlzt_pl", "0"))
            
            # 손익률 계산 (실현손익 / 총매수금액 * 100)
            profit_rate = (realized_pl / total_buy_amt * 100) if total_buy_amt > 0 else 0.0
            
            # 일별 거래 내역에서 거래일지 개수 계산
            dt_records = api_result.get("dt_rlzt_pl", [])
            journal_count = len([record for record in dt_records if record.get("dt")])
            
            summary_data = HomeSummaryData(
                id=1,  # 내부 ID
                journal_count_year=journal_count,  # 매매일지 개수
                cumulative_investment_principal=total_buy_amt,  # 투자 원금 (총 매수금액)
                cumulative_profit_loss=realized_pl,  # 투자 손익 (실현손익)
                cumulative_profit_rate=round(profit_rate, 2)  # 손익률
            )
            
            return {
                "data": summary_data.dict(),  # Pydantic 모델을 딕셔너리로 변환
                "success": True
            }
        
        except Exception as e:
            log_error(f"❌ HomeService 오류: {e}")
            return {"error": f"홈 요약 정보 처리 중 오류가 발생했습니다: {str(e)}"}
