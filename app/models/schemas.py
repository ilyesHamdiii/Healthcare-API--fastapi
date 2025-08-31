from pydantic import BaseModel,EmailStr


class CreateUser(BaseModel):
    email:EmailStr
    password:str
class UserRead(BaseModel):
    id:int
    email:EmailStr
class UserLogin(CreateUser):
    pass