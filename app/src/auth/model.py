from uuid import UUID
from pydantic import BaseModel, EmailStr

class registerUser(BaseModel):
    username: str
    email: EmailStr
    password: str


