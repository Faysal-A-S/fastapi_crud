from fastapi import FastAPI,HTTPException,Depends
import uvicorn 
from database.database import read_json_file,write_json_file
import models.userModels
from schemas.users import UserCreate,UserUpdate
from database.databaseSQL import engine,SessionLocal
from sqlalchemy.orm import Session
import models
app = FastAPI()

models.userModels.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@app.get("/users")
def user_list(db: Session = Depends(get_db)):
    userlist = db.query(models.userModels.Users).all()
    print(db.query(models.userModels.Users).all())
    return {"data":userlist}

@app.get("/users/{id}")
def user(id:int,db: Session = Depends(get_db)):
    userModel = db.query(models.userModels.Users).filter(models.userModels.Users.id==id).first()
    if userModel is None:
        raise HTTPException(status_code=404, detail="User with given id doesn't exists") 
    return [{"data":userModel}]      
    

@app.post("/users/")
def create_user(user:UserCreate,db: Session = Depends(get_db)):
    userModel = models.userModels.Users()
    userModel.id=user.id
    userModel.name = user.name
    userModel.age = user.age
    userModel.city = user.city
    db.add(userModel)
    db.commit()
    db.refresh(userModel)
    return [{"data":userModel}]


@app.put("/users/{id}")
def update_user(id: int, data: UserUpdate,db: Session = Depends(get_db)):
    userModel = db.query(models.userModels.Users).filter(models.userModels.Users.id==id).first()

    if userModel is None:
        raise HTTPException(status_code=404, detail="Data with the given id not found.")    

@app.delete("/users/{id}")
def delete_user(id:int):
    userlist = read_json_file()
    deletedUser={}
    for index,user in enumerate(userlist):
        if user["id"]== id:
            deletedUser=userlist[index]
            del userlist[index]
            write_json_file(userlist)
            return {"message":deletedUser}
    raise HTTPException(status_code=404,detail="User with the given id not found")    

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="127.0.0.1", port=8000, reload=True, log_level="info"
    )