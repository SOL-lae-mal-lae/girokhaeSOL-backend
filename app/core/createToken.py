from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jose import jwt
from app.core.config import settings

KST=ZoneInfo("Asia/Seoul")

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # data: 토큰에 넣을 유저 정보 등 (예: {"sub": "username"})
    # expires_delta: 토큰 유효 시간 (timedelta 객체)
    # return: JWT 문자열

    to_encode = data.copy()

    expire = datetime.now(tz=KST)+(
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt
