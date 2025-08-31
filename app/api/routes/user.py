from fastapi import FastAPI,APIRouter,status
from sqlalchemy.orm import Session
from app.db.base import Base
from app.models import models,schemas
from fastapi.params import Depends
from app.db.base import engine,get_db
from app.core import utility



app=FastAPI
router=APIRouter(
    prefix="/users",
    tags=["users"]
)
models.Base.metadata.create_all(bind=engine)

@router.post("register",status_code=status.HTTP_201_CREATED,response_model=schemas.UserRead)
def CreateUser(user:schemas.CreateUser,db:Session=Depends(get_db)):
    hashed_passowrd=utility.hash(user.password)
    user.password=hashed_passowrd
    new_user=models.user(*user.dict())
    db.add(new_user)
    db.commit()
    db.refresh()
    return new_user