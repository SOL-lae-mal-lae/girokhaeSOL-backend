from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.core import Base

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True, comment="댓글 ID")
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, comment="게시글 ID")
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False, comment="작성자 ID")
    content = Column(Text, nullable=False, comment="댓글 내용")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="작성일시")
