from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CreateUser(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "patient"
    speciality: Optional[str] = None
    bio: Optional[str] = None

class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: str
    speciality: Optional[str] = None
    bio: Optional[str] = None

class UserLogin(CreateUser):
    pass

class AuthorInfo(BaseModel):
    id: int
    email: EmailStr
    role: str
    speciality: Optional[str] = None
    bio: Optional[str] = None
    class config:
        from_attributes = True

class CreateArticle(BaseModel):
    title: str
    content: str

class UpdateAppointment(BaseModel):
    appointment_time: datetime
    status: str

class ResAppointment(BaseModel):
    id: int
    patient: Optional[AuthorInfo]
    doctor: Optional[AuthorInfo] = None
    appointment_time: datetime
    status: str
    class config:
        from_attributes = True

class CreateAppointment(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_time: datetime
    class config:
        from_attributes = True

class ResArticle(BaseModel):
    id: int
    title: str
    content: str
    author: Optional[AuthorInfo]
    class config:
       from_attributes = True

class UpdateArticle(BaseModel):
    title: Optional[str] | None
    content: Optional[str] | None

class TokenData(BaseModel):
    id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class NotificationSchema(BaseModel):
    id:int
    message:str
    is_read:bool
    created_at:datetime
    class Config:
        from_attributes=True