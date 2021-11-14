from fastapi import Response, status, Depends, APIRouter
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
