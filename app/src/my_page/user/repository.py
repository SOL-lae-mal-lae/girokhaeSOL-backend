from sqlalchemy.orm import Session
from app.src.common_models import User

def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()
