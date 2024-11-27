from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import date

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
