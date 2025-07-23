from sqlalchemy.orm import Session
from app.src.community.posts.model import Post

import logging

def get_posts_by_user_id(db: Session, user_id: str):
    logging.debug(f"Repository: Querying posts for user_id={user_id}")
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    logging.debug(f"Repository: Retrieved posts={posts}")
    return posts
