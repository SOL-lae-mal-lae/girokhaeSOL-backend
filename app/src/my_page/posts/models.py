from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.core import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    post_type = Column(Boolean, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    created_at = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_public = Column(Boolean, default=True)

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
