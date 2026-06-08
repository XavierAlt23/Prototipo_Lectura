"""
backend/app/api/predictions.py
Endpoints para predicciones
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datetime import datetime
import logging
import time

from app.schemas.prediction import PredictionRequest, PredictionResponse, BatchPredictionRequest
from app.services.ml_service import MLService
from app.db.database import SessionLocal
from app.models.prediction import Prediction

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/predictions", tags=["predictions"])

ml_service = None


def get_ml_service():
    """Inyección de dependencia para MLService"""
    global ml_service
    if ml_service is None:
        ml_service = MLService()
    return ml_service


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    ml_service: MLService = Depends(get_ml_service)
):
    """
    Realiza una predicción de cyberbullying para un texto individual
    
    Args:
        request: Contiene el texto y ID del modelo
        
    Returns:
        PredictionResponse con la predicción y confianza
    """
    try:
        # Validar longitud del texto
        if len(request.text) < 5 or len(request.text) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text length must be between 5 and 500 characters"
            )
        
        # Realizar predicción
        start_time = time.time()
        prediction = ml_service.predict(
            text=request.text,
            model_id=request.model_id
        )
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Mapear label a nombre legible
        class_label = "Cyberbullying" if prediction['prediction'] == 1 else "No Cyberbullying"
        
        return PredictionResponse(
            prediction=prediction['prediction'],
            confidence=prediction['confidence'],
            class_label=class_label,
            model_name=prediction['model_name'],
            execution_time_ms=execution_time_ms,
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing prediction"
        )


@router.post("/batch")
async def batch_predict(
    request: BatchPredictionRequest,
    ml_service: MLService = Depends(get_ml_service)
):
    """
    Realiza predicciones para múltiples textos
    
    Args:
        request: Lista de textos y ID del modelo
        
    Returns:
        Lista de predicciones
    """
    try:
        if len(request.texts) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Texts list cannot be empty"
            )
        
        if len(request.texts) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum 100 texts per batch"
            )
        
        start_time = time.time()
        predictions = ml_service.batch_predict(
            texts=request.texts,
            model_id=request.model_id
        )
        total_time_ms = int((time.time() - start_time) * 1000)
        
        return {
            "predictions": predictions,
            "total_time_ms": total_time_ms,
            "timestamp": datetime.utcnow()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en predicción por lote: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing batch prediction"
        )


@router.get("/history")
async def get_prediction_history(
    limit: int = 100,
    offset: int = 0,
    model_id: int = None
):
    """
    Obtiene historial de predicciones
    
    Args:
        limit: Número máximo de resultados
        offset: Salto en resultados
        model_id: Filtrar por modelo (opcional)
        
    Returns:
        Lista de predicciones con metadatos
    """
    try:
        db = SessionLocal()
        
        # Construir query
        query = db.query(Prediction)
        if model_id:
            query = query.filter(Prediction.experiment_id == model_id)
        
        # Contar total
        total = query.count()
        
        # Obtener resultados
        predictions = query.order_by(Prediction.created_at.desc()).offset(offset).limit(limit).all()
        
        db.close()
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "predictions": [
                {
                    "id": p.id,
                    "text": p.input_text,
                    "prediction": p.prediction,
                    "confidence": p.confidence,
                    "model_name": "unknown",  # Obtener del DB si es necesario
                    "created_at": p.created_at
                }
                for p in predictions
            ]
        }
    
    except Exception as e:
        logger.error(f"Error obteniendo historial: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving prediction history"
        )
