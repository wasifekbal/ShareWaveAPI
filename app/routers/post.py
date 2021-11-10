from fastapi import Response, status, Depends, APIRouter, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

# For getting all posts


@router.get("", response_model=List[schemas.ResponsePostSchema])
def get_posts(db: Session = Depends(get_db),
              search: Optional[str] = "",
              limit: int = 10,
              offset: int = 0,
              ):
    if not limit:
        limit = None
    posts = db.query(models.Posts).filter(models.Posts.title.contains(search)) .order_by(
        models.Posts.post_id.desc()).limit(limit).offset(offset).all()
    return posts

# For getting a single post


@router.get("/{id}", response_model=schemas.ResponsePostSchema)
def get_post(id: int,
             db: Session = Depends(get_db),
             response: Response = None,
             current_user: int = Depends(oauth2.get_current_user)
             ):

    post = db.query(models.Posts).filter(models.Posts.post_id == id).first()
    if post:
        response.status_code = status.HTTP_200_OK
        return post
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"404": "Post not found"}

# For creating a post


@router.post("", response_model=schemas.CreatePostResponseSchema)
def create_post(post_data: schemas.CreatePostSchema,
                db: Session = Depends(get_db),
                response: Response = None,
                current_user: int = Depends(oauth2.get_current_user)
                ):

    new_post = models.Posts(
        user_id=current_user["user_id"], **post_data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    response.status_code = status.HTTP_201_CREATED
    return new_post

# For deleting a post


@router.delete("/{id}")
def delete_post(id: int,
                db: Session = Depends(get_db),
                response: Response = None,
                current_user: int = Depends(oauth2.get_current_user)
                ):

    post_query = db.query(models.Posts).filter(models.Posts.post_id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Operation Forbidden")

    post_query.delete(synchronize_session=False)
    db.commit()
    response.status_code = status.HTTP_204_NO_CONTENT

# For updating a post


@router.put("/{id}", response_model=schemas.ResponsePostSchema)
def update_post(id: int, post_data: schemas.UpdatePostSchema,
                db: Session = Depends(get_db),
                response: Response = None,
                current_user: int = Depends(oauth2.get_current_user)
                ):

    post_query = db.query(models.Posts).filter(models.Posts.post_id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} not found"
        )
    if post.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Operation Forbidden")

    post_query.update(post_data.dict(), synchronize_session=False)
    db.commit()
    response.status_code = status.HTTP_200_OK
    return post_query.first()
