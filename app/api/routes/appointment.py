from fastapi import FastAPI,APIRouter,status,Depends,HTTPException
from app.db.base import get_db
from sqlalchemy.orm import Session,joinedload
from app.models.schemas import CreateAppointment,ResAppointment,UpdateAppointment
from app.models.models import Appointment,Role
from app.models import models
from app.core import oauth
from sqlalchemy.exc import IntegrityError
from datetime import datetime,timedelta
from app.core.roles import require_role

app=FastAPI()
router=APIRouter(
    prefix="/appointment",
    tags=["appointments"]
)
@router.post(
    "/book",
    status_code=status.HTTP_201_CREATED,
    response_model=ResAppointment,
    summary="Book Appointment",
    description="Book a new appointment with a doctor. Only patients and admins can book appointments."
)
def book_appointment(
    appointment: CreateAppointment,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(Role.PATIENT, Role.ADMIN)),
):
    # 1. Authorization: only allow booking for yourself
    if appointment.patient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only book appointments for yourself."
        )

    # 2. Check doctor exists and is a doctor
    doctor = db.query(models.User).filter(models.User.id == appointment.doctor_id, models.User.role == "doctor").first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")

    start_time = appointment.appointment_time
    end_time = start_time + timedelta(minutes=30)

    # 3. Check doctor availability with time overlap
    conflict = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == appointment.doctor_id,
        models.Appointment.appointment_time < end_time,
        (models.Appointment.appointment_time + timedelta(minutes=30)) > start_time
    ).first()

    if conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Doctor already has an appointment around {appointment.appointment_time}"
        )

    # 4. Create appointment
    new_appointment = models.Appointment(
        patient_id=current_user.id,
        doctor_id=appointment.doctor_id,
        appointment_time=appointment.appointment_time,
        status="booked"
    )

    try:
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        doctor_notification=models.Notification(
            user_id=appointment.doctor_id,
            message=f"New appointment booked by {current_user.email}"
        )
        db.add(doctor_notification)
        db.commit()
        db.refresh(doctor_notification)


        return new_appointment
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid appointment data or duplicate booking."
        )
@router.get(
    "/my_appointments",
    response_model=list[ResAppointment],
    status_code=status.HTTP_200_OK,
    summary="Get My Appointments",
    description="Retrieve all appointments for the currently authenticated user."
)
def get_appointment(
    current_user = Depends(require_role(Role.PATIENT, Role.DOCTOR, Role.ADMIN)),
    db: Session = Depends(get_db)
):
    appointments = (
        db.query(models.Appointment)
        .options(
            joinedload(models.Appointment.patient),
            joinedload(models.Appointment.doctor)
        )
        .filter(models.Appointment.patient_id == current_user.id)
        .all()
    )
    if not appointments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No appointments found")
    return appointments
@router.put(
    "/update",
    response_model=ResAppointment,
    status_code=status.HTTP_200_OK,
    summary="Update Appointment",
    description="Update an existing appointment. Only the patient who booked the appointment can update it."
)
def update(
    appointment: UpdateAppointment,
    id: int,
    current_user: models.User = Depends(require_role(Role.ADMIN, Role.DOCTOR)),
    db: Session = Depends(get_db)
):
    update_appointment=db.query(Appointment).options(
        joinedload(Appointment.patient),joinedload(Appointment.doctor)
    ).filter(Appointment.id==id).first()
    if not update_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid appointment Data")
    if current_user.id !=update_appointment.patient_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You can only update your appointment")
    update_appointment.appointment_time=appointment.appointment_time
    if appointment.status not in ["booked","canceled","completed"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"status need to be valid (completed,canceled,booked)")
    update_appointment.status=appointment.status
    db.commit()
    db.refresh(update_appointment)
    return update_appointment
@router.delete(
    "/cancel",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel Appointment",
    description="Cancel an appointment by its ID. Only the patient who booked the appointment can cancel it."
)
def delete(
    id: int,
    current_user: models.User = Depends(require_role(Role.ADMIN, Role.DOCTOR)),
    db: Session = Depends(get_db)
):
    appointment=db.query(Appointment).filter(Appointment.id==id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid appointment Data")
    if appointment.patient_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"U can only delete your own appointments")
    db.delete(appointment)
    db.commit()
    return {"message": f"Appointment  with id ({id}) is canceled"}
