from sqlalchemy.orm import Session
from typing import List, Dict, Any
from .repository import AccountRepository
from .schemas import AccountCreate, AccountGetResponse, AccountCreateResponse, ErrorResponse
from fastapi import HTTPException
from app.logging import log_debug, log_info, log_error  # logging.py 사용

class AccountService:
    def __init__(self, db: Session):
        self.repository = AccountRepository(db)
    
    def get_user_accounts(self, user_id: str) -> AccountGetResponse:  # str로 변경
        """사용자의 계좌 목록 조회"""
        try:
            log_debug(f"user_id = '{user_id}'")  # ✅ logging 사용
            accounts = self.repository.get_accounts_by_user_id(user_id)
            log_debug(f"found {len(accounts)} accounts")  # ✅ logging 사용
            
            # 응답 형식에 맞게 데이터 변환 - account_id도 포함
            account_data = [
                {
                    "account_id": account.id,
                    "account_number": account.account_number
                }
                for account in accounts
            ]
            
            log_debug(f"account_data = {account_data}")  # ✅ logging 사용
            
            return AccountListResponse(
                message="계좌 목록 불러오기 완료",
                data=account_data
            )
        except Exception as e:
            log_error(f"get_user_accounts 실패: {e}")  # ✅ logging 사용
            raise HTTPException(status_code=400, detail="오류가 발생했습니다.")
    
    def create_account(self, user_id: str, account_data: AccountCreate) -> AccountCreateResponse:
        """계좌 생성"""
        try:
            log_debug(f"계좌 생성 요청: user_id={user_id}, account_number={account_data.account_number}")
            
            # 계좌번호 중복 체크
            existing_account = self.repository.get_account_by_number(account_data.account_number)
            if existing_account:
                log_error(f"중복된 계좌번호 - {account_data.account_number}")
                raise HTTPException(status_code=400, detail="이미 존재하는 계좌번호입니다.")
            
            log_debug("계좌번호 중복 체크 완료")
            
            account = self.repository.create_account(user_id, account_data)
            if not account:
                log_error("계좌 생성 실패")
                raise HTTPException(status_code=400, detail="계좌 생성에 실패했습니다.")
            
            log_info(f"계좌 생성 완료 - ID: {account.id}, 계좌번호: {account.account_number}")
            
            return AccountCreateResponse(
                message="계좌 생성 완료",
                data={
                    "id": account.id,
                    "account_number": account.account_number
                }
            )
        except HTTPException:
            raise
        except Exception as e:
            log_error(f"create_account 실패 - {type(e).__name__}: {e}")
            import traceback
            log_error(f"TRACEBACK: {traceback.format_exc()}")
            raise HTTPException(status_code=400, detail="오류가 발생했습니다.")
    
   

