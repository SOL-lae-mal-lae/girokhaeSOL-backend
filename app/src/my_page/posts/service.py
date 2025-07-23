from sqlalchemy.orm import Session
from .repository import get_posts_by_user_id

def fetch_user_posts(db: Session, user_id: str):
    return get_posts_by_user_id(db, user_id)
