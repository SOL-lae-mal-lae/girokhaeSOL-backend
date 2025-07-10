from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.database.core import SessionLocal
from .services import AccountService
from .schemas import AccountCreate, AccountUpdate, AccountListResponse, ErrorResponse

router = APIRouter()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT 토큰에서 user_id 추출하는 의존성 (임시로 "user123"으로 고정)
def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:  # str로 변경
    # TODO: JWT 토큰 검증 로직 추가
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="인증이 필요합니다.")
    
    # 임시로 user_id = "user123" 반환 (실제로는 JWT에서 추출)
    return "user123"

@router.get(
    "/accounts", 
    response_model=AccountListResponse,
    responses={
        200: {"model": AccountListResponse, "description": "계좌 목록 조회 성공"},
        400: {"model": ErrorResponse, "description": "잘못된 요청"},
        404: {"description": "사용자를 찾을 수 없음"},
        422: {"description": "유효성 검증 실패"}
    }
)
def get_accounts(
    userId: str,  # query parameter로 변경 (camelCase)
    db: Session = Depends(get_db)
):
    """사용자의 계좌 목록 조회"""
    try:
        # 공백 제거
        user_id = userId.strip()
        service = AccountService(db)
        return service.get_user_accounts(user_id)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="오류가 발생했습니다.")

@router.post(
    "/accounts",
    responses={
        200: {"description": "계좌 생성 성공"},
        400: {"description": "계좌번호 중복 또는 일반 오류"},
        422: {"description": "유효성 검증 실패"}
    }
)
def create_account(
    account_data: AccountCreate,
    userId: str,  # query parameter로 변경
    db: Session = Depends(get_db)
):
    """계좌 생성"""
    try:
        # user_id를 query parameter에서 가져와서 설정
        account_data.user_id = userId.strip()
        service = AccountService(db)
        return service.create_account(account_data)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="오류가 발생했습니다.")

@router.put("/accounts")
def update_account(
    account_data: AccountUpdate,
    accountId: int,  # query parameter로 변경
    db: Session = Depends(get_db)
):
    """계좌 업데이트"""
    try:
        service = AccountService(db)
        return service.update_account(accountId, account_data)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="오류가 발생했습니다.")

@router.delete("/accounts")
def delete_account(
    accountId: int,  # query parameter로 변경
    db: Session = Depends(get_db)
):
    """계좌 삭제"""
    try:
        service = AccountService(db)
        return service.delete_account(accountId)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="오류가 발생했습니다.")
