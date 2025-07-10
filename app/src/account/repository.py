from sqlalchemy.orm import Session
from typing import List, Optional
from .model import Account
from .schemas import AccountCreate, AccountUpdate

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_accounts_by_user_id(self, user_id: str) -> List[Account]:  # str로 변경
        """사용자 ID로 계좌 목록 조회"""
        return self.db.query(Account).filter(Account.user_id == user_id).all()
    
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        """계좌 ID로 계좌 조회"""
        return self.db.query(Account).filter(Account.id == account_id).first()
    
    def get_account_by_number(self, account_number: str) -> Optional[Account]:
        """계좌번호로 계좌 조회"""
        return self.db.query(Account).filter(Account.account_number == account_number).first()
    
    def create_account(self, account_data: AccountCreate) -> Account:
        """계좌 생성"""
        account = Account(**account_data.dict())
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account


        return False
