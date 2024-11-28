from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from ..dependencies import get_mongo_db, get_current_user
from ..schemas.mongo_schemas import (
    ProductBase,
    ProductCreate,
    Product,
    ProductSpecs,
    DetailedSpecs,
    InventoryItem,
    RentalRequest,
    RentalRequestBase,
)

router = APIRouter(prefix="/catalog", tags=["Product Catalog"])

@router.get("/products", response_model=List[ProductBase])
async def get_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    query = {}
    if category:
        query["category"] = category
    if brand:
        query["brand"] = brand
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price

    products = await db.products.find(query).to_list(1000)
    return products

@router.get("/products/{product_id}", response_model=ProductBase) 
async def get_product(
    product_id: str,
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    product = await db.products.find_one({"_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/categories")
async def get_categories(
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    categories = await db.products.distinct("category")
    return categories

@router.get("/brands")
async def get_brands(
    category: Optional[str] = None,
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    query = {}
    if category:
        query["category"] = category
    brands = await db.products.distinct("brand", query)
    return brands

@router.post("/products", response_model=ProductBase)
async def create_product(
    product: ProductBase,
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    result = await db.products.insert_one(product.dict())
    created_product = await db.products.find_one({"_id": result.inserted_id})
    return created_product

@router.put("/products/{product_id}", response_model=ProductBase)
async def update_product(
    product_id: str,
    product: ProductBase,
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    result = await db.products.update_one(
        {"_id": product_id},
        {"$set": product.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = await db.products.find_one({"_id": product_id})
    return updated_product

@router.get("/specifications/{product_id}/detailed", response_model=DetailedSpecs)
async def get_detailed_specifications(
    product_id: str,
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    detailed_specs = await db.equipment_specifications.find_one({"product_id": product_id})
    if not detailed_specs:
        raise HTTPException(status_code=404, detail="Detailed specifications not found")
    
    return {
        **detailed_specs["detailed_specs"],
        "benchmarks": detailed_specs["benchmarks"],
        "certifications": detailed_specs["certifications"]
    }

@router.get("/inventory", response_model=List[InventoryItem])
async def get_inventory(
    status: Optional[str] = None,
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    query = {}
    if status:
        query["status"] = status
    inventory = await db.inventory.find(query).to_list(1000)
    return inventory

@router.get("/inventory/{inventory_id}", response_model=InventoryItem)
async def get_inventory_item(
    inventory_id: str,
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    item = await db.inventory.find_one({"_id": inventory_id})
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item

@router.get("/rental-requests", response_model=List[RentalRequest])
async def get_rental_requests(
    client_nit: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncIOMotorClient = Depends(get_mongo_db),
    current_user = Depends(get_current_user)
):
    query = {}
    if client_nit:
        query["client_nit"] = client_nit
    if status:
        query["status"] = status
    
    requests = await db.rental_requests.find(query).to_list(1000)
    return requests

@router.post("/rental-requests", response_model=RentalRequest)
async def create_rental_request(
    request: RentalRequestBase,
    db: AsyncIOMotorClient = Depends(get_mongo_db),
    current_user = Depends(get_current_user)
):
    new_request = request.dict()
    new_request["request_date"] = datetime.now()  # Añade la fecha actual
    result = await db.rental_requests.insert_one(new_request)

    # Recupera el documento insertado
    created_request = await db.rental_requests.find_one({"_id": result.inserted_id})
    
    # Mapea _id a request_id
    created_request["request_id"] = str(created_request["_id"])
    del created_request["_id"]  # Elimina _id si no es necesario

    return created_request

@router.get("/rental-requests/{request_id}", response_model=RentalRequest)
async def get_rental_request(
    request_id: str,
    db: AsyncIOMotorClient = Depends(get_mongo_db),
    current_user = Depends(get_current_user)
):
    request = await db.rental_requests.find_one({"request_id": request_id})
    if not request:
        raise HTTPException(status_code=404, detail="Rental request not found")
    return request

@router.patch("/rental-requests/{request_id}", response_model=RentalRequest)
async def update_rental_request_status(
    request_id: str,
    status: str,
    db: AsyncIOMotorClient = Depends(get_mongo_db),
    current_user = Depends(get_current_user)
):
    if status not in ["pending", "approved", "rejected", "fulfilled"]:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    # Actualización del estado, usando request_id directamente como string
    result = await db.rental_requests.update_one(
        {"request_id": request_id},  # Usamos request_id que es un string
        {"$set": {"status": status}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Rental request not found")
        
    # Obtener el documento actualizado usando request_id
    updated_request = await db.rental_requests.find_one({"request_id": request_id})  # Usamos request_id aquí también
    return updated_request