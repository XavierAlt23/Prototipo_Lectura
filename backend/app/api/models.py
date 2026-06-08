"""
backend/app/api/models.py
Endpoints para gestión de modelos
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/models", tags=["models"])


class ModelComparisonRequest(BaseModel):
    model_1_id: int
    model_2_id: int
    metric: str = "f1_score"


@router.get("")
async def list_models():
    """Lista todos los modelos disponibles"""
    # Implementar consulta a DB
    return {
        "models": [
            {
                "id": 1,
                "name": "beto-v1",
                "model_type": "transformer",
                "status": "active",
                "accuracy": 0.892,
                "f1_score": 0.879
            }
        ]
    }


@router.get("/{model_id}")
async def get_model(model_id: int):
    """Obtiene detalles de un modelo"""
    # Implementar
    return {"id": model_id, "name": "model-name"}


@router.get("/{model_id}/metrics")
async def get_model_metrics(model_id: int):
    """Obtiene métricas de un modelo"""
    # Implementar
    return {
        "model_id": model_id,
        "accuracy": 0.892,
        "precision": 0.885,
        "recall": 0.873,
        "f1_score": 0.879
    }


@router.post("/compare")
async def compare_models(request: ModelComparisonRequest):
    """Compara dos modelos"""
    # Implementar
    return {
        "winner": "model-1",
        "difference": 0.017
    }
