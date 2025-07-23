from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.core import Base
from typing import List
from app.src.my_page.posts.models import Post
from app.src.my_page.comments.models import Comment

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(50), primary_key=True, index=True)
    nickname: Mapped[str] = mapped_column(String(25))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(10))  # ex: 'male', 'female'

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="user")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user")