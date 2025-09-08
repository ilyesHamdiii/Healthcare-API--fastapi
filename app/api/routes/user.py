from fastapi import FastAPI,APIRouter,status,Query
from sqlalchemy.orm import Session
from app.db.base import Base
from app.models import models,schemas
from fastapi.params import Depends
from app.db.base import engine,get_db
from app.core import utility
from app.models.models import Role
from app.core.roles import require_role

app=FastAPI()


app=FastAPI
router=APIRouter(
    prefix="/users",
    tags=["users"]
)
models.Base.metadata.create_all(bind=engine)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRead)
def CreateUser(user: schemas.CreateUser, db: Session = Depends(get_db),current_user:models.User=Depends(require_role(Role.ADMIN))):
    hashed_password = utility.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/doctors", status_code=status.HTTP_200_OK, response_model=list[schemas.UserRead],)
def get_doctors(db: Session = Depends(get_db),current_user:models.User=Depends(require_role(Role.ADMIN,Role.DOCTOR,Role.PATIENT)),limit:int=Query(default=10,le=100),speciality:str=""):
    doctors = db.query(models.User).filter(models.User.role == "doctor").filter(models.User.speciality.startswith(speciality)).all()
    return doctors