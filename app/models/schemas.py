from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class CreateUser(BaseModel):
    email:EmailStr
    password:str
class UserRead(BaseModel):
    id:int
    email:EmailStr
class UserLogin(CreateUser):
    pass
class AuthorInfo(BaseModel):
    id:int
    email:EmailStr
    class config:
        from_attributes = True 

class CreateArticle(BaseModel):
    title:str
    content:str

class CreateDoctor(BaseModel):
    name:str
    speciality:str
    bio:str
class ResDoctor(BaseModel):
    id:int
    name:str
    speciality:str
    bio:str
    

class DoctorInfo(BaseModel):
    id:int
    name:str
    specialty:str
    bio:str    
    class config:
        from_attributes=True
class ResAppointment(BaseModel):
    id:int
    patient:Optional[AuthorInfo]
    doctor:Optional[DoctorInfo]
    appointment_time:datetime
    status:str
    class config:
        from_attributes=True
class CreateAppointment(BaseModel):
    doctor_name:str
    appintment_time:datetime
    status:str
    class config:
        from_attributes=True
    




class ResArticle(BaseModel):
    id:int
    title:str
    content:str
    author: Optional[AuthorInfo]
    class config:
       from_attributes = True 
class UpdateArticle(BaseModel):
    title:Optional[str]|None
    content:Optional[str]|None

class TokenData(BaseModel):
    id:Optional[str]=None
class Token(BaseModel):
    access_token:str
    token_type:str

class LoginRequest(BaseModel):
    email:EmailStr
    password:str
