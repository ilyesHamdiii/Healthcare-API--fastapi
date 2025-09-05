from sqlalchemy import Column,Integer,String,ForeignKey,CheckConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression  import text

class User(Base):
    __tablename__ = "users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    articles = relationship("Article", back_populates="author")
    appointment=relationship("Appointment",back_populates="patient")
class Article(Base):
    __tablename__="articles"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    author_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE",onupdate="CASCADE"))
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    author = relationship("User", back_populates="articles")
    class config:
        from_attributes = True 
class Doctor(Base):
    __tablename__="doctors"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    speciality=Column(String,nullable=False)
    bio=Column(String,nullable=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    appointments = relationship("Appointment", back_populates="doctor")

class Appointment(Base):
    __tablename__="appointments"
    id=Column(Integer,primary_key=True,nullable=False)
    patient=relationship("User",back_populates="appointments")
    patient_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    doctor=relationship("Doctor",back_populates="appointments")
    doctor_id=Column(Integer,ForeignKey("doctors.id"),nullable=False)

    appointment_time=Column(TIMESTAMP(timezone=True),nullable=False)
    status=Column(String,CheckConstraint("status IN ('booked','canceled','completed')"),nullable=False)
