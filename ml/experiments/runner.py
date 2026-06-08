"""
Ejecutor simple de experimentos.
"""


def run_experiment(config: dict) -> dict:
    return {"name": config.get("name", "experiment"), "status": "pending"}
