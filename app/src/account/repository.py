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
    

    def get_account_by_number(self, account_number: str) -> Optional[Account]:
        """계좌번호로 계좌 조회 (중복 체크용)"""
        try:
            log_debug(f"계좌번호 중복 체크: account_number={account_number}")
            account = self.db.query(Account).filter(Account.account_number == account_number).first()
            return account
        except Exception as e:
            log_error(f"계좌번호 조회 중 오류: {e}")
            return None

    
    def create_account(self, user_id: str, account_data: AccountCreate) -> Optional[Account]:
        """계좌 생성"""
        try:
            log_debug(f"계좌 생성 시작: user_id={user_id}, account_number={account_data['account_number']}")
            
            # user_id를 설정하여 Account 객체 생성
            account_dict = account_data
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
    
    
    
    def get_api_keys_of_primary_account(self, user_id: str) -> Optional[dict]:
        """대표 계좌의 API 키 조회"""
        try:
            log_debug(f"대표 계좌 API 키 조회 시작: user_id={user_id}")
            account = self.db.query(Account).filter(
                Account.user_id == user_id,
                Account.is_primary == True
            ).first()
            if account:
                log_debug(f"대표 계좌 API 키 조회 완료: account_id={account.id}")
                return {
                    "app_key": account.app_key,
                    "secret_key": account.secret_key
                }
            else:
                log_error(f"대표 계좌를 찾을 수 없음: user_id={user_id}")
                return None
        except Exception as e:
            log_error(f"대표 계좌 API 키 조회 중 오류: {e}")
            return None
    
    def get_primary_account_by_user_id(self, user_id: str) -> Optional[Account]:
        """사용자의 주계좌 조회. 없으면 첫 번째 계좌를 대표 계좌로 자동 지정"""
        try:
            log_debug(f"주계좌 조회 시작: user_id={user_id}")
            account = self.db.query(Account).filter(
                Account.user_id == user_id,
                Account.is_primary == True
            ).first()
            
            if account:
                log_debug(f"주계좌 조회 완료: account_id={account.id}")
                return account
            else:
                log_debug(f"주계좌를 찾을 수 없음: user_id={user_id}, 첫 번째 계좌를 대표 계좌로 지정 시도")
                # 첫 번째 계좌를 찾아서 대표 계좌로 지정
                first_account = self.db.query(Account).filter(Account.user_id == user_id).order_by(Account.id.asc()).first()
                if first_account:
                    first_account.is_primary = True
                    self.db.commit()
                    self.db.refresh(first_account)
                    log_info(f"첫 번째 계좌를 대표 계좌로 자동 지정: account_id={first_account.id}")
                    return first_account
                else:
                    log_debug(f"해당 유저의 계좌가 존재하지 않음: user_id={user_id}")
                    return None
        except Exception as e:
            log_error(f"주계좌 조회 중 오류: {e}")
            return None
    
    def clear_all_primary_accounts(self, user_id: str):
        """사용자의 모든 계좌에서 is_primary 제거"""
        try:
            self.db.query(Account).filter(Account.user_id == user_id).update(
                {"is_primary": False}
            )
            self.db.commit()
            log_debug(f"모든 주계좌 설정 해제 완료: user_id={user_id}")
        except Exception as e:
            log_error(f"주계좌 설정 해제 중 오류: {e}")
            self.db.rollback()
            raise
    
    def set_account_as_primary(self, account_id: int, user_id: str) -> Optional[Account]:
        """특정 계좌를 주계좌로 설정"""
        try:
            account = self.db.query(Account).filter(
                Account.id == account_id,
                Account.user_id == user_id
            ).first()
            
            if account:
                account.is_primary = True
                self.db.commit()
                self.db.refresh(account)
                log_info(f"주계좌 설정 완료: account_id={account_id}")
                return account
            else:
                log_error(f"계좌를 찾을 수 없음: account_id={account_id}, user_id={user_id}")
                return None
        except Exception as e:
            log_error(f"주계좌 설정 중 오류: {e}")
            self.db.rollback()
            raise


    def update_token(self, user_id: str, token: str, expires_dt: str):
        """사용자의 주계좌의 토큰과 만료일을 업데이트"""
        try:
            # user_id와 is_primary가 True인 주계좌 조회
            account = self.db.query(Account).filter(
                Account.user_id == user_id,
                Account.is_primary == True
            ).first()
            
            if not account:
                log_error(f"주계좌를 찾을 수 없음: user_id={user_id}")
                return None
            
            # 토큰과 만료일 업데이트
            account.token = token
            account.expires_dt = expires_dt
            
            # 변경 사항 DB에 반영
            self.db.commit()  # commit을 사용하여 변경사항을 저장
            self.db.refresh(account)  # 최신 상태로 갱신
            
            log_info(f"🔍 주계좌 토큰 업데이트 완료 - user_id: {user_id}, token: {token}, expires_dt: {expires_dt}")
            return account  # 변경된 계좌 객체 반환
            
        except Exception as e:
            log_error(f"🔍 주계좌 토큰 업데이트 중 오류 발생 - user_id={user_id}, 오류: {e}")
            self.db.rollback()  # 오류 발생 시 롤백
            raise
