from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from  app.core.clerk import sdk
from clerk_backend_api.security.types import AuthenticateRequestOptions
from app.core.oauth_token import get_oauth_token
from app.database.core import get_db
from app.src.account.services import AccountService
from app.core.oauth_token import get_oauth_token
from app.logging import log_debug, log_info
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

EXCLUDE_PATHS = ["/docs",
                 "/openapi.json",
                 "/favicon.ico",
                 "/api/v1/auth",
                #  "/api/v1/trade-logs",
                #  "/api/v1/trade-logs/ai",
                 "/api/v1/trade-logs/search",
                 "/api/v1/trade-logs/statement/",
                 "/api/v1/recent-post",
                 # "/api/v1/community",
                 "/api/v1/financial-statements",
                 "/api/v1/stock-search",
                 ]

class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        # OPTIONS 요청 (CORS preflight)은 인증 제외
        if request.method == "OPTIONS":
            return await call_next(request)

        # 인증 제외 경로라면 건너뛰기
        if any([request.url.path.startswith(path) for path in EXCLUDE_PATHS]):
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


class KiwoomOAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
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

            # ✅ 데이터베이스에서 is_primary=1인 계좌의 토큰 조회
            try:
                db = next(get_db())
                account_service = AccountService(db)
                primary_account = account_service.get_primary_account(user_id)
                log_debug(primary_account.token)
                log_debug(primary_account.expires_dt)
                # 토큰 만료일 확인 및 갱신
                if primary_account.token and primary_account.expires_dt < datetime.now():
                    logger.debug(f"토큰 만료됨. 새로운 토큰을 발급합니다.")
                    token_data = await get_oauth_token(user_id)
                    if not token_data:
                        logger.error(f"OAuth 토큰 발급 실패: user_id={user_id}")
                        return await call_next(request)

                    # 새로운 토큰과 만료일로 업데이트
                    primary_account.token = token_data.token                    
                    primary_account.expires_dt = token_data.expires_dt
                    db.commit()
                    db.refresh(primary_account)
                    logger.debug(f"새로운 토큰이 DB에 업데이트되었습니다: {primary_account.token}")

                # 만약 토큰이 없으면 새로 발급
                elif not primary_account.token:
                    logger.debug(f"대표 계좌에 토큰이 없습니다. 새로 발급합니다.")
                    token_data = await get_oauth_token(user_id)
                    if not token_data:
                        logger.error(f"OAuth 토큰 발급 실패: user_id={user_id}")
                        return await call_next(request)

                    primary_account.token = token_data["token"]
                    primary_account.expires_dt = token_data["expires_dt"]
                    db.commit()
                    db.refresh(primary_account)
                    logger.debug(f"새로운 토큰이 DB에 저장되었습니다: {primary_account.token}")

                # 토큰 설정
                request.state.token = primary_account.token  # 요청에 토큰을 설정
                logger.debug(f"Middleware token set: token={self.token}, expires_dt={self.expires_dt}")

            except Exception as e:
                logger.error(f"Failed to fetch or update token for user {user_id}: {e}")
                return await call_next(request)

        response = await call_next(request)
        return response