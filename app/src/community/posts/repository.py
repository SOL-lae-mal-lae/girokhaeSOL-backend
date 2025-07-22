from sqlalchemy.orm import Session
from .model import Post
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

    def get_all_posts(self) -> List[Post]:
        return self.db.query(Post).order_by(Post.created_at.desc()).all()

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
