from pydantic import BaseModel
from typing import List, Optional


# Pydantic 모델 설정
class Config:
        from_attributes = True  # ORM 모델을 Pydantic 모델로 변환 가능하게 설정


# 계좌 스키마의 기본 클래스
# 모든 계좌 관련 스키마의 기본이 되는 클래스입니다.
class AccountBase(BaseModel):
    account_number: str  # 계좌 번호

# 계좌 생성을 위한 스키마
# AccountBase를 상속받아 계좌 생성에 필요한 추가 필드를 정의합니다.
class AccountCreate(AccountBase):
    app_key: str        # API 앱 키
    secret_key: str     # API 시크릿 키


# 계좌 생성 응답 스키마
# 계좌 생성 API의 응답 형식을 정의합니다.
class AccountCreateResponse(BaseModel):
    message: str    # 응답 메시지
    data: dict     # 응답 데이터


# 에러 응답 스키마
# API 에러 발생시 사용되는 응답 형식입니다.
class ErrorResponse(BaseModel):
    message: str = "오류가 발생했습니다."  # 기본 에러 메시지

# 계좌 조회 응답 스키마
# 계좌 정보 조회 API의 응답 형식을 정의합니다.
class AccountListResponse(BaseModel):
    account_number: str        # 계좌 번호
    account_id: int             # 계좌 ID
    


# 다수의 계좌 조회 응답 스키마
# 여러 계좌 정보를 조회할 때 사용하는 응답 형식입니다.
class AccountGetResponse(BaseModel):
    message: str                    # 응답 메시지
    data: List[AccountListResponse]     # 계좌 목록

