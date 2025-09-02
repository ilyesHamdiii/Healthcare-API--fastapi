from datetime import timedelta,timezone,datetime
import jwt 
import os 
from jose import JWTError
from fastapi import Depends,status,HTTPException
from app.models import schemas
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from app.models import models
from app.db import base
from sqlalchemy.orm import Session

ouath_scheme=OAuth2PasswordBearer(tokenUrl="/login")
load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_access_token(data:dict,expires_delta:timedelta|None=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.now(timezone.utc)+expires_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id:str=payload.get("user_id")
        print(id)
        if not user_id:
            raise credentials_exception
        token_data=schemas.TokenData(id=user_id)
    except JWTError:raise credentials_exception
    return token_data(id=user_id)


def get_current_user(token: str = Depends(ouath_scheme),db: Session = Depends(base.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == int(token_data.id)).first()
    if not user:
        raise credentials_exception
    return user