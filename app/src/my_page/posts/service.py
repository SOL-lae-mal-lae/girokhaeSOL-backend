from sqlalchemy.orm import Session
from .repository import get_posts_by_user_id
from .schemas import PostResponse

def fetch_user_posts(db: Session, user_id: str):
    # get_posts_by_user_id 함수에 user_id를 전달하여 게시글을 가져옴
    posts = get_posts_by_user_id(db, user_id)
    
    # 가져온 게시글 리스트를 PostResponse로 변환하여 반환
    return [PostResponse.from_orm(post) for post in posts]
