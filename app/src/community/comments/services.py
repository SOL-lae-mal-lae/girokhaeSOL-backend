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
        comments = self.repo.get_comments_by_post_id(post_id)
        return [
            CommentListResponse(
                id=comment.id,
                user_id=comment.user_id,
                content=comment.content,
                created_at=comment.created_at
            ) for comment in comments
        ]

    def delete_comment(self, comment_id: int) -> bool:
        return self.repo.delete_comment(comment_id)

    def update_comment(self, comment_id: int, request: CommentUpdateRequest) -> Optional[CommentResponse]:
        update_data = {"content": request.content}
        
        updated_comment = self.repo.update_comment(comment_id, update_data)
        if not updated_comment:
            return None
        
        return CommentResponse(
            id=updated_comment.id,
            post_id=updated_comment.post_id,
            user_id=updated_comment.user_id,
            content=updated_comment.content,
            created_at=updated_comment.created_at
        )
