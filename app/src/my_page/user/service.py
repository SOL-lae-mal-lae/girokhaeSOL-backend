from sqlalchemy.orm import Session
from .repository import get_user_by_id

def fetch_user_details(db: Session, user_id: str):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    return user
