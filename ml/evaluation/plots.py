"""
Funciones para visualizaciones de evaluacion.
"""


def confusion_matrix_payload(matrix) -> dict:
    return {"matrix": matrix}
