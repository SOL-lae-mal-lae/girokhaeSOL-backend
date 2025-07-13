from typing import Dict, Any
from .kiwoom_client import KiwoomAPIClient
from .models import HomeSummaryData
from app.logging import log_debug, log_info, log_error


class HomeService:
    """홈 서비스 - 계좌 요약 정보만 제공"""
    
    def __init__(self):
        self.kiwoom_client = KiwoomAPIClient()
    
    def get_user_summary(self, user_id: str) -> Dict[str, Any]:
        """사용자 홈 요약 정보 조회"""
        try:
            log_debug(f"사용자 홈 요약 정보 조회: {user_id}")
            
            # 키움 API를 통해 계좌 요약 정보 조회
            result = self.kiwoom_client.get_account_summary(user_id)
            
            if "error" in result:
                log_error(f"사용자 홈 요약 정보 조회 실패: {result['error']}")
                return {"error": result["error"]}
            
            # 응답 데이터 검증 및 변환
            summary_data = result["data"]
            
            # 필요한 필드가 모두 있는지 확인
            required_fields = ["Id", "id", "journal_count_year", "cumulative_investment_principal", 
                             "cumulative_profit_loss", "cumulative_profit_rate"]
            
            for field in required_fields:
                if field not in summary_data:
                    log_error(f"필수 필드 누락: {field}")
                    return {"error": f"필수 필드가 누락되었습니다: {field}"}
            
            log_info(f"사용자 홈 요약 정보 조회 성공: {user_id}")
            return {"data": summary_data}
            
        except Exception as e:
            log_error(f"사용자 홈 요약 정보 조회 중 오류: {e}")
            return {"error": "홈 요약 정보 조회 중 서버 오류가 발생했습니다"}
