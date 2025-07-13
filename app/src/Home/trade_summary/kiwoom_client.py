import requests
import json
from typing import Dict, Any
from app.logging import log_info, log_error, log_debug


class KiwoomAPIClient:
    """키움 API 클라이언트 - 계좌 요약 정보만 제공"""
    
    def __init__(self):
        self.host = 'https://mockapi.kiwoom.com'  # 모의투자
        # self.host = 'https://api.kiwoom.com'  # 실전투자
        self.appkey = 'ck2aFnUqE5w2if5WX2gYNXUlw9mMsw4OQHUMy4mSYuw'
        self.secretkey = 'B781rDYU855V4uy7ljdF-q-3zhA4j47W-sBwMl85_jQ'
    
    def get_account_summary(self, user_id: str) -> Dict[str, Any]:
        """계좌 요약 정보 조회 - 홈 화면용"""
        try:
            log_debug(f"계좌 요약 정보 조회: user_id={user_id}")
            
            # 키움 API 호출 (실제 API 엔드포인트로 교체 필요)
            endpoint = '/api/account/summary'
            url = self.host + endpoint
            
            headers = {
                'Content-Type': 'application/json',
                'appkey': self.appkey,
                'secretkey': self.secretkey
            }
            
            request_data = {
                'user_id': user_id
            }
            
            response = requests.post(url, headers=headers, json=request_data)
            
            if response.status_code == 200:
                response_data = response.json()
                
                # 응답 데이터 구조 확인 및 변환
                if 'data' in response_data:
                    summary_data = response_data['data']
                    
                    # API 명세에 맞는 형태로 데이터 구조화
                    formatted_data = {
                        "Id": summary_data.get("user_id", user_id),
                        "id": summary_data.get("internal_id", 1),
                        "journal_count_year": summary_data.get("journal_count", 55),
                        "cumulative_investment_principal": summary_data.get("total_principal", 12000000),
                        "cumulative_profit_loss": summary_data.get("total_profit_loss", 1800000),
                        "cumulative_profit_rate": summary_data.get("profit_rate", 0.15)
                    }
                    
                    log_info(f"계좌 요약 정보 조회 성공: user_id={user_id}")
                    return {"data": formatted_data}
                else:
                    log_error("API 응답에 data 필드가 없습니다")
                    return {"error": "API 응답 형식이 올바르지 않습니다"}
            else:
                log_error(f"API 호출 실패: {response.status_code}, {response.text}")
                return {"error": f"API 호출 실패: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            log_error(f"네트워크 오류: {e}")
            return {"error": "네트워크 연결 오류가 발생했습니다"}
        except Exception as e:
            log_error(f"계좌 요약 정보 조회 중 오류: {e}")
            return {"error": "계좌 요약 정보 조회 중 오류가 발생했습니다"}
