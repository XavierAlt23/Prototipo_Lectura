"""
backend/app/main.py
Aplicación FastAPI principal
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.api import predictions, models, experiments, health
from app.db.database import engine, Base
from app.utils.logger import setup_logging

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager para eventos de startup y shutdown
    """
    # Startup
    logger.info("Iniciando aplicación...")
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown
    logger.info("Cerrando aplicación...")


# Crear aplicación
app = FastAPI(
    title="Cyberbullying Detection API",
    description="API para detección automática de ciberbullying en español",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(predictions.router, prefix="/api/v1", tags=["Predictions"])
app.include_router(models.router, prefix="/api/v1", tags=["Models"])
app.include_router(experiments.router, prefix="/api/v1", tags=["Experiments"])


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Welcome to Cyberbullying Detection API",
        "docs": "/docs",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG
    )
