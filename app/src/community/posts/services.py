from sqlalchemy.orm import Session
from .repository import PostRepository
from .model import Post
from .schemas import PostCreateRequest, PostUpdateRequest, PostResponse, PostListResponse
from typing import Optional, List

class PostService:
    def __init__(self, db: Session):
        self.repo = PostRepository(db)

    def create_post(self, request: PostCreateRequest, user_id: str) -> dict:
        post = Post(
            post_type=request.post_type,
            user_id=user_id,
            title=request.title,
            content=request.content,
            trade_log_id=request.trade_log_id,
            is_public=request.is_public
        )
        
        created_post = self.repo.create_post(post)
        
        return {"id": created_post.id}

    def get_post_by_id(self, post_id: int) -> Optional[PostResponse]:
        post = self.repo.get_post_by_id(post_id)
        if not post:
            return None
        
        return PostResponse(
            id=post.id,
            post_type=post.post_type,
            user_id=post.user_id,
            created_at=post.created_at,
            title=post.title,
            content=post.content,
            trade_log_id=post.trade_log_id,
            is_public=post.is_public
        )

    def get_all_posts(self) -> List[PostListResponse]:
        posts_with_data = self.repo.get_all_posts()
        return [
            PostListResponse(
                id=post.id,
                post_type=post.post_type,
                user_id=post.user_id,
                nickname=nickname,
                created_at=post.created_at,
                title=post.title,
                content=post.content,
                comment_count=comment_count
            ) for post, nickname, comment_count in posts_with_data
        ]

    def get_general_posts(self) -> List[PostListResponse]:
        posts_with_data = self.repo.get_general_posts()
        return [
            PostListResponse(
                id=post.id,
                post_type=post.post_type,
                user_id=post.user_id,
                nickname=nickname,
                created_at=post.created_at,
                title=post.title,
                content=post.content,
                comment_count=comment_count
            ) for post, nickname, comment_count in posts_with_data
        ]

    def get_trade_log_posts(self) -> List[PostListResponse]:
        posts_with_data = self.repo.get_trade_log_posts()
        return [
            PostListResponse(
                id=post.id,
                post_type=post.post_type,
                user_id=post.user_id,
                nickname=nickname,
                created_at=post.created_at,
                title=post.title,
                content=post.content,
                comment_count=comment_count
            ) for post, nickname, comment_count in posts_with_data
        ]

    def update_post(self, post_id: int, request: PostUpdateRequest) -> Optional[PostResponse]:
        # None이 아닌 필드만 업데이트 데이터로 구성
        update_data = {}
        if request.post_type is not None:
            update_data['post_type'] = request.post_type
        if request.title is not None:
            update_data['title'] = request.title
        if request.content is not None:
            update_data['content'] = request.content
        if request.trade_log_id is not None:
            update_data['trade_log_id'] = request.trade_log_id
        if request.is_public is not None:
            update_data['is_public'] = request.is_public

        updated_post = self.repo.update_post(post_id, update_data)
        if not updated_post:
            return None
        
        return PostResponse(
            id=updated_post.id,
            post_type=updated_post.post_type,
            user_id=updated_post.user_id,
            created_at=updated_post.created_at,
            title=updated_post.title,
            content=updated_post.content,
            trade_log_id=updated_post.trade_log_id,
            is_public=updated_post.is_public
        )

    def delete_post(self, post_id: int) -> bool:
        return self.repo.delete_post(post_id)

    def check_post_ownership(self, post_id: int, user_id: str) -> bool:
        post = self.repo.get_post_by_id(post_id)
        if not post:
            return False
        return post.user_id == user_id
