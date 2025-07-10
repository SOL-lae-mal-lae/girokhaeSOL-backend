# Community Repository
# 커뮤니티 관련 데이터베이스 접근 로직을 처리합니다.

from sqlalchemy.orm import Session
from typing import List, Optional
from .model import Post, Comment


class CommunityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        """ID로 게시글 조회"""
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_posts(self, skip: int = 0, limit: int = 100) -> List[Post]:
        """게시글 목록 조회"""
        return self.db.query(Post).offset(skip).limit(limit).all()

    def create_post(self, post_data: dict) -> Post:
        """새 게시글 생성"""
        post = Post(**post_data)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def update_post(self, post_id: int, update_data: dict) -> Optional[Post]:
        """게시글 업데이트"""
        post = self.get_post_by_id(post_id)
        if post:
            for key, value in update_data.items():
                setattr(post, key, value)
            self.db.commit()
            self.db.refresh(post)
        return post

    def delete_post(self, post_id: int) -> bool:
        """게시글 삭제"""
        post = self.get_post_by_id(post_id)
        if post:
            self.db.delete(post)
            self.db.commit()
            return True
        return False

    def get_comments_by_post_id(self, post_id: int) -> List[Comment]:
        """게시글별 댓글 조회"""
        return self.db.query(Comment).filter(Comment.post_id == post_id).all()

    def create_comment(self, comment_data: dict) -> Comment:
        """새 댓글 생성"""
        comment = Comment(**comment_data)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment
