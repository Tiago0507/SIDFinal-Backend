from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from ..dependencies import get_mongo_db
from ..schemas.mongo_schemas import (
    ProductBase,
    ProductCreate,
    Product
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

@router.get("/products/{product_id}", response_model=ProductBase) # con problemas
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