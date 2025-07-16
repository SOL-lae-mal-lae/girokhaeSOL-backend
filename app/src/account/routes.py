from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from app.database.core import SessionLocal
from .services import AccountService
from .schemas import AccountCreate, AccountGetResponse, AccountCreateResponse, ErrorResponse

router = APIRouter()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get(
    "", 
    response_model=AccountGetResponse,
    responses={
        200: {"model": AccountGetResponse, "description": "계좌 목록 조회 성공"},
        400: {"model": ErrorResponse, "description": "잘못된 요청"},
        404: {"description": "사용자를 찾을 수 없음"},
        422: {"description": "유효성 검증 실패"}
    }
)
def get_accounts(
    request: Request,
    db: Session = Depends(get_db)
):
    """사용자의 계좌 목록 조회"""
    try:
        # request.state에서 user_id 가져오기
        user_id = request.state.user
        service = AccountService(db)
        return service.get_user_accounts(user_id)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="오류가 발생했습니다.")

@router.post(
    "",
    response_model=AccountCreateResponse,
    responses={
        200: {"model": AccountCreateResponse, "description": "계좌 생성 완료"},
        400: {"model": ErrorResponse, "description": "이미 존재하는 계좌번호입니다."},
        401: {"model": ErrorResponse, "description": "인증이 필요합니다."},
        422: {"description": "유효성 검증 실패"}
    }
)


def create_account(
    account_data: AccountCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """계좌 생성"""
    try:
        # request.state에서 user_id 가져오기
        user_id = request.state.user
        
        if not user_id:
            raise HTTPException(status_code=401, detail="인증이 필요합니다.")
        
        service = AccountService(db)
        return service.create_account(user_id, account_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail="오류가 발생했습니다.")

