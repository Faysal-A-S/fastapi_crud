from pydantic import BaseModel
from sqlalchemy.orm import Session


from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from fastapi import APIRouter,Depends,HTTPException,status
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
oauth2_scheme = HTTPBearer()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


@router.post("/token",response_model = Token)
def login(user_data: LoginUser, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.name == user_data.name).first()
    if not user or not bcrypt_context.verify(user_data.password, user.password):
        return {"message" : "Couldn't validate"}
        
    token = create_access_token(user.id, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}
    
        
def create_access_token(id: int,expire: timedelta):
    encode = {"id":id}
    expires = datetime.utcnow() + expire
    encode.update({"exp": expires})   
    return jwt.encode(encode,SECRET_KEY,algorithm = ALGORITHM)

def get_current_user(token: HTTPAuthorizationCredentials  = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not logged in",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT validation failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

