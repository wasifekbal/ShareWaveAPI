from fastapi import Response, status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import or_
from app import oauth2
from .. import models, schemas, utils
from datetime import datetime
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

## For getting info of a logged in user

@router.get("/me", response_model=schemas.UserOut)
def who_am_i(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    user = db.query(models.Users).filter(
        models.Users.user_id == current_user["user_id"]).first()
    return user

## For getting info of a user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user_of_id(id: int,
             db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)
             ):
    user = db.query(models.Users).filter(models.Users.user_id == id).first()
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"404": "User not found"}
        )

## Updating user info

@router.put("/update", response_model=schemas.UserOut)
def update_user_info(user_data: schemas.UpdateUserSchema,
                     db: Session = Depends(get_db),
                     current_user: dict = Depends(oauth2.get_current_user),
                     response: Response = None
                    ):
    email_check_q = db.query(models.Users).filter(models.Users.email == user_data.new_email).first()
    username_check_q = db.query(models.Users).filter(models.Users.username == user_data.username).first()
    query = db.query(models.Users).filter(models.Users.email == user_data.old_email)
    if email_check_q:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="New email address is already in use. Please choose another"
        )
    if username_check_q:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Username is already in use. Please choose another"
        )
    query.update({
            "email":user_data.new_email,
            "username":user_data.username
        }, synchronize_session=False)
    db.commit()
    response.status_code = status.HTTP_200_OK
    return query.first()

## resetting password

@router.put("/forgotpassword")
def forgot_password(user_data: schemas.ForgotPasswordSchema, db: Session = Depends(get_db)):
    query = db.query(models.Users).filter(
        models.Users.email == user_data.email)
    if query.first():
        hashed_password = utils.get_password_hash(user_data.new_password)
        query.update({"password": hashed_password}, synchronize_session=False)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Password updated successfully"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
