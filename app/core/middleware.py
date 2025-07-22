from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from  app.core.clerk import sdk
from clerk_backend_api.security.types import AuthenticateRequestOptions
from datetime import datetime
from app.core.oauth_token import get_oauth_token
from app.database.core import get_db
from app.src.account.services import AccountService
from app.core.oauth_token import get_oauth_token
import logging

logger = logging.getLogger(__name__)

EXCLUDE_PATHS = ["/docs",
                 "/openapi.json",
                 "/favicon.ico",
                 "/api/v1/auth",
                 "/api/v1/trade-logs/search",
                 "/api/v1/trade-logs/statement/",
                 "/api/v1/recent-post",
                 "/api/v1/community",
                 "/api/v1/financial-statements",
                 ]

class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        # OPTIONS 요청 (CORS preflight)은 인증 제외
        if request.method == "OPTIONS":
            return await call_next(request)
            
        # 인증 제외 경로라면 건너뛰기
        if any(request.url.path.startswith(path) for path in EXCLUDE_PATHS):
            return await call_next(request)
    
        request_state = sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=[settings.CLERK_KEY_URL]
            )
        )
        if not request_state or not getattr(request_state, 'payload', None):
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=401, content={"detail": "인증 정보가 없습니다."})

        request.state.user = request_state.payload.get('sub')
        return await call_next(request)

KIWOOM_API_USE_PATH = [
    "/api/v1/home/summary",  
    "/api/v1/accounts",
    "/api/v1/trade-logs/chart",
    '/api/v1/trade-logs/transaction',
   
]

class KiwoomOAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.token = ""
        self.expires_dt = ""

    async def dispatch(self, request: Request, call_next):
        # OAuth 토큰이 필요한 경로들
        token_required_paths = [
            "/api/v1/home/",
            "/api/v1/trade-logs/",
            "/api/v1/data-lab/",
            "/api/v1/stock-search/",
            "/api/v1/home/summary",
            "/api/v1/accounts",
            "/api/v1/trade-logs/chart",
            "/api/v1/trade-logs/transaction",
        ]

        # 경로가 토큰을 요구하는지 확인
        if any(request.url.path.startswith(path) for path in token_required_paths) or "/set-primary" in request.url.path:
            user_id = getattr(request.state, 'user', None)
            if not user_id:
                request.state.token = None
                return await call_next(request)

            # ✅ 대표 계좌 변경 시엔 무조건 재발급
            force_refresh = "/set-primary" in request.url.path

            # 토큰 갱신 여부 판단
            if force_refresh or not self.token or datetime.strptime(self.expires_dt, '%Y%m%d%H%M%S') < datetime.now():
                try:
                    # get_oauth_token 함수 호출
                    token_data = await get_oauth_token(user_id)
                    if not token_data:
                        raise HTTPException(status_code=401, detail="Failed to retrieve OAuth token")

                    # 토큰 갱신 후 request state에 저장
                    self.token = token_data["token"]
                    self.expires_dt = token_data["expires_dt"]
                    request.state.token = self.token

                    # 활성 계좌 정보도 함께 저장
                    db = next(get_db())
                    account_service = AccountService(db)
                    primary_account = account_service.get_primary_account(user_id)
                    if not primary_account:
                        logger.warning(f"No primary account found for user {user_id}")
                        return await call_next(request)

                    request.state.active_account = primary_account

                except Exception as e:
                    logger.error(f"OAuth token refresh failed for user {user_id}: {e}")
                    raise HTTPException(status_code=401, detail="OAuth token refresh failed")

            else:
                # 만약 토큰이 유효하다면 기존 토큰 사용
                request.state.token = self.token

        # 최종 응답 반환
        response = await call_next(request)
        return response