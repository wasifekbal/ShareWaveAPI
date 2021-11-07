from fastapi import FastAPI, Response, status, HTTPException, Depends
from time import sleep
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Root dir


@app.get("/")
def read_root():
    return {"Message": "/docs for documentation."}

# For getting all posts


@app.get("/posts", response_model=List[schemas.ResponsePostSchema])
def get_posts(db: Session = Depends(get_db), response: Response = None):

    posts = db.query(models.Post).all()
    response.status_code = status.HTTP_200_OK
    return posts

# For getting a single post


@app.get("/post/{id}", response_model=schemas.ResponsePostSchema)
def get_post(id: int, db: Session = Depends(get_db), response: Response = None):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        response.status_code = status.HTTP_200_OK
        return post
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"404": "Post not found"}

# For creating a post


@app.post("/create", response_model=schemas.ResponsePostSchema)
def create_post(post_data: schemas.CreatePostSchema, db: Session = Depends(get_db), response: Response = None):

    new_post = models.Post(**post_data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    response.status_code = status.HTTP_201_CREATED
    return new_post

# For deleting a post


@app.delete("/post/{id}")
def delete_post(id: int, db: Session = Depends(get_db), response: Response = None):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if(post_query.first()):
        post_query.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"404": "Post not found"}

# For updating a post


@app.put("/post/{id}")
def update_post(id: int, post_data: schemas.UpdatePostSchema,
                db: Session = Depends(get_db),
                response: Response = None):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if(post_query.first()):
        post_query.update(post_data.dict(), synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_200_OK
        return post_query.first()
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"404": "Post not found"}
