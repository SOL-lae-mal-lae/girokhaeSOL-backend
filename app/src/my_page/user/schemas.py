from app.src.common_models import User as UserBase
from typing import List, Optional
from sqlalchemy.orm import Mapped
from app.src.my_page.posts.schemas import PostResponse
from app.src.common_models.users.schemas import BaseResponse
from app.src.my_page.comments.schemas import CommentResponse

class UserResponse(UserBase):
    posts: Optional[List[PostResponse]] = []
    comments: Optional[List[CommentResponse]] = []

    class Config:
        orm_mode = True
