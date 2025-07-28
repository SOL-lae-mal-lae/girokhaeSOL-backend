from sqlalchemy.orm import Session
from app.src.common_models.users.schemas import UserResponse
from app.src.common_models.users.model import User

def get_user_by_id(db: Session, user_id: str) -> UserResponse:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    return UserResponse(
        id=user.id,
        nickname=user.nickname,
        age=user.age,
        gender=user.gender,
        email=user.email,
        posts_count=user.posts_count,  # 이 부분은 나중에 카운트 값이 계산된 값으로 교체할 수 있습니다.
        comments_count=user.comments_count,
        profile_image=user.profile_image
    )
