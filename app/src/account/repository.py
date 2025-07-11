from sqlalchemy.orm import Session
from typing import List, Optional
from .model import Account
from .schemas import AccountCreate, AccountUpdate
from app.src.common_models.users import User
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

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        """계좌 ID로 계좌 조회"""
        try:
            log_debug(f"계좌 ID 조회 시작: {account_id}")
            account = self.db.query(Account).filter(Account.id == account_id).first()
            if account:
                log_debug(f"계좌 조회 성공: ID={account_id}")
            else:
                log_debug(f"계좌를 찾을 수 없음: ID={account_id}")
            return account
        except Exception as e:
            log_error(f"계좌 ID 조회 중 오류: {e}")
            return None
    
    def get_account_by_number(self, account_number: str) -> Optional[Account]:
        """계좌번호로 계좌 조회"""
        try:
            log_debug(f"계좌번호 조회 시작: {account_number}")
            account = self.db.query(Account).filter(Account.account_number == account_number).first()
            if account:
                log_debug(f"계좌 조회 성공: 계좌번호={account_number}")
            else:
                log_debug(f"계좌를 찾을 수 없음: 계좌번호={account_number}")
            return account
        except Exception as e:
            log_error(f"계좌번호 조회 중 오류: {e}")
            return None

    def get_all_accounts(self, skip: int = 0, limit: int = 100) -> List[Account]:
        """전체 계좌 목록 조회"""
        try:
            log_debug(f"전체 계좌 조회 시작: skip={skip}, limit={limit}")
            accounts = self.db.query(Account).offset(skip).limit(limit).all()
            log_debug(f"전체 계좌 조회 완료: {len(accounts)}개")
            return accounts
        except Exception as e:
            log_error(f"전체 계좌 조회 중 오류: {e}")
            return []
    
    def create_account(self, account_data: AccountCreate) -> Optional[Account]:
        """계좌 생성"""
        try:
            log_debug(f"계좌 생성 시작: user_id={account_data.user_id}, account_number={account_data.account_number}")
            
            # 중복 계좌번호 확인
            existing = self.get_account_by_number(account_data.account_number)
            if existing:
                log_error(f"이미 존재하는 계좌번호: {account_data.account_number}")
                return None
            
            account = Account(**account_data.dict())
            self.db.add(account)
            self.db.commit()
            self.db.refresh(account)
            
            log_info(f"계좌 생성 완료: ID={account.id}, 계좌번호={account.account_number}")
            return account
        except Exception as e:
            log_error(f"계좌 생성 중 오류: {e}")
            self.db.rollback()
            return None
    
    def update_account(self, account_id: int, update_data: AccountUpdate) -> Optional[Account]:
        """계좌 수정"""
        try:
            log_debug(f"계좌 수정 시작: ID={account_id}")
            account = self.get_account_by_id(account_id)
            
            if not account:
                log_error(f"수정할 계좌를 찾을 수 없음: ID={account_id}")
                return None
            
            # 값이 있는 필드만 업데이트
            update_dict = update_data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                if hasattr(account, field):
                    setattr(account, field, value)
            
            self.db.commit()
            self.db.refresh(account)
            
            log_info(f"계좌 수정 완료: ID={account.id}")
            return account
        except Exception as e:
            log_error(f"계좌 수정 중 오류: {e}")
            self.db.rollback()
            return None
    
    def delete_account(self, account_id: int) -> bool:
        """계좌 삭제"""
        try:
            log_debug(f"계좌 삭제 시작: ID={account_id}")
            account = self.get_account_by_id(account_id)
            
            if not account:
                log_error(f"삭제할 계좌를 찾을 수 없음: ID={account_id}")
                return False
            
            self.db.delete(account)
            self.db.commit()
            
            log_info(f"계좌 삭제 완료: ID={account_id}")
            return True
        except Exception as e:
            log_error(f"계좌 삭제 중 오류: {e}")
            self.db.rollback()
            return False
    
    def get_count(self) -> int:
        """전체 계좌 개수 조회"""
        try:
            count = self.db.query(Account).count()
            log_debug(f"전체 계좌 개수: {count}")
            return count
        except Exception as e:
            log_error(f"계좌 개수 조회 중 오류: {e}")
            return 0

