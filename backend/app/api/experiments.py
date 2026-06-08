"""
backend/app/api/experiments.py
Endpoints para gestión de experimentos
"""

from fastapi import APIRouter

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.get("")
async def list_experiments(status: str = None, model_type: str = None):
    """Lista experimentos"""
    return {"experiments": []}


@router.get("/{experiment_id}")
async def get_experiment(experiment_id: int):
    """Obtiene detalles de un experimento"""
    return {"id": experiment_id, "name": "experiment-name"}
