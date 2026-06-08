"""
Comparacion de resultados de modelos.
"""


def best_model(results: list[dict], metric: str = "f1_score") -> dict | None:
    if not results:
        return None
    return max(results, key=lambda item: item.get(metric, 0))
