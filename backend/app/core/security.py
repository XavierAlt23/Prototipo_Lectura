"""
Utilidades de seguridad.
"""


def get_password_hash(password: str) -> str:
    """Placeholder para hashing de contrasenas cuando se habilite auth."""
    return password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Placeholder para verificacion de contrasenas."""
    return plain_password == hashed_password
