from sqlalchemy.orm import Session
from .models import Post

def get_posts_by_user_id(db: Session, user_id: str):
    return db.query(Post).filter(Post.user_id == user_id).all()
