"""
Validadores reutilizables.
"""


def validate_text_length(text: str, min_length: int = 5, max_length: int = 500) -> bool:
    return min_length <= len(text.strip()) <= max_length
