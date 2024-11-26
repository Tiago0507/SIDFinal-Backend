from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import date

# MongoDB Schemas
class ProductSpecs(BaseModel):
    processor: Optional[str]
    ram: Optional[str]
    storage: Optional[str]
    graphics: Optional[str]
    screen_size: Optional[str]
    os: Optional[str]
    battery_life: Optional[str]
    camera: Optional[str]
    printer_technology: Optional[str]
    connectivity: Optional[List[str]]
    other_specs: Optional[Dict[str, str]]

class ProductBase(BaseModel):
    name: str
    category: str
    brand: str
    model: str
    description: str = Field(..., description="Descripción detallada del producto")
    specs: ProductSpecs
    price: float
    stock: int
    warranty_period: str
    release_date: date
    image_urls: List[str]

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: str

    class Config:
        from_attributes = True

# Inventory Schemas
class InventoryItemBase(BaseModel):
    product_id: str
    inventory_code: str
    serial_number: str
    status: str  # available, rented, maintenance, retired
    condition: str
    purchase_date: date
    warranty_end: date
    location: str

class MaintenanceRecord(BaseModel):
    date: date
    type: str
    description: str
    technician: str

class InventoryItem(InventoryItemBase):
    maintenance_history: List[MaintenanceRecord] = []

    class Config:
        from_attributes = True

# Rental Request Schemas
class RentalItemRequest(BaseModel):
    product_id: str
    quantity: int
    rental_period: Dict[str, date]  # {"start_date": date, "end_date": date}
    price_agreement: Optional[float]

class DeliveryAddress(BaseModel):
    street: str
    city: str
    state: str
    zip: str

class RentalRequestBase(BaseModel):
    client_nit: str
    contact_id: str
    items: List[RentalItemRequest]
    notes: Optional[str]
    delivery_address: DeliveryAddress
    status: str = "pending"  # pending, approved, rejected, fulfilled

class RentalRequest(RentalRequestBase):
    request_id: str
    request_date: date

    class Config:
        from_attributes = True