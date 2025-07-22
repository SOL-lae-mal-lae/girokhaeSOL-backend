from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from  app.core.clerk import sdk
from clerk_backend_api.security.types import AuthenticateRequestOptions
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
                # OAuth 토큰 없이도 접근 가능하도록 설정
                request.state.token = None
                return await call_next(request)

            # ✅ 데이터베이스에서 is_primary=1인 계좌의 토큰 조회
            try:
                db = next(get_db())
                account_service = AccountService(db)
                primary_account = account_service.get_primary_account(user_id)

            
                if not primary_account.token:
                    logger.debug(f"No token found for primary account. Fetching new token for user {user_id}.")
                    token_data = await get_oauth_token(user_id)
                    if not token_data:
                        logger.error(f"Failed to retrieve OAuth token for user {user_id}.")
                        return await call_next(request)  # 토큰 없이도 진행

                    logger.debug(f"Token data received: {token_data}")
                    primary_account.token = token_data["token"]
                    primary_account.expires_dt = token_data["expires_dt"]
                    logger.debug(f"Updating primary_account with token: {primary_account.token}, expires_dt: {primary_account.expires_dt}")
                    db.commit()
                    db.refresh(primary_account)
                    logger.debug(f"Primary account after update: token={primary_account.token}, expires_dt={primary_account.expires_dt}")

                # 토큰 설정
                request.state.token = primary_account.token
                self.expires_dt = primary_account.expires_dt
                logger.debug(f"Middleware token set: token={self.token}, expires_dt={self.expires_dt}")

            except Exception as e:
                logger.error(f"Failed to fetch or update token for user {user_id}: {e}")
                return await call_next(request)  # 토큰 없이도 진행


        response = await call_next(request)
        return response