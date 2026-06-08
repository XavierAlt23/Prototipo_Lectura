"""
Schemas Pydantic para informacion de modelos.
"""

from typing import Optional

from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    id: int
    name: str
    model_type: str
    status: str = "active"
    accuracy: Optional[float] = None
    f1_score: Optional[float] = None


class ModelMetrics(BaseModel):
    model_id: int
    accuracy: Optional[float] = Field(default=None)
    precision: Optional[float] = Field(default=None)
    recall: Optional[float] = Field(default=None)
    f1_score: Optional[float] = Field(default=None)
    auc_roc: Optional[float] = Field(default=None)
