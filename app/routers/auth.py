from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..dependencies import get_db, get_mongo_db, get_current_user
from ..schemas import UserAccountCreate, UserAccount, Token
from ..models import UserAccount as UserAccountModel
from ..core.security import create_access_token, get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserAccount)
def create_user(user: UserAccountCreate, db: Session = Depends(get_db)):
    db_user = UserAccountModel(
        user_id=f"U{datetime.now().strftime('%Y%m%d%H%M%S')}",
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password),
        nit=user.nit,
        created_at=datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserAccountModel).filter(UserAccountModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}