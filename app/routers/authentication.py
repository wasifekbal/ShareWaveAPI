from fastapi import Response, status, Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from datetime import datetime
from ..database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), response: Response = None):

    fetched_user = db.query(models.Users).filter(
        models.Users.email == user_data.username).first()

    if not fetched_user:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"403": "FORBIDDEN"}

    if not utils.verify_password(user_data.password, fetched_user.password):
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"403": "FORBIDDEN"}

    token = oauth2.create_access_token(
        data={
            "user_id": fetched_user.user_id
        }
    )

    return {"access_token": token, "token_type": "bearer"}

@router.post("/signup", response_model=schemas.UserOut)
def Signup(user_data: schemas.CreateUserSchema,
                db: Session = Depends(get_db),
                response: Response = None,
                ):
    email_check_q = db.query(models.Users).filter(models.Users.email == user_data.email).first()
    username_check_q = db.query(models.Users).filter(models.Users.username == user_data.username).first()
    if email_check_q:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Email address is already in use. Please choose another"
        )
    if username_check_q:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Username is already in use. Please choose another"
        )
    users_data = user_data.dict()
    users_data.update({
        "password": utils.get_password_hash(users_data["password"]),
        # "created_at": str(datetime.utcnow())
    })
    new_user = models.Users(**users_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response.status_code = status.HTTP_201_CREATED
    return new_user
