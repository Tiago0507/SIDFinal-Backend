from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..dependencies import get_db, get_mongo_db, get_current_user
from ..schemas import EquipmentCreate, Equipment, Category, CategoryCreate
from ..models.postgres_models import (
    Contract as ContractModel,
    Equipment as EquipmentModel,
    Category as CategoryModel,
    UserAccount
)

router = APIRouter(prefix="/equipment", tags=["Equipment"])

@router.get("/", response_model=List[Equipment])
def get_all_equipment(
    skip: int = 0, 
    limit: int = 100,
    category_id: str = None,
    active: bool = None,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    query = db.query(EquipmentModel)
    if category_id:
        query = query.filter(EquipmentModel.category_id == category_id)
    if active is not None:
        query = query.filter(EquipmentModel.active == active)
    return query.offset(skip).limit(limit).all()

@router.get("/categories", response_model=List[Category])
def get_categories(db: Session = Depends(get_db)):
    return db.query(CategoryModel).all()

@router.post("/categories", response_model=Category)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    db_category = CategoryModel(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category