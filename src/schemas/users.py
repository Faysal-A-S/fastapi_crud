from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email:str
    phone:str

class UserIn(UserBase):
    pass

class UserOut(UserBase):
    id: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone:Optional[str]  = None