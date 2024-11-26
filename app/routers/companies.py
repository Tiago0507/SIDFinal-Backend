from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..dependencies import get_db, get_mongo_db, get_current_user
from ..schemas import CompanyCreate, Company, Contact, ContactCreate
from ..models.postgres_models import (
    Company as CompanyModel, 
    Contact as ContactModel,
    UserAccount
)

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("/", response_model=List[Company])
def get_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    return db.query(CompanyModel).offset(skip).limit(limit).all()

@router.get("/{nit}", response_model=Company)
def get_company(
    nit: str,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    company = db.query(CompanyModel).filter(CompanyModel.nit == nit).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.get("/{nit}/contacts", response_model=List[Contact])
def get_company_contacts(
    nit: str,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    return db.query(ContactModel).filter(ContactModel.nit == nit).all()