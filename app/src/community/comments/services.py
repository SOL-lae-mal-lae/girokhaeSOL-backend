from sqlalchemy.orm import Session
from .repository import CommentRepository
from .model import Comment
from .schemas import CommentCreateRequest, CommentUpdateRequest, CommentListResponse, CommentResponse
from typing import List, Optional


class CommentService:
    def __init__(self, db: Session):
        self.repo = CommentRepository(db)

    def create_comment(self, request: CommentCreateRequest, post_id: int, user_id: str) -> dict:
        comment = Comment(
            post_id=post_id,
            user_id=user_id,
            content=request.content
        )
        
        created_comment = self.repo.create_comment(comment)
        
        return {"id": created_comment.id}

    def get_comments_by_post_id(self, post_id: int) -> List[CommentListResponse]:
        comments_with_data = self.repo.get_comments_with_nickname_by_post_id(post_id)
        return [
            CommentListResponse(
                id=comment.id,
                user_id=comment.user_id,
                nickname=nickname,
                content=comment.content,
                created_at=comment.created_at
            ) for comment, nickname in comments_with_data
        ]

    def delete_comment(self, comment_id: int) -> bool:
        return self.repo.delete_comment(comment_id)

    def update_comment(self, comment_id: int, request: CommentUpdateRequest) -> Optional[CommentResponse]:
        update_data = {"content": request.content}
        
        updated_comment = self.repo.update_comment(comment_id, update_data)
        if not updated_comment:
            return None
        
        # 업데이트된 댓글의 닉네임 정보를 가져옴
        comment_data = self.repo.get_comment_with_nickname_by_id(comment_id)
        if not comment_data:
            return None
        
        comment, nickname = comment_data
        
        return CommentResponse(
            id=comment.id,
            post_id=comment.post_id,
            user_id=comment.user_id,
            nickname=nickname,
            content=comment.content,
            created_at=comment.created_at
        )

    def check_comment_ownership(self, comment_id: int, user_id: str) -> bool:
        comment = self.repo.get_comment_by_id(comment_id)
        if not comment:
            return False
        return comment.user_id == user_id
