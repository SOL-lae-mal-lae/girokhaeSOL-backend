from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.core import Base

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(String, nullable=False)

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
