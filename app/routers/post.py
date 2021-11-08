from fastapi import Response, status, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

# For getting all posts


@router.get("/", response_model=List[schemas.ResponsePostSchema])
def get_posts(db: Session = Depends(get_db), response: Response = None):

    posts = db.query(models.Posts).all()
    response.status_code = status.HTTP_200_OK
    return posts

# For getting a single post


@router.get("/{id}", response_model=schemas.ResponsePostSchema)
def get_post(id: int, db: Session = Depends(get_db), response: Response = None):

    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if post:
        response.status_code = status.HTTP_200_OK
        return post
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"404": "Post not found"}

# For creating a post


@router.post("/", response_model=schemas.ResponsePostSchema)
def create_post(post_data: schemas.CreatePostSchema, 
                db: Session = Depends(get_db), 
                response: Response = None,
                get_current_user: int = Depends(oauth2.get_current_user)
                ):

    new_post = models.Posts(**post_data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    response.status_code = status.HTTP_201_CREATED
    return new_post

# For deleting a post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), response: Response = None):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    if(post_query.first()):
        post_query.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"404": "Post not found"}

# For updating a post


@router.put("/{id}")
def update_post(id: int, post_data: schemas.UpdatePostSchema,
                db: Session = Depends(get_db),
                response: Response = None):

    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    if(post_query.first()):
        post_query.update(post_data.dict(), synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_200_OK
        return post_query.first()
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"404": "Post not found"}
