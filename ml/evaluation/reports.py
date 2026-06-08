"""
Generacion de reportes de evaluacion.
"""


def build_markdown_report(metrics: dict) -> str:
    lines = ["# Reporte de Evaluacion", ""]
    lines.extend(f"- {key}: {value}" for key, value in metrics.items())
    return "\n".join(lines)
