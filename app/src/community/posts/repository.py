from sqlalchemy.orm import Session
from app.src.common_models.users.model import User
from app.src.community.comments.model import Comment
from sqlalchemy import func
from .model import Post, TagPost
from typing import Optional, List

class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, post: Post) -> Post:
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_post_with_nickname(self, post_id: int) -> Optional[tuple]:
        return (
            self.db.query(Post, User.nickname)
            .join(User, Post.user_id == User.id)
            .filter(Post.id == post_id)
            .first()
        )

    def get_all_posts(self) -> List[tuple]:
        return (
            self.db.query(
                Post, 
                User.nickname,
                func.count(Comment.id).label('comment_count')
            )
            .join(User, Post.user_id == User.id)
            .outerjoin(Comment, Post.id == Comment.post_id)
            .group_by(Post.id, User.nickname)
            .order_by(Post.created_at.desc())
            .all()
        )

    def get_general_posts(self) -> List[tuple]:
        return (
            self.db.query(
                Post, 
                User.nickname,
                func.count(Comment.id).label('comment_count')
            )
            .join(User, Post.user_id == User.id)
            .outerjoin(Comment, Post.id == Comment.post_id)
            .filter(Post.post_type == True)
            .group_by(Post.id, User.nickname)
            .order_by(Post.created_at.desc())
            .all()
        )

    def get_trade_log_posts(self) -> List[tuple]:
        return (
            self.db.query(
                Post, 
                User.nickname,
                func.count(Comment.id).label('comment_count')
            )
            .join(User, Post.user_id == User.id)
            .outerjoin(Comment, Post.id == Comment.post_id)
            .filter(Post.post_type == False)
            .group_by(Post.id, User.nickname)
            .order_by(Post.created_at.desc())
            .all()
        )

    def update_post(self, post_id: int, update_data: dict) -> Optional[Post]:
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return None
        
        for key, value in update_data.items():
            if hasattr(post, key):
                setattr(post, key, value)
        
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete_post(self, post_id: int) -> bool:
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return False
        
        self.db.delete(post)
        self.db.commit()
        return True

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        return self.db.query(Post).filter(Post.id == post_id).first()

    def create_tag(self, tag: TagPost) -> TagPost:
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag
