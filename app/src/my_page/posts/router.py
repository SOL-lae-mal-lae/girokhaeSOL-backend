from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.core import get_db
from .service import fetch_user_posts
from app.src.common_models.users.schemas import BaseResponse

router = APIRouter()

@router.get("/posts", response_model=BaseResponse)
def get_user_posts(request: Request, db: Session = Depends(get_db)):
    # 미들웨어에서 설정한 user_id를 가져옴
    user_id = request.state.user  # 미들웨어에서 user_id를 설정했다고 가정
    
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    # user_id를 기반으로 게시글을 가져옴
    posts = fetch_user_posts(db, user_id)
    
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for the user")
    
    return BaseResponse(message="Posts fetched successfully", data={"posts": posts})
