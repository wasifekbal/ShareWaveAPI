from typing import Optional
from pydantic import BaseModel
from datetime import datetime


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