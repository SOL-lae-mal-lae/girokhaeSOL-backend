from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.core import get_db
from .service import fetch_user_posts
from app.src.common_models.users.schemas import BaseResponse
from .schemas import PostResponse
from typing import List

router = APIRouter()

@router.get("/posts/{user_id}", response_model=BaseResponse)
def get_user_posts(user_id: str, db: Session = Depends(get_db)):
    posts = fetch_user_posts(db, user_id)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for the user")
    return BaseResponse(message="Posts fetched successfully", data={"posts": posts})
