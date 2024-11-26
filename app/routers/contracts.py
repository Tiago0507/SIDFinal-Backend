from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..dependencies import get_db, get_mongo_db, get_current_user
from ..schemas import ContractCreate, Contract, DeliveryCertificateCreate, DeliveryCertificate
from ..models.postgres_models import (
    Contract as ContractModel, 
    DeliveryCertificate as DeliveryCertificateModel,
    UserAccount
)

router = APIRouter(prefix="/contracts", tags=["Contracts"])

@router.get("/", response_model=List[Contract])
def get_user_contracts(
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    return db.query(ContractModel).filter(ContractModel.nit == current_user.nit).all()

@router.get("/{contract_id}", response_model=Contract)
def get_contract(
    contract_id: str,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    contract = db.query(ContractModel).filter(
        ContractModel.contract_id == contract_id,
        ContractModel.nit == current_user.nit
    ).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@router.get("/{contract_id}/certificates", response_model=List[DeliveryCertificate])
def get_contract_certificates(
    contract_id: str,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    contract = db.query(ContractModel).filter(
        ContractModel.contract_id == contract_id,
        ContractModel.nit == current_user.nit
    ).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract.delivery_certificates