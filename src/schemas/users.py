from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    age: int
    city: str
class UserUpdate(UserBase):
    name :str =None
    age :int =None
    city: str =None

class UserCreate(UserBase):
    id:int




