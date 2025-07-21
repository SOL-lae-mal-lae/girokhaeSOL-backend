"""
계좌별 토큰 관리 미들웨어
사용자가 계좌를 변경할 때 자동으로 해당 계좌의 OAuth 토큰을 사용하도록 처리
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.database.core import get_db
from app.src.account.services import AccountService
from app.core.oauth_token import get_oauth_token
import logging


logger = logging.getLogger(__name__)

class AccountTokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        
    async def dispatch(self, request: Request, call_next):
        # OAuth 토큰이 필요한 API 경로들
        token_required_paths = [
            "/api/v1/home/",
            "/api/v1/trade-logs/",
            "/api/v1/data-lab/",
            "/api/v1/stock-search/"
        ]
        
        # 현재 요청이 토큰이 필요한 경로인지 확인
        if any(request.url.path.startswith(path) for path in token_required_paths):
            try:
                # 사용자 정보 가져오기
                user_id = request.state.user  # user를 user_id로 간주
                if not user_id:
                    return await call_next(request)

                # 현재 활성 계좌의 OAuth 토큰 확인 및 갱신
                db = next(get_db())
                account_service = AccountService(db)

                # 사용자의 주계좌(활성 계좌) 가져오기
                primary_account = account_service.get_primary_account(user_id)
                if not primary_account:
                    logger.warning(f"No primary account found for user {user_id}")
                    return await call_next(request)
                
                # OAuth 토큰 확인 및 갱신
                try:
                    # get_oauth_token 함수 호출
                    token_data = await get_oauth_token(user_id)
                    if not token_data:
                        raise HTTPException(
                            status_code=401,
                            detail="Failed to retrieve OAuth token"
                        )

                    # request state에 토큰 정보 저장
                    request.state.oauth_token = token_data["token"]
                    request.state.active_account = primary_account

                except Exception as e:
                    logger.error(f"Failed to get valid token for account {primary_account.account_number}: {e}")
                    # 토큰 갱신 실패시 에러 응답
                    raise HTTPException(
                        status_code=401,
                        detail=f"OAuth token refresh failed for account {primary_account.account_number}"
                    )
                    
            except Exception as e:
                logger.error(f"AccountTokenMiddleware error: {e}")
                # 미들웨어 에러가 전체 요청을 막지 않도록 처리
                pass
        
        response = await call_next(request)
        return response
