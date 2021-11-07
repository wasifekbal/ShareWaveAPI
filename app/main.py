from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Root dir

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"Message": "/docs for documentation."}

# For getting all posts



