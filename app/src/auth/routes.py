from fastapi import APIRouter, Depends
from datetime import timedelta
from app.core.config import settings
from app.src.auth.schemas import ClerkTokenRequest
from app.database.core import SessionLocal
from app.src.auth.services import login_and_issue_token
from sqlalchemy.orm import Session

router = APIRouter()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def auth_token(
    req: ClerkTokenRequest,
    db: Session = Depends(get_db)
):
    token = login_and_issue_token(req.userId, db)

    return {"token": token}

