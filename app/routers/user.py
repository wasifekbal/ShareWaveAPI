from fastapi import Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from datetime import datetime
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserOut)
def create_user(users_data: schemas.CreateUserSchema,db: Session = Depends(get_db),response: Response = None):
    users_data = users_data.dict()
    users_data.update({
        "password":utils.get_password_hash(users_data["password"]),
        "created_at": str(datetime.now())
        })
    print(users_data)
    new_user = models.Users(**users_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response.status_code = status.HTTP_201_CREATED
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db),response: Response = None):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user:
        return user
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"404":f"User with id : {id} not found"}