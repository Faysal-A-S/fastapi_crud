from sqlalchemy import Column,Integer,String
from src.database.databaseSQL import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(255))