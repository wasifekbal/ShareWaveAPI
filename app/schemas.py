from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from pydantic.networks import EmailStr


class PostSchema(BaseModel):
    title: str
    content: str

class CreatePostSchema(PostSchema):
    published: Optional[bool] = True

class UpdatePostSchema(PostSchema):
    published: bool

class ResponsePostSchema(PostSchema):
    id: int
    published: bool
    timestamp: datetime

    class Config:
        orm_mode=True

class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    last_modified: datetime

    class Config:
        orm_mode=True
    
