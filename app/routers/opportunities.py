from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..dependencies import get_db, get_mongo_db, get_current_user
from ..schemas import OpportunityCreate, Opportunity
from ..models import Opportunity as OpportunityModel
from ..models.postgres_models import (
    Opportunity as OpportunityModel,
    UserAccount
)

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])

@router.get("/", response_model=List[Opportunity])
def get_opportunities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    return db.query(OpportunityModel).filter(
        OpportunityModel.nit == current_user.nit
    ).offset(skip).limit(limit).all()

@router.post("/", response_model=Opportunity)
def create_opportunity(
    opportunity: OpportunityCreate,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    db_opportunity = OpportunityModel(**opportunity.dict())
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity