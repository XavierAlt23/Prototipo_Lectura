# Workflow

1. Cargar dataset en `ml/data/raw`.
2. Dividir datos con `ml/data/splitter.py`.
3. Limpiar y tokenizar textos desde `ml/preprocessing`.
4. Entrenar modelos con scripts en `ml/training`.
5. Evaluar resultados en `ml/evaluation`.
6. Exponer inferencia desde `backend`.
7. Consumir la API desde `frontend`.
