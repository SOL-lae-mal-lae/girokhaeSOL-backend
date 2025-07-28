from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.core import get_db
from .service import fetch_user_comments
from app.src.common_models.users.schemas import BaseResponse
from typing import List
from app.src.community.comments.model import Comment

router = APIRouter()

@router.get("/comments", response_model=BaseResponse)
def get_user_comments(request: Request, db: Session = Depends(get_db)):
    # 미들웨어에서 설정한 user_id 가져오기
    user_id = request.state.user  # 미들웨어에서 설정된 user_id를 사용
    
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    # fetch_user_comments 함수에서 user_id를 전달하여 댓글을 가져옴
    comments = fetch_user_comments(db, user_id)
    
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for the user")
    
    return BaseResponse(message="Comments fetched successfully", data={"comments": comments})
