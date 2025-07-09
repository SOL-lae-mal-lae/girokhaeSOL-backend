# Data Lab Repository
# 데이터 분석 관련 데이터베이스 접근 로직을 처리합니다.

from sqlalchemy.orm import Session
from typing import List, Optional
from .model import DataAnalysis, DataSource


class DataLabRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_analysis_by_id(self, analysis_id: int) -> Optional[DataAnalysis]:
        """ID로 분석 결과 조회"""
        return self.db.query(DataAnalysis).filter(DataAnalysis.id == analysis_id).first()

    def get_analyses_by_user_id(self, user_id: int) -> List[DataAnalysis]:
        """사용자별 분석 결과 조회"""
        return self.db.query(DataAnalysis).filter(DataAnalysis.user_id == user_id).all()

    def create_analysis(self, analysis_data: dict) -> DataAnalysis:
        """새 분석 결과 생성"""
        analysis = DataAnalysis(**analysis_data)
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def update_analysis(self, analysis_id: int, update_data: dict) -> Optional[DataAnalysis]:
        """분석 결과 업데이트"""
        analysis = self.get_analysis_by_id(analysis_id)
        if analysis:
            for key, value in update_data.items():
                setattr(analysis, key, value)
            self.db.commit()
            self.db.refresh(analysis)
        return analysis

    def get_data_sources(self) -> List[DataSource]:
        """활성화된 데이터 소스 목록 조회"""
        return self.db.query(DataSource).filter(DataSource.is_active == 1).all()

    def create_data_source(self, source_data: dict) -> DataSource:
        """새 데이터 소스 생성"""
        source = DataSource(**source_data)
        self.db.add(source)
        self.db.commit()
        self.db.refresh(source)
        return source
