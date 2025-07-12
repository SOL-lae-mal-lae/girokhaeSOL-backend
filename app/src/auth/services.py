from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import timedelta
from app.src.auth.repository import check_user_by_user_id
from app.core.createToken import create_access_token
from app.core.config import settings

def login_and_issue_token(user_id: str, db: Session) -> str:
    user = check_user_by_user_id(db, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="존재하지 않는 사용자입니다.")

    token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return token
