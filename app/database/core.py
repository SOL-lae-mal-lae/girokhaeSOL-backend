
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# DB URL 구성
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Engine 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,           # SQL 로그 찍히게 하려면 True
    pool_pre_ping=True,  # DB 연결 끊김 방지
)

# Session 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base 클래스 (모델 정의 시 상속)
Base = declarative_base()
