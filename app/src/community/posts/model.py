from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.core import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True, comment="게시글 ID")
    post_type = Column(Boolean, nullable=False, comment="게시글 타입 (True: 일반, False: 매매일지)")
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False, comment="작성자 ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="작성일시")
    title = Column(String(200), nullable=False, comment="제목")
    content = Column(Text, nullable=False, comment="내용")
    trade_log_id = Column(Integer, ForeignKey("trade_logs.id"), nullable=True, comment="매매일지 ID")
    is_public = Column(Boolean, default=True, comment="공개 여부")

