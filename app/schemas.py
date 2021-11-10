from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from pydantic.networks import EmailStr


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime
    last_modified: datetime

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class PostSchema(BaseModel):
    title: str
    content: str


class CreatePostSchema(PostSchema):
    published: Optional[bool] = True


class CreatePostResponseSchema(PostSchema):
    post_id: int
    user_id: int
    published: bool
    timestamp: datetime

    class Config:
        orm_mode = True


class UpdatePostSchema(PostSchema):
    published: bool


class ResponsePostSchema(PostSchema):

    class User_info(BaseModel):
        user_id: int
        email: EmailStr

        class Config:
            orm_mode = True

    post_id: int
    published: bool
    timestamp: datetime
    user_info: User_info

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    user_id: int
    exp: str
