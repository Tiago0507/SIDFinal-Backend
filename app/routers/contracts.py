from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from ..dependencies import get_db, get_mongo_db, get_current_user
from ..schemas import (
    ContractCreate,
    Contract,
    DeliveryCertificateCreate,
    DeliveryCertificate,
    Equipment
)
from ..models.postgres_models import (
    Contract as ContractModel,
    DeliveryCertificate as DeliveryCertificateModel,
    Equipment as EquipmentModel,
    UserAccount
)

router = APIRouter(prefix="/contracts", tags=["Contracts"])

# Obtener contratos del usuario
@router.get("/", response_model=List[Contract])
def get_user_contracts(
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    return db.query(ContractModel).filter(ContractModel.nit == current_user.nit).all()

# Obtener contrato específico
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

# Crear contrato a partir de una solicitud aprobada
@router.post("/from-request/{request_id}", response_model=Contract)
async def create_contract_from_request(
    request_id: str,
    contract_create: ContractCreate,
    db: Session = Depends(get_db),
    mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
    current_user: UserAccount = Depends(get_current_user)
):
    # 1. Verificar la solicitud
    rental_request = await mongo_db.rental_requests.find_one({"request_id": request_id})
    if not rental_request:
        raise HTTPException(status_code=404, detail="Rental request not found")
    if rental_request["status"] != "approved":
        raise HTTPException(status_code=400, detail="Rental request is not approved")

    # 2. Crear el contrato manejando las fechas correctamente
    start_date = rental_request["items"][0]["rental_period"]["start_date"]
    end_date = rental_request["items"][0]["rental_period"]["end_date"]
    
    # Si las fechas ya son objetos datetime, las convertimos a date
    if isinstance(start_date, datetime):
        start_date = start_date.date()
    if isinstance(end_date, datetime):
        end_date = end_date.date()

    contract = ContractModel(
        contract_id=f"CTR-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        nit=rental_request["client_nit"],
        contract_number=contract_create.contract_number,
        start_date=start_date,
        end_date=end_date,
        monthly_value=contract_create.monthly_value
    )
    
    db.add(contract)
    db.commit()
    db.refresh(contract)

    # 3. Actualizar estado de la solicitud
    await mongo_db.rental_requests.update_one(
        {"_id": request_id},
        {"$set": {"status": "fulfilled", "contract_id": contract.contract_id}}
    )

    return contract

# Crear certificado de entrega
@router.post("/{contract_id}/certificates", response_model=DeliveryCertificate)
async def create_delivery_certificate(
    contract_id: str,
    certificate: DeliveryCertificateCreate,
    db: Session = Depends(get_db),
    mongo_db: AsyncIOMotorClient = Depends(get_mongo_db),
    current_user: UserAccount = Depends(get_current_user)
):
    # 1. Verificar contrato
    print(current_user.nit)
    print(contract_id)
    contract = db.query(ContractModel).filter(
        ContractModel.contract_id == contract_id,
        ContractModel.nit == certificate.nit
    ).first()
    
    print(contract)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    # 2. Crear certificado
    db_certificate = DeliveryCertificateModel(
        certificate_id=f"DC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        contract_id=contract_id,
        delivery_date=certificate.delivery_date,
        notes=certificate.notes,
        nit=certificate.nit
    )
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)

    # 3. Verificar rental request asociado
    rental_request = await mongo_db.rental_requests.find_one({"contract_id": contract_id})
    if rental_request:
        # 4. Actualizar inventario para cada ítem
        for item in rental_request["items"]:
            # Encontrar equipos disponibles
            inventory_items = await mongo_db.inventory.find({
                "product_id": item["product_id"],
                "status": "available"
            }).limit(item["quantity"]).to_list(length=item["quantity"])

            # Marcar equipos como rentados
            for inv_item in inventory_items:
                await mongo_db.inventory.update_one(
                    {"_id": inv_item["_id"]},
                    {
                        "$set": {
                            "status": "rented",
                            "current_contract_id": contract_id,
                            "current_certificate_id": db_certificate.certificate_id
                        }
                    }
                )

                # Crear registro de equipo en PostgreSQL
                equipment = EquipmentModel(
                    equipment_id=f"EQ-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    certificate_id=db_certificate.certificate_id,
                    inventory_code=inv_item["inventory_code"],
                    description=f"Equipo asignado del inventario {inv_item['_id']}",
                    active=True
                )
                db.add(equipment)

    db.commit()
    return db_certificate

# Obtener certificados de un contrato
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

# Obtener equipos de un certificado
@router.get("/certificates/{certificate_id}/equipment", response_model=List[Equipment])
def get_certificate_equipment(
    certificate_id: str,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    equipment = db.query(EquipmentModel).filter(
        EquipmentModel.certificate_id == certificate_id
    ).all()
    return equipment