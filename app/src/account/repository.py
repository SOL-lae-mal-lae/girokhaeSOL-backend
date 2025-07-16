from sqlalchemy.orm import Session
from typing import List, Optional
from .model import Account
from .schemas import AccountCreate
from app.src.common_models.users.model import User
from app.logging import log_debug, log_info, log_error

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_accounts_by_user_id(self, user_id: str) -> List[Account]:
        """사용자 ID로 계좌 목록 조회"""
        try:
            log_debug(f"사용자별 계좌 조회 시작: user_id={user_id}")
            accounts = self.db.query(Account).filter(Account.user_id == user_id).all()
            log_debug(f"사용자별 계좌 조회 완료: {len(accounts)}개")
            return accounts
        except Exception as e:
            log_error(f"사용자별 계좌 조회 중 오류: {e}")
            return []

    
    def create_account(self, user_id: str, account_data: AccountCreate) -> Optional[Account]:
        """계좌 생성"""
        try:
            log_debug(f"계좌 생성 시작: user_id={user_id}, account_number={account_data.account_number}")
            
            # 중복 계좌번호 확인
            existing = self.get_account_by_number(account_data.account_number)
            if existing:
                log_error(f"이미 존재하는 계좌번호: {account_data.account_number}")
                return None
            
            # user_id를 설정하여 Account 객체 생성
            account_dict = account_data.dict()
            account_dict['user_id'] = user_id
            
            account = Account(**account_dict)
            self.db.add(account)
            self.db.commit()
            self.db.refresh(account)
            
            log_info(f"계좌 생성 완료: ID={account.id}, 계좌번호={account.account_number}")
            return account
        except Exception as e:
            log_error(f"계좌 생성 중 오류: {e}")
            self.db.rollback()
            return None
    
    
    
    def get_api_keys_by_user_id(self, user_id: str) -> Optional[dict]:
        """사용자 ID로 API 키 조회"""
        try:
            log_debug(f"API 키 조회 시작: user_id={user_id}")
            account = self.db.query(Account).filter(Account.user_id == user_id).first()
            
            if account:
                log_debug(f"API 키 조회 완료: user_id={user_id}")
                return {
                    "app_key": account.app_key,
                    "secret_key": account.secret_key
                }
            else:
                log_error(f"사용자의 계좌를 찾을 수 없음: user_id={user_id}")
                return None
        except Exception as e:
            log_error(f"API 키 조회 중 오류: {e}")
            return None
    
  

