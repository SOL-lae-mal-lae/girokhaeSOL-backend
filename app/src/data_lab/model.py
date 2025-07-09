# Data Lab Model
# 데이터 분석 관련 데이터베이스 모델을 정의합니다.

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.core import Base
from datetime import datetime


class DataAnalysis(Base):
    """데이터 분석 결과 모델"""
    __tablename__ = "data_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    analysis_type = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    result_data = Column(Text)  # JSON 형태로 저장
    status = Column(String(50), default="pending")  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    user = relationship("User", back_populates="data_analyses")


class DataSource(Base):
    """데이터 소스 모델"""
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    source_type = Column(String(100), nullable=False)  # csv, api, database
    file_path = Column(String(500))
    api_endpoint = Column(String(500))
    connection_string = Column(String(500))
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
