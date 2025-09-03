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
class AuthorInfo(BaseModel):
    id:int
    email:EmailStr

class CreateArticle(BaseModel):
    title:str
    content:str


class ResArticle(BaseModel):
    id:int
    title:str
    content:str


class TokenData(BaseModel):
    id:Optional[str]=None
class Token(BaseModel):
    access_token:str
    token_type:str

class LoginRequest(BaseModel):
    email:EmailStr
    password:str
