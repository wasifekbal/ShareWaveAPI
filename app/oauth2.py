from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "82d10e4c732871b463134eeccf8e8141cc3eb8ca2a19b0f03c4c27451e3041d4d3e290"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    data_copy = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy.update({"exp":expire})
    encoded_jwt = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenDataSchema(id=id)
        return token_data
        
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"could not validate credentials"},
        headers={"WWW-Authenticate":"Bearer"}
    )

    return verify_access_token(token=token, credentials_exception=credentials_exception)
