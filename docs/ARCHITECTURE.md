# Arquitectura

El proyecto se organiza en tres capas principales:

- `backend`: API FastAPI, persistencia y servicios de inferencia.
- `ml`: carga de datos, preprocesamiento, entrenamiento, evaluacion y checkpoints.
- `frontend`: cliente React/Vite para prediccion, modelos y analitica.

La comunicacion externa del frontend ocurre contra `/api/v1`, expuesto por FastAPI.
