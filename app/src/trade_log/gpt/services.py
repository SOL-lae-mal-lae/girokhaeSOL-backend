from sqlalchemy.orm import Session
from typing import Dict, Any
from .repository import GPTAnalysisRepository
from .schemas import GPTAnalysisCreate, GPTAnalysisRequest
from fastapi import HTTPException
from app.logging import log_debug, log_info, log_error
# import openai  # 필요시 주석 해제
from app.core.config import settings

class GPTAnalysisService:
    """GPT 거래 로그 분석 서비스"""
    
    def __init__(self, db: Session):
        self.repository = GPTAnalysisRepository(db)
        self.db = db
        # OpenAI API 키 설정
        self.openai_api_key = settings.OPENAI_API_KEY
        # openai.api_key = self.openai_api_key  # 실제 사용시 주석 해제
    
    def analyze_trade_log(self, user_id: str, request: GPTAnalysisRequest) -> Dict[str, Any]:
        """거래 로그 GPT 분석"""
        try:
            trade_log_id = request.trade_log_id
            log_info(f"거래 로그 GPT 분석 시작: user_id={user_id}, trade_log_id={trade_log_id}")
            
            # 1. 이미 분석된 결과가 있는지 확인
            existing_analysis = self.repository.get_analysis_by_trade_log_id(trade_log_id)
            if existing_analysis:
                log_info(f"기존 분석 결과 반환: trade_log_id={trade_log_id}")
                return {
                    "message": "기존 분석 결과",
                    "data": existing_analysis
                }
            
            # 2. 거래 로그 데이터 조회 (trade_logs 테이블에서)
            trade_log_data = self._get_trade_log_data(trade_log_id, user_id)
            if not trade_log_data:
                raise HTTPException(status_code=404, detail="거래 로그를 찾을 수 없습니다.")
            
            # 3. GPT API 호출하여 분석
            analysis_result = self._call_gpt_for_analysis(trade_log_data)
            
            # 4. 분석 결과 저장
            analysis_data = GPTAnalysisCreate(
                trade_log_id=trade_log_id,
                result=analysis_result
            )
            analysis = self.repository.create_analysis(analysis_data)
            
            log_info(f"거래 로그 GPT 분석 완료: trade_log_id={trade_log_id}")
            
            return {
                "message": "분석 완료",
                "data": analysis
            }
            
        except HTTPException:
            raise
        except Exception as e:
            log_error(f"거래 로그 분석 실패: {e}")
            raise HTTPException(status_code=500, detail="거래 로그 분석 중 오류가 발생했습니다.")
    
    def get_analysis(self, user_id: str, trade_log_id: int) -> Dict[str, Any]:
        """저장된 GPT 분석 결과 조회"""
        try:
            log_debug(f"GPT 분석 결과 조회: user_id={user_id}, trade_log_id={trade_log_id}")
            
            # 거래 로그 소유권 확인
            trade_log_data = self._get_trade_log_data(trade_log_id, user_id)
            if not trade_log_data:
                raise HTTPException(status_code=404, detail="거래 로그를 찾을 수 없습니다.")
            
            analysis = self.repository.get_analysis_by_trade_log_id(trade_log_id)
            if not analysis:
                raise HTTPException(status_code=404, detail="분석 결과를 찾을 수 없습니다.")
            
            return {
                "message": "분석 결과 조회 완료",
                "data": analysis
            }
            
        except HTTPException:
            raise
        except Exception as e:
            log_error(f"분석 결과 조회 실패: {e}")
            raise HTTPException(status_code=400, detail="분석 결과 조회 중 오류가 발생했습니다.")
    
    def _get_trade_log_data(self, trade_log_id: int, user_id: str) -> Dict[str, Any]:
        """거래 로그 데이터 조회"""
        try:
            # trade_logs 테이블에서 데이터 조회
            from app.src.trade_log.model import TradeLog
            
            trade_log = self.db.query(TradeLog)\
                .filter(TradeLog.id == trade_log_id, TradeLog.user_id == user_id)\
                .first()
            
            if not trade_log:
                return None
            
            return {
                "id": trade_log.id,
                "user_id": trade_log.user_id,
                "stock_name": trade_log.stock_name,
                "stock_code": trade_log.stock_code,
                "trade_type": trade_log.trade_type,
                "quantity": trade_log.quantity,
                "price": trade_log.price,
                "total_amount": trade_log.total_amount,
                "trade_date": trade_log.trade_date,
                "profit_loss": trade_log.profit_loss,
                "notes": trade_log.notes
            }
            
        except Exception as e:
            log_error(f"거래 로그 데이터 조회 실패: {e}")
            return None
    
    def _call_gpt_for_analysis(self, trade_log_data: Dict[str, Any]) -> str:
        """GPT API 호출하여 거래 로그 분석"""
        try:
            # 거래 로그 데이터를 분석 요청 메시지로 변환
            prompt = f"""
다음 거래 로그를 분석해주세요:

종목명: {trade_log_data['stock_name']} ({trade_log_data['stock_code']})
거래유형: {trade_log_data['trade_type']}
수량: {trade_log_data['quantity']}주
거래가격: {trade_log_data['price']:,}원
총금액: {trade_log_data['total_amount']:,}원
거래일자: {trade_log_data['trade_date']}
손익: {trade_log_data['profit_loss']:,}원
메모: {trade_log_data.get('notes', '없음')}

이 거래에 대한 분석을 다음 관점에서 제공해주세요:
1. 거래 타이밍 분석
2. 손익 평가
3. 개선점 및 권장사항
4. 향후 투자 전략 제안
"""
            
            # TODO: 실제 OpenAI API 호출
            # response = openai.ChatCompletion.create(
            #     model="gpt-3.5-turbo",
            #     messages=[
            #         {"role": "system", "content": "당신은 전문적인 주식 투자 분석가입니다."},
            #         {"role": "user", "content": prompt}
            #     ],
            #     max_tokens=1000,
            #     temperature=0.7
            # )
            # return response.choices[0].message.content
            
            # 임시 분석 결과 (개발용)
            return f"""
## 거래 분석 결과

**종목**: {trade_log_data['stock_name']} ({trade_log_data['stock_code']})

### 1. 거래 타이밍 분석
- 거래 유형: {trade_log_data['trade_type']}
- 거래 일자: {trade_log_data['trade_date']}
- 시장 상황에 따른 타이밍 평가가 필요합니다.

### 2. 손익 평가
- 현재 손익: {trade_log_data['profit_loss']:,}원
- {'수익' if trade_log_data['profit_loss'] > 0 else '손실' if trade_log_data['profit_loss'] < 0 else '무손익'} 거래입니다.

### 3. 개선점 및 권장사항
- 거래량과 가격 분석을 통한 진입/청산 타이밍 개선
- 리스크 관리 전략 수립 필요

### 4. 향후 투자 전략
- 분산 투자를 통한 리스크 관리
- 장기적 관점에서의 투자 계획 수립

*이는 GPT 기반 분석 결과입니다. 투자 결정 시 추가적인 분석과 전문가 상담을 권장합니다.*
"""
            
        except Exception as e:
            log_error(f"GPT 분석 호출 실패: {e}")
            return "분석 중 오류가 발생했습니다. 다시 시도해주세요."
