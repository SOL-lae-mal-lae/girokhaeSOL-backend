from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from  app.core.clerk import sdk
from clerk_backend_api.security.types import AuthenticateRequestOptions
from datetime import datetime
from app.core.oauth_token import get_oauth_token

EXCLUDE_PATHS = ["/docs",
                 "/openapi.json",
                 "/favicon.ico",
                 "/api/v1/auth",
                 "/api/v1/trade-logs/chart",
                 "/api/v1/trade-logs/search",
                 "/api/v1/trade-logs/statement/",
                 "/api/v1/recent-post",
                 "/api/v1/community",
                 "/api/v1/financial-statements",
                 "/api/v1/home/summary",
                 ]

class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        # 인증 제외 경로라면 건너뛰기
        if any(request.url.path.startswith(path) for path in EXCLUDE_PATHS):
            return await call_next(request)
    
        request_state = sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=[settings.CLERK_KEY_URL]
            )
        )
        
        request.state.user = request_state.payload.get('sub')
        return await call_next(request)

KIWOOM_API_USE_PATH = [
    "/api/v1/home/summary",  
    "/api/v1/accounts",
    "/api/v1/trade-logs/chart",
    '/api/v1/trade-logs/transaction',
]

class KiwoomOAuthMiddleware(BaseHTTPMiddleware):
    expires_dt= ""
    token=''

    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in KIWOOM_API_USE_PATH):
            # 사용자 ID 가져오기 (JWT 미들웨어에서 설정됨)
            user_id = getattr(request.state, 'user', None)
            
            if not user_id:
                # 사용자 ID가 없으면 인증 오류
                request.state.token = None
                return await call_next(request)
            
            if not self.token or datetime.strptime(self.expires_dt, '%Y%m%d%H%M%S') < datetime.now():
                res = await get_oauth_token(user_id)
                if res:
                    token, expires_dt = res.get('token'), res.get('expires_dt')
                    self.token = token
                    self.expires_dt = expires_dt
                    request.state.token = self.token
                else:
                    request.state.token = None
            else:
                request.state.token = self.token

        return await call_next(request)