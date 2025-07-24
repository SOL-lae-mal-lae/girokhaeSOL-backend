from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.core import get_db
from app.src.my_page.user.service import UserService
from app.src.common_models.users.schemas import BaseResponse

router = APIRouter()

@router.get("/user", response_model=BaseResponse)
def get_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user  # request.state.user에서 user_id 가져오기
    user_service = UserService(db)  # UserService 인스턴스 생성
    user = user_service.get_user(user_id)  # get_user 메서드 호출
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return BaseResponse(message="User fetched successfully", data={"user": user})
