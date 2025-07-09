# Account Repository
# 데이터베이스 접근 로직을 처리합니다.

from sqlalchemy.orm import Session
from typing import List, Optional
from .model import Account


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        """ID로 계좌 조회"""
        return self.db.query(Account).filter(Account.id == account_id).first()

    def get_accounts_by_user_id(self, user_id: int) -> List[Account]:
        """사용자 ID로 계좌 목록 조회"""
        return self.db.query(Account).filter(Account.user_id == user_id).all()

    def create_account(self, account_data: dict) -> Account:
        """새 계좌 생성"""
        account = Account(**account_data)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update_account(self, account_id: int, update_data: dict) -> Optional[Account]:
        """계좌 정보 업데이트"""
        account = self.get_account_by_id(account_id)
        if account:
            for key, value in update_data.items():
                setattr(account, key, value)
            self.db.commit()
            self.db.refresh(account)
        return account

    def delete_account(self, account_id: int) -> bool:
        """계좌 삭제"""
        account = self.get_account_by_id(account_id)
        if account:
            self.db.delete(account)
            self.db.commit()
            return True
        return False
