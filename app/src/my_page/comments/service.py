from sqlalchemy.orm import Session
from .repository import get_comments_by_user_id

def fetch_user_comments(db: Session, user_id: str):
    return get_comments_by_user_id(db, user_id)
