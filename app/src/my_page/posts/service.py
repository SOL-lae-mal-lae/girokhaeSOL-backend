from sqlalchemy.orm import Session
from .repository import get_posts_by_user_id

from .schemas import PostResponse

def fetch_user_posts(db, user_id):
    posts = get_posts_by_user_id(db, user_id)
    return [PostResponse.from_orm(post) for post in posts]
