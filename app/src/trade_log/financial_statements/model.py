from sqlalchemy import Column, Integer, String, Float, BigInteger
from app.database.core import Base
from app.src.common_models.users.model import User  # 기존 User 모델 import

# User 클래스는 이미 common_models에 정의되어 있으므로 제거

class FinancialStatement(Base):
    """
    국내주식 재무제표 모델
    간소화된 재무 데이터를 저장
    """
    __tablename__ = "financial_statements"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # 기본 정보
    stock_code = Column(String(6), nullable=False, unique=True, index=True)  # 종목코드 (6자리)
    
    # 주요 재무비율
    pbr = Column(Float, nullable=True)              # PBR (주가순자산비율)
    per = Column(Float, nullable=True)              # PER (주가수익비율)
    debt_ratio = Column(Float, nullable=True)       # 부채비율
    
    # 재무제표 주요 항목 (단위: 원)
    revenue = Column(BigInteger, nullable=True)           # 매출액
    operating_income = Column(BigInteger, nullable=True)  # 영업이익
    net_income = Column(BigInteger, nullable=True)        # 순이익
    
    # 주당 지표
    eps = Column(Float, nullable=True)              # EPS (주당순이익)
    
   