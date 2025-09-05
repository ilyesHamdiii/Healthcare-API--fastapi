from fastapi import FastAPI,APIRouter,status,HTTPException,Depends
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.schemas import ResDoctor,CreateDoctor
from app.models.models import Doctor

app=FastAPI()
router=APIRouter(
    prefix="/doctors",
    tags=["doctors"]
)

@router.post("",status_code=status.HTTP_201_CREATED,response_model=ResDoctor)
def create(doctor:CreateDoctor,db:Session=Depends(get_db)):
    new_doctor=Doctor(**doctor.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor
@router.get("/list",status_code=status.HTTP_200_OK,response_model=list[ResDoctor])
def get(db:Session=Depends(get_db)):
    doctors=db.query(Doctor).all()
    return doctors