from fastapi import FastAPI,HTTPException,Depends
import uvicorn 
import models.userModels
from sqlalchemy import text
from schemas.users import UserOut,UserUpdate,UserIn
from database.databaseSQL import engine,SessionLocal
from sqlalchemy.orm import Session
import models
from typing import List
app = FastAPI()

models.userModels.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@app.get("/users", response_model=List[UserOut])
def user_list(db: Session = Depends(get_db)):
    data = db.query(models.userModels.Users).all()
    return data

@app.post("/users/",response_model=UserOut)
def create_user(user:UserIn,db: Session = Depends(get_db)):
    userCheck =db.query(models.userModels.Users).filter(models.userModels.Users.id==user.id).first()
    if userCheck is not None:
        raise HTTPException(status_code=403,detail="User with same id already exists")
    userModel = models.userModels.Users()
    userModel.id=user.id
    userModel.name = user.name
    userModel.age = user.age
    userModel.city = user.city
    db.add(userModel)
    db.commit()
    db.refresh(userModel)
    return userModel


@app.get("/users/{id}",response_model=UserOut)
def user(id:int,db: Session = Depends(get_db)):
    userModel = db.query(models.userModels.Users).filter(models.userModels.Users.id==id).first()
    if userModel is None:
        raise HTTPException(status_code=404, detail="User with given id doesn't exists") 
    return userModel     
    

@app.put("/users/{id}",response_model=UserOut)
def update_user(id: int, data: UserUpdate,db: Session = Depends(get_db)):
    userModel = db.query(models.userModels.Users).filter(models.userModels.Users.id==id).first()

    if userModel is None:
        raise HTTPException(status_code=404, detail="Data with the given id not found.") 
    for key,value in data.dict(exclude_unset=True).items():
        setattr(userModel,key,value)
    db.commit()
    db.refresh(userModel)    
    return userModel
    

@app.delete("/users/{id}")
def delete_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.userModels.Users).filter(models.userModels.Users.id==id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User with the given id not found")    
    db.delete(user)
    db.commit()
    return {"message":"Data deleted"}



if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="127.0.0.1", port=8000, reload=True, log_level="info"
    )