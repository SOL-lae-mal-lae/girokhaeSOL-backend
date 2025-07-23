from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.core import get_db
from .service import fetch_user_details
from app.src.common_models.users.schemas import BaseResponse

router = APIRouter()

@router.get("/user/{user_id}", response_model=BaseResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = fetch_user_details(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return BaseResponse(message="User fetched successfully", data={"user": user})
