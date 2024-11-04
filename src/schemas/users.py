from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email:str
    phone:str

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    id: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone:Optional[str]  = None


class LoginUser(BaseModel):
    name: str
    password: str 


class Token(BaseModel):
    access_token: str
    token_type: str        