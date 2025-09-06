from fastapi import FastAPI,APIRouter,status,Depends,HTTPException
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.models.schemas import CreateAppointment,ResAppointment
from app.models.models import Appointment,Doctor
from app.models import models
from app.core import oauth

app=FastAPI()
router=APIRouter(
    prefix="/appointment",
    tags=["appointments"]

)
@router.post("/book",status_code=status.HTTP_201_CREATED,response_model=ResAppointment)
def book_appointment(appointment:CreateAppointment,db:Session=Depends(get_db),current_user:models.User=Depends(oauth.get_current_user)):
    new_appointment=Appointment(**appointment.dict())
    appointments=db.query(Appointment).all()
    try:
        new_appointment.patient_id=current_user.id
        doctor=db.query(Doctor).filter(new_appointment.doctor_name==Doctor.name).first()
        new_appointment.doctor_id=doctor.id
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        return new_appointment
    except:
        raise HTTPException(status_code=status.HTTP_306_RESERVED,detail=f"You cannot engage an appointment in {new_appointment.appointment_time}")

