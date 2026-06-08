"""
backend/app/schemas/prediction.py
Schemas Pydantic para validación de requests
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PredictionRequest(BaseModel):
    """Request para predicción individual"""
    text: str = Field(..., min_length=5, max_length=500, description="Texto a clasificar")
    model_id: int = Field(..., description="ID del modelo a usar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Eres un imbécil, no sirves para nada",
                "model_id": 1
            }
        }


class BatchPredictionRequest(BaseModel):
    """Request para predicción en lote"""
    texts: List[str] = Field(..., min_length=1, max_length=100, description="Lista de textos")
    model_id: int = Field(..., description="ID del modelo a usar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "texts": [
                    "Eres un imbécil",
                    "Hola, ¿cómo estás?"
                ],
                "model_id": 1
            }
        }


class PredictionResponse(BaseModel):
    """Response de predicción"""
    prediction: int = Field(..., description="Clase predicha (0 o 1)")
    confidence: float = Field(..., description="Confianza de la predicción")
    class_label: str = Field(..., description="Etiqueta legible de la clase")
    model_name: str = Field(..., description="Nombre del modelo usado")
    execution_time_ms: int = Field(..., description="Tiempo de ejecución en ms")
    timestamp: datetime = Field(..., description="Timestamp de la predicción")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction": 1,
                "confidence": 0.95,
                "class_label": "Cyberbullying",
                "model_name": "beto-v1",
                "execution_time_ms": 245,
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }


class BatchPredictionResponse(BaseModel):
    """Response de predicción en lote"""
    class SinglePrediction(BaseModel):
        text: str
        prediction: int
        confidence: float
        class_label: str
    
    predictions: List[SinglePrediction]
    total_time_ms: int
    timestamp: datetime
