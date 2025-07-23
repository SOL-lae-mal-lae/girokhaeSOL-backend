from sqlalchemy.orm import Session
from .models import Comment

def get_comments_by_user_id(db: Session, user_id: str):
    return db.query(Comment).filter(Comment.user_id == user_id).all()
