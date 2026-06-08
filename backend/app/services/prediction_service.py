"""
Servicio para persistir y consultar predicciones.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.prediction import Prediction


class PredictionService:
    def __init__(self, db: Session):
        self.db = db

    def create_prediction(
        self,
        *,
        experiment_id: int,
        input_text: str,
        prediction: int,
        confidence: float,
        execution_time_ms: Optional[int] = None,
    ) -> Prediction:
        record = Prediction(
            experiment_id=experiment_id,
            input_text=input_text,
            prediction=prediction,
            confidence=confidence,
            execution_time_ms=execution_time_ms,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
