"""
Factory de sesiones de base de datos.
"""

from app.db.database import SessionLocal, get_db

__all__ = ["SessionLocal", "get_db"]
