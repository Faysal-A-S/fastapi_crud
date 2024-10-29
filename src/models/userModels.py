from sqlalchemy import Column,Integer,String
from database.databaseSQL import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    city = Column(String)
    age = Column(Integer)