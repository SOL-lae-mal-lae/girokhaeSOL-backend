from sqlalchemy.orm import Session
from app.src.common_models.users.schemas import UserResponse
from app.src.common_models.users.model import User
from app.src.community.posts.model import Post
from app.src.community.comments.model import Comment
from sqlalchemy import func
from fastapi import HTTPException

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: str) -> UserResponse:
        # 사용자 정보 조회
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 게시글 수 카운트
        try:
            post_count = self.db.query(func.count(Post.id)).filter(Post.user_id == user_id).scalar()
            print(f"[DEBUG] post_count for user_id={user_id}: {post_count}")
        except Exception as e:
            print(f"[ERROR] Failed to count posts for user_id={user_id}: {e}")
            post_count = 0

        # 댓글 수 카운트
        try:
            comment_count = self.db.query(func.count(Comment.id)).filter(Comment.user_id == user_id).scalar()
            print(f"[DEBUG] comment_count for user_id={user_id}: {comment_count}")
        except Exception as e:
            print(f"[ERROR] Failed to count comments for user_id={user_id}: {e}")
            comment_count = 0

        # UserResponse 생성
        return UserResponse(
            id=user.id,
            nickname=user.nickname,
            age=user.age,
            gender=user.gender,
            email=user.email,
            posts_count=post_count,  # 게시글 수
            comments_count=comment_count,  # 댓글 수
            profile_image=user.profile_image
        )
