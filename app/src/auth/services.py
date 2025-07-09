# Auth Services
# 인증 관련 비즈니스 로직을 처리합니다.

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from .repository import AuthRepository
from .schemas import UserCreate, UserResponse, Token


class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repo = auth_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = "your-secret-key"  # 환경변수로 관리 필요
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """비밀번호 해시화"""
        return self.pwd_context.hash(password)

    def authenticate_user(self, email: str, password: str):
        """사용자 인증"""
        user = self.auth_repo.get_user_by_email(email)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """액세스 토큰 생성"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def register_user(self, user_data: UserCreate) -> UserResponse:
        """사용자 등록"""
        hashed_password = self.get_password_hash(user_data.password)
        user_dict = user_data.dict()
        user_dict.pop("password")
        user_dict["hashed_password"] = hashed_password
        
        user = self.auth_repo.create_user(user_dict)
        return UserResponse.from_orm(user)

    def login_for_access_token(self, email: str, password: str) -> Token:
        """로그인 및 토큰 발급"""
        user = self.authenticate_user(email, password)
        if not user:
            raise ValueError("Invalid credentials")
        
        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
