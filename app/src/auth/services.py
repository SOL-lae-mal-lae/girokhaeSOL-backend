from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import timedelta
from app.src.auth.repository import check_user_by_user_id
from app.core.createToken import create_access_token
from app.core.config import settings
import requests
from typing import Optional
from app.logging import log_info, log_error, log_debug



def login_and_issue_token(user_id: str, db: Session) -> str:
    user = check_user_by_user_id(db, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="존재하지 않는 사용자입니다.")

    token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return token


class KiwoomAuthService:
    """키움 API 인증 서비스 - 전역 토큰 관리"""
    
    BASE_URL = "https://mockapi.kiwoom.com"
    APP_KEY = "ck2aFnUqE5w2if5WX2gYNXUlw9mMsw4OQHUMy4mSYuw"
    SECRET_KEY = "B781rDYU855V4uy7ljdF-q-3zhA4j47W-sBwMl85_jQ"
    
    _token: Optional[str] = None  # 클래스 변수로 토큰 저장 (싱글톤)
    
    @classmethod
    def authenticate(cls) -> Optional[str]:
        """키움 API 인증 후 토큰 발급"""
        try:
            log_info("🔐 키움 API 인증 시작")
            
            url = f"{cls.BASE_URL}/oauth2/token"
            headers = {
                'Content-Type': 'application/json;charset=UTF-8',
            }
            data = {
                'grant_type': 'client_credentials',
                'appkey': cls.APP_KEY,
                'secretkey': cls.SECRET_KEY,
            }
            
            log_debug(f"🌐 인증 요청 URL: {url}")
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                res_data = response.json()
                cls._token = res_data.get('token')
                log_info(f"✅ 키움 API 인증 성공 - 토큰 길이: {len(cls._token) if cls._token else 0}")
                return cls._token
            else:
                log_error(f"❌ 키움 API 인증 실패: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            log_error(f"❌ 키움 API 인증 중 오류: {type(e).__name__}: {e}")
            return None
    
    @classmethod
    def get_token(cls) -> Optional[str]:
        """토큰 반환 (없으면 자동 인증)"""
        if not cls._token:
            log_debug("🔄 토큰 없음 - 자동 인증 시도")
            cls.authenticate()
        
        return cls._token
    
    @classmethod
    def clear_token(cls):
        """토큰 초기화 (인증 실패 시 사용)"""
        log_debug("🗑️ 키움 API 토큰 초기화")
        cls._token = None
