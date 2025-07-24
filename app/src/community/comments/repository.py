from sqlalchemy.orm import Session
from .model import Comment
from app.src.common_models.users.model import User
from typing import List
from typing import Optional


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_comment(self, comment: Comment) -> Comment:
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_comments_by_post_id(self, post_id: int) -> List[Comment]:
        return self.db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.asc()).all()

    def get_comments_with_nickname_by_post_id(self, post_id: int) -> List[tuple]:
        return (
            self.db.query(Comment, User.nickname)
            .join(User, Comment.user_id == User.id)
            .filter(Comment.post_id == post_id)
            .order_by(Comment.created_at.asc())
            .all()
        )

    def delete_comment(self, comment_id: int) -> bool:
        comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            return False
        
        self.db.delete(comment)
        self.db.commit()
        return True

    def update_comment(self, comment_id: int, update_data: dict) -> Optional[Comment]:
        comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            return None
        
        for key, value in update_data.items():
            if hasattr(comment, key):
                setattr(comment, key, value)
        
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_comment_by_id(self, comment_id: int) -> Optional[Comment]:
        return self.db.query(Comment).filter(Comment.id == comment_id).first()

    def get_comment_with_nickname_by_id(self, comment_id: int) -> Optional[tuple]:
        return (
            self.db.query(Comment, User.nickname)
            .join(User, Comment.user_id == User.id)
            .filter(Comment.id == comment_id)
            .first()
        )
