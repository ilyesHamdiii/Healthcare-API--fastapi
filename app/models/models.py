from sqlalchemy import Column, Integer,DateTime, String, ForeignKey, CheckConstraint,Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from enum import Enum
from datetime import datetime
class Role(str, Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    articles = relationship("Article", back_populates="author")
    appointments = relationship("Appointment", back_populates="patient", foreign_keys='Appointment.patient_id')
    doctor_appointments = relationship("Appointment", back_populates="doctor", foreign_keys='Appointment.doctor_id')
    role = Column(String, nullable=False, default="patient")
    speciality = Column(String, nullable=True)  # Only for doctors
    bio = Column(String, nullable=True)     
    notifications=relationship("Notification",back_populates="user")    # Only for doctors

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    author = relationship("User", back_populates="articles")
    class config:
        from_attributes = True

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False,onupdate="CASCADE")
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False,onupdate="CASCADE")
    appointment_time = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(String, CheckConstraint("status IN ('booked','canceled','completed')"), nullable=False)

    patient = relationship("User", foreign_keys=[patient_id], back_populates="appointments")
    doctor = relationship("User", foreign_keys=[doctor_id], back_populates="doctor_appointments")
class Notification(Base):
    __tablename__="notifications"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    message=Column(String,nullable=False)
    is_read=Column(Boolean,default=False)
    created_at=Column(DateTime(timezone=True),server_default=text("now()"))
    user=relationship("User",back_populates="notifications")