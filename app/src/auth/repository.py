from sqlalchemy.orm import Session
from app.src.account.model import User

def check_user_by_user_id(db: Session, user_id: str) -> User | None:
    return db.query(User).filter(User.id == user_id).first()