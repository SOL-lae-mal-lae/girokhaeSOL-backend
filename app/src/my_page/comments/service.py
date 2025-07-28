from sqlalchemy.orm import Session
from .repository import get_comments_with_post_title_by_user_id  # Updated import
from .schemas import CommentResponse  # CommentResponse import

def fetch_user_comments(db: Session, user_id: str):
    # Use the repository function to fetch comments with post titles
    comments = get_comments_with_post_title_by_user_id(db, user_id)

    # SQLAlchemy 모델을 Pydantic 모델로 변환하여 반환
    return [
        CommentResponse(
            id=comment.id,
            post_id=comment.post_id,
            user_id=comment.user_id,
            created_at=comment.created_at,
            content=comment.content,
            post_title=post_title
        )
        for comment, post_title in comments
    ]
