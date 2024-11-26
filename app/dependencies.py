from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .config.database import SessionLocal, mongodb
from .models import UserAccount
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_mongo_db():
    return mongodb

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserAccount:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            os.getenv('SECRET_KEY'),
            algorithms=[os.getenv('ALGORITHM')]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(UserAccount).filter(UserAccount.username == username).first()
    if user is None:
        raise credentials_exception
    return user