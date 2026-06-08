"""
backend/app/utils/logger.py
Configuración de logging
"""

import logging
from app.core.config import settings


def setup_logging():
    """Configura el sistema de logging"""
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
