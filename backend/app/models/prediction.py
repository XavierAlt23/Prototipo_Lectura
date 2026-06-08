"""
backend/app/models/prediction.py
Modelos SQLAlchemy para BD
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON
from datetime import datetime
from app.db.database import Base


class Experiment(Base):
    """Modelo de experimento (entrenamiento)"""
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    model_type = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    hyperparameters = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="pending")
    checkpoint_path = Column(String(500), nullable=True)
    accuracy = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    auc_roc = Column(Float, nullable=True)
    training_time_seconds = Column(Integer, nullable=True)


class Prediction(Base):
    """Modelo de predicción"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"), nullable=False)
    input_text = Column(String(500), nullable=False)
    prediction = Column(Integer, nullable=False)  # 0 o 1
    confidence = Column(Float, nullable=False)
    execution_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_correct = Column(Boolean, nullable=True)
    actual_label = Column(Integer, nullable=True)


class ModelMetric(Base):
    """Modelo de métricas"""
    __tablename__ = "model_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"), nullable=False)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    auc_roc = Column(Float)
    specificity = Column(Float)
    sensitivity = Column(Float)
    mcc = Column(Float)
    threshold = Column(Float, default=0.5)
    evaluated_at = Column(DateTime, default=datetime.utcnow)
