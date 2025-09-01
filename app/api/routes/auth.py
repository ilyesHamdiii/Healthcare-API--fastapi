from fastapi import FastAPI,APIRouter,status,HTTPException
from fastapi.params import Depends
from app.models import schemas
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models import models
from app.core import utility,oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
app=FastAPI()
router=APIRouter(
    tags=["authorisation"]
)

@router.post("/login",status_code=status.HTTP_202_ACCEPTED,response_model=schemas.UserRead)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials")
    else:
        if not utility.verify(user_credentials.password,user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials")
    token=oauth.create_access_token({"user_id ":user.id})
    return {"access_token":token,"token_type":"bearer"}
@router.get("/me",response_model=schemas.UserRead)
def GetUser(db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User id does not exit")
    return user