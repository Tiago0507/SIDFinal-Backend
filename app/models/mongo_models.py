from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import date

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