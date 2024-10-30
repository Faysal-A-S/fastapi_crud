from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    age: int
    city: str

class UserIn(UserBase):
    id: int

class UserOut(UserBase):
    id: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    city:Optional[str]  = None