from sqlalchemy.orm import Session
from .models import Comment

def get_comments_by_user_id(db: Session, user_id: str):
    # user_id에 해당하는 댓글을 모두 가져옴
    return db.query(Comment).filter(Comment.user_id == user_id).all()
