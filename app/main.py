from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import (
    auth_router,
    catalog_router,
    companies_router,
    contracts_router,
    equipment_router,
    opportunities_router
)
from .config.database import engine
from .models import Base

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tech Rental API",
    description="API para sistema de alquiler de equipos tecnológicos",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router)
app.include_router(catalog_router)
app.include_router(companies_router)
app.include_router(contracts_router)
app.include_router(equipment_router)
app.include_router(opportunities_router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a Tech Rental API"}