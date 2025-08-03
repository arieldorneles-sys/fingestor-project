from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fingestor.backend.app.config.settings import settings
from fingestor.backend.app.config.database import engine, Base

# Importar todos os modelos para que sejam registrados
from .models import user, company, plan, customer, supplier, financial, invoice, billing, sales, integrations

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "FinGestor API - Sistema ERP Financeiro"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Incluir routers
from .routers import auth, customers, dashboard, suppliers, financial

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(customers.router, prefix=f"{settings.API_V1_STR}/customers", tags=["customers"])
app.include_router(suppliers.router, prefix=f"{settings.API_V1_STR}/suppliers", tags=["suppliers"])
app.include_router(financial.router, prefix=f"{settings.API_V1_STR}/financial", tags=["financial"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["dashboard"])

