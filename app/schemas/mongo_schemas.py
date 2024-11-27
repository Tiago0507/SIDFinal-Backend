from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# MongoDB Schemas
class ProductSpecs(BaseModel):
    processor: Optional[str] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    graphics: Optional[str] = None
    screen_size: Optional[str] = None
    os: Optional[str] = None
    battery_life: Optional[str] = None
    camera: Optional[str] = None
    printer_technology: Optional[str] = None
    connectivity: Optional[List[str]] = None
    other_specs: Optional[Dict[str, str]] = None
    raid_support: Optional[str] = None
    redundant_power: Optional[str] = None
    remote_management: Optional[str] = None

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
    release_date: datetime
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
    purchase_date: datetime
    warranty_end: datetime
    location: str

class MaintenanceRecord(BaseModel):
    date: datetime
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
    rental_period: Dict[str, datetime]  # {"start_date": date, "end_date": date}
    price_agreement: Optional[float]

class DeliveryAddress(BaseModel):
    street: str
    city: str
    state: str
    zip: str

class RentalRequestBase(BaseModel):
    request_id: str  
    request_date: datetime
    client_nit: str
    contact_id: str
    items: List[RentalItemRequest]
    notes: Optional[str]
    delivery_address: DeliveryAddress
    status: str = "pending"  # pending, approved, rejected, fulfilled

class RentalRequest(RentalRequestBase):
    request_id: str
    request_date: datetime

    class Config:
        from_attributes = True
        
class DetailedProcessorSpecs(BaseModel):
    model: str
    cores: int
    threads: int
    base_clock: str
    turbo_clock: str

class DetailedMemorySpecs(BaseModel):
    type: str
    speed: str
    max_capacity: str

class DetailedStorageSpecs(BaseModel):
    type: str
    interface: str
    read_speed: str
    write_speed: str

class Benchmark(BaseModel):
    name: str
    score: int
    date_tested: str

class DetailedSpecs(BaseModel):
    processor: DetailedProcessorSpecs
    memory: DetailedMemorySpecs
    storage: DetailedStorageSpecs
    benchmarks: List[Benchmark]
    certifications: List[str]