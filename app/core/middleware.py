from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.clerk import sdk
from app.logging import log_debug
from clerk_backend_api.security.types import AuthenticateRequestOptions

EXCLUDE_PATHS = ["/docs",
                 "/openapi.json",
                 "/favicon.ico",
                 "/api/v1/auth",
                 "/api/v1/trade-logs/chart",
                 "/api/v1/trade-logs/search",
                 "/api/v1/trade-logs/detail/gpt",
                 "/api/v1/trade-logs/statement/",
                 "/api/v1/recent-post",
                 "/api/v1/community",
                 "/api/v1/financial-statements",
                 "/api/v1/home/summary"
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
# class JWTMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # 인증 제외 경로라면 건너뛰기
#         if any(request.url.path.startswith(path) for path in EXCLUDE_PATHS):
#             return await call_next(request)


#         auth_header = request.headers.get("Authorization")
#         if not auth_header or not auth_header.startswith("Bearer "):
#             return JSONResponse(status_code=401, content={
#                 "message": "토큰이 존재하지 않습니다.",
#                 "data": None
#             })

#         token = auth_header.split(" ")[1]

#         try:
#             payload = jwt.decode(
#                 token,
#                 settings.JWT_SECRET_KEY,
#                 algorithms=[settings.JWT_ALGORITHM]
#             )
#             request.state.user = payload["sub"]
#         except JWTError:
#             return JSONResponse(status_code=402, content={
#                 "message": "유효하지 않은 토큰입니다.",
#                 "data": None
#             })

#         return await call_next(request)
