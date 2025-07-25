from sqlalchemy.orm import Session
from app.src.community.comments.model import Comment
from app.src.community.posts.model import Post


def get_comments_by_user_id(db: Session, user_id: str):
    # user_id에 해당하는 댓글을 모두 가져옴
    return db.query(Comment).filter(Comment.user_id == user_id).all()

def get_comments_with_post_title_by_user_id(db: Session, user_id: str):
    # Join comments with posts to fetch post titles
    return db.query(Comment, Post.title.label("post_title"))\
        .join(Post, Comment.post_id == Post.id)\
        .filter(Comment.user_id == user_id)\
        .order_by(Comment.created_at.desc()).all()