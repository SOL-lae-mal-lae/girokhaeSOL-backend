from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.core import get_db
from .service import fetch_user_comments
from app.src.common_models.users.schemas import BaseResponse
from typing import List

router = APIRouter()

@router.get("/comments/{user_id}", response_model=BaseResponse)
def get_user_comments(user_id: str, db: Session = Depends(get_db)):
    comments = fetch_user_comments(db, user_id)
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for the user")
    return BaseResponse(message="Comments fetched successfully", data={"comments": comments})
