from pydantic import BaseModel, Field


# API 명세에 맞는 홈 요약 응답 모델 
class HomeSummaryData(BaseModel):
    """홈 요약 정보 데이터 모델"""
   
    id: int = Field(..., description="내부 ID")
    journal_count_year: int = Field(..., description="최근 1년간 매매일지 작성 개수")
    cumulative_investment_principal: int = Field(..., description="누적 투자 원금")
    cumulative_profit_loss: int = Field(..., description="누적 투자 손익")
    cumulative_profit_rate: float = Field(..., description="누적 손익률 (소수)")


class HomeSummaryResponse(BaseModel):
    """홈 요약 정보 전체 응답 모델"""
    message: str = Field(..., description="응답 메시지")
    data: HomeSummaryData = Field(..., description="요약 정보 데이터")
