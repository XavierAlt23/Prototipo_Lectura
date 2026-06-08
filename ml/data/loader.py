"""
ml/data/loader.py
Módulo para carga y gestión de datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict
from sklearn.model_selection import train_test_split
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class DatasetLoader:
    """
    Cargador de dataset de Twitter para detección de ciberbullying en español.
    
    Dataset: "A Labeled Spanish Twitter Dataset for Binary Cyberbullying Detection"
    """
    
    def __init__(self, data_path: str, test_size: float = 0.15, val_size: float = 0.15, random_seed: int = 42):
        """
        Args:
            data_path: Ruta al archivo CSV del dataset
            test_size: Proporción de datos para test (0-1)
            val_size: Proporción de datos para validación (0-1)
            random_seed: Semilla para reproducibilidad
        """
        self.data_path = Path(data_path)
        self.test_size = test_size
        self.val_size = val_size
        self.random_seed = random_seed
        self.df = None
        self.stats = {}
        
    def load(self) -> pd.DataFrame:
        """Carga el dataset desde CSV"""
        logger.info(f"Cargando dataset desde {self.data_path}")
        
        try:
            self.df = pd.read_csv(self.data_path)
            logger.info(f"Dataset cargado: {len(self.df)} registros")
            self._log_statistics()
            return self.df
        except FileNotFoundError:
            logger.error(f"Archivo no encontrado: {self.data_path}")
            raise
    
    def _log_statistics(self):
        """Registra estadísticas del dataset"""
        self.stats = {
            'total_samples': len(self.df),
            'non_cyberbullying': (self.df['label'] == 0).sum(),
            'cyberbullying': (self.df['label'] == 1).sum(),
            'avg_text_length': self.df['text'].str.len().mean(),
            'max_text_length': self.df['text'].str.len().max(),
            'min_text_length': self.df['text'].str.len().min(),
        }
        
        logger.info(f"Estadísticas del dataset:")
        logger.info(f"  - Total de muestras: {self.stats['total_samples']}")
        logger.info(f"  - No cyberbullying (0): {self.stats['non_cyberbullying']}")
        logger.info(f"  - Cyberbullying (1): {self.stats['cyberbullying']}")
        logger.info(f"  - Promedio de longitud: {self.stats['avg_text_length']:.2f}")
        
    def split_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Divide el dataset en train, val y test
        
        Returns:
            Tupla de (train_df, val_df, test_df)
        """
        if self.df is None:
            self.load()
        
        # Primer split: train + val vs test
        train_val, test = train_test_split(
            self.df,
            test_size=self.test_size,
            random_state=self.random_seed,
            stratify=self.df['label']
        )
        
        # Segundo split: train vs val
        train_size = 1 - (self.val_size / (1 - self.test_size))
        train, val = train_test_split(
            train_val,
            train_size=train_size,
            random_state=self.random_seed,
            stratify=train_val['label']
        )
        
        logger.info(f"Dataset dividido:")
        logger.info(f"  - Train: {len(train)} ({len(train)/len(self.df)*100:.1f}%)")
        logger.info(f"  - Val: {len(val)} ({len(val)/len(self.df)*100:.1f}%)")
        logger.info(f"  - Test: {len(test)} ({len(test)/len(self.df)*100:.1f}%)")
        
        return train, val, test
    
    def get_class_weights(self, split: pd.DataFrame) -> Dict[int, float]:
        """
        Calcula pesos de clases para balancear el dataset
        Útil para entrenamientos con clases desbalanceadas
        """
        class_counts = split['label'].value_counts()
        total = len(split)
        weights = {
            0: total / (class_counts[0] * 2),
            1: total / (class_counts[1] * 2)
        }
        logger.info(f"Pesos de clases: {weights}")
        return weights


# Ejemplo de uso
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    loader = DatasetLoader(
        data_path="data/raw/dataset.csv",
        test_size=0.15,
        val_size=0.15,
        random_seed=42
    )
    
    df = loader.load()
    train, val, test = loader.split_data()
    weights = loader.get_class_weights(train)
    
    print(f"\nDatos de entrenamiento:")
    print(f"  - Positivos: {(train['label'] == 1).sum()}")
    print(f"  - Negativos: {(train['label'] == 0).sum()}")
