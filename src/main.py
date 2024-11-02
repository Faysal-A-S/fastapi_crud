from fastapi import FastAPI,HTTPException,Depends
import uvicorn 
from src.models.userModels import Users
from sqlalchemy import text
from src.schemas.users import UserOut,UserUpdate,UserIn
from src.database.databaseSQL import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@app.get("/users", response_model=List[UserOut])
def user_list(db: Session = Depends(get_db)):
    data = db.query(Users).all()
    return data

@app.post("/users/",response_model=UserOut)
def create_user(user_data:UserIn,db: Session = Depends(get_db)):
    user = Users()
    user.name = user_data.name
    user.email = user_data.email
    user.phone = user_data.phone
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users/{id}",response_model=UserOut)
def user(id:int,db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id==id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User with given id doesn't exists") 
    return user     
    

@app.put("/users/{id}",response_model=UserOut)
def update_user(id: int, data: UserUpdate,db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id==id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="Data with the given id not found.") 
    for key,value in data.dict(exclude_unset=True).items():
        setattr(user,key,value)
    db.commit()
    db.refresh(user)    
    return user
    

@app.delete("/users/{id}")
def delete_user(id:int,db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id==id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User with the given id not found")    
    db.delete(user)
    db.commit()
    return {"message":"Data deleted"}



if __name__ == "__main__":
    uvicorn.run(
        "src.main:app", host="127.0.0.1", port=8000, reload=True, log_level="info"
    )