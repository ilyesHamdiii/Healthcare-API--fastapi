from pydantic import BaseModel,EmailStr
from typing import Optional

class CreateUser(BaseModel):
    email:EmailStr
    password:str
class UserRead(BaseModel):
    id:int
    email:EmailStr
class UserLogin(CreateUser):
    pass
class TokenData(BaseModel):
    id:Optional[str]=None
class Token(BaseModel):
    access_token:str
    token_type:str