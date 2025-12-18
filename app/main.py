from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import users, rfid, logs
from app.database import SessionLocal
from app.models import HttpLog

app = FastAPI(
    title="SafeWay API",
    description="API para sistema de controle de acesso inteligente",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(rfid.router, prefix="/api/v1/rfid", tags=["rfid"])
app.include_router(logs.router, prefix="/api/v1/logs", tags=["logs"])


@app.get("/")
async def root():
    return {"message": "SafeWay API - Sistema de Controle de Acesso"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
