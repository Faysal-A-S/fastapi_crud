from pydantic import BaseModel
from sqlalchemy.orm import Session


from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import APIRouter,Depends
from src.database.databaseSQL import SessionLocal
from src.schemas.users import LoginUser,Token
from src.models.userModels import Users
from datetime import timedelta,datetime
router = APIRouter(
    prefix = "/auth",
    tags=["auth"]
)

SECRET_KEY = "dgfjsdghfsdjhgfsh"
ALGORITHM = "HS256"
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl = "auth/token")

@router.post("/token",response_model = Token)
def login(user_data: LoginUser, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.name == user_data.name).first()
    if not user or not bcrypt_context.verify(user_data.password, user.password):
        print(bcrypt_context.verify(user_data.password, user.password))
        return {"message" : "Couldn't validate"}
        
    token = create_access_token(user.name, user.id, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}
    
        
def create_access_token(name: str,id: int,expire: timedelta):
    encode = {"sub":name,"id":id}
    expires = datetime.utcnow() + expire
    encode.update({"exp": expires})   
    return jwt.encode(encode,SECRET_KEY,algorithm = ALGORITHM)

def create_user():
    pass