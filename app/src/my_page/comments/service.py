from sqlalchemy.orm import Session
from .repository import get_comments_by_user_id
from .schemas import CommentResponse  # CommentResponse import

def fetch_user_comments(db: Session, user_id: str):
    # user_id를 전달하여 해당 사용자의 댓글을 가져옴
    comments = get_comments_by_user_id(db, user_id)
    
    # SQLAlchemy 모델을 Pydantic 모델로 변환하여 반환
    return [CommentResponse.from_orm(comment) for comment in comments]
