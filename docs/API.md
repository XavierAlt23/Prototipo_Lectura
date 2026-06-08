# 🔌 Documentación de Endpoints REST (FastAPI)

## Base URL
```
http://localhost:8000/api/v1
```

---

## 🏥 Health Check

### GET /health
Verifica el estado de la API.

**Request:**
```bash
GET /health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0"
}
```

---

## 🤖 Predicciones

### POST /predictions/predict
Realiza una predicción individual de cyberbullying.

**Request:**
```json
{
  "text": "Eres un imbécil, no sirves para nada",
  "model_id": 1
}
```

**Response (200 OK):**
```json
{
  "prediction": 1,
  "confidence": 0.95,
  "class_label": "Cyberbullying",
  "model_name": "beto-v1",
  "execution_time_ms": 245,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Text length must be between 10 and 500 characters"
}
```

---

### POST /predictions/batch
Realiza predicciones para múltiples textos.

**Request:**
```json
{
  "texts": [
    "Eres un imbécil",
    "Hola, ¿cómo estás?",
    "Vete a la mierda"
  ],
  "model_id": 1
}
```

**Response (200 OK):**
```json
{
  "predictions": [
    {
      "text": "Eres un imbécil",
      "prediction": 1,
      "confidence": 0.92,
      "class_label": "Cyberbullying"
    },
    {
      "text": "Hola, ¿cómo estás?",
      "prediction": 0,
      "confidence": 0.88,
      "class_label": "No Cyberbullying"
    },
    {
      "text": "Vete a la mierda",
      "prediction": 1,
      "confidence": 0.91,
      "class_label": "Cyberbullying"
    }
  ],
  "total_time_ms": 650,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

---

### GET /predictions/history
Obtiene historial de predicciones.

**Query Parameters:**
- `limit`: Número máximo de resultados (default: 100)
- `offset`: Número de resultados a saltar (default: 0)
- `model_id`: Filtrar por modelo (opcional)
- `from_date`: Filtrar predicciones desde esta fecha (opcional)

**Request:**
```bash
GET /predictions/history?limit=50&offset=0&model_id=1
```

**Response (200 OK):**
```json
{
  "total": 1250,
  "limit": 50,
  "offset": 0,
  "predictions": [
    {
      "id": 1250,
      "text": "Eres un imbécil",
      "prediction": 1,
      "confidence": 0.95,
      "model_name": "beto-v1",
      "created_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

---

## 🧠 Modelos

### GET /models
Lista todos los modelos disponibles.

**Request:**
```bash
GET /models
```

**Response (200 OK):**
```json
{
  "models": [
    {
      "id": 1,
      "name": "beto-v1",
      "model_type": "transformer",
      "status": "active",
      "accuracy": 0.892,
      "f1_score": 0.879,
      "precision": 0.885,
      "recall": 0.873,
      "auc_roc": 0.945,
      "training_date": "2024-01-01T00:00:00Z",
      "checkpoint_path": "checkpoints/beto/beto-v1"
    },
    {
      "id": 2,
      "name": "bilstm-v1",
      "model_type": "recurrent",
      "status": "active",
      "accuracy": 0.875,
      "f1_score": 0.862,
      "precision": 0.870,
      "recall": 0.854,
      "auc_roc": 0.925,
      "training_date": "2024-01-02T00:00:00Z",
      "checkpoint_path": "checkpoints/bilstm/bilstm-v1"
    }
  ]
}
```

---

### GET /models/{model_id}
Obtiene detalles de un modelo específico.

**Request:**
```bash
GET /models/1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "beto-v1",
  "model_type": "transformer",
  "description": "BETO (Spanish BERT) entrenado con dataset de ciberbullying",
  "status": "active",
  "accuracy": 0.892,
  "precision": 0.885,
  "recall": 0.873,
  "f1_score": 0.879,
  "auc_roc": 0.945,
  "training_date": "2024-01-01T00:00:00Z",
  "hyperparameters": {
    "learning_rate": 2e-5,
    "batch_size": 16,
    "epochs": 10,
    "max_length": 128
  }
}
```

---

### GET /models/{model_id}/metrics
Obtiene métricas detalladas de un modelo.

**Request:**
```bash
GET /models/1/metrics
```

**Response (200 OK):**
```json
{
  "model_id": 1,
  "model_name": "beto-v1",
  "metrics": {
    "accuracy": 0.892,
    "precision": 0.885,
    "recall": 0.873,
    "f1_score": 0.879,
    "auc_roc": 0.945,
    "specificity": 0.910,
    "sensitivity": 0.873,
    "mcc": 0.782
  },
  "confusion_matrix": {
    "true_negatives": 7800,
    "false_positives": 800,
    "false_negatives": 900,
    "true_positives": 6500
  },
  "roc_curve": {
    "fpr": [0.0, 0.01, 0.02, ...],
    "tpr": [0.0, 0.85, 0.92, ...],
    "thresholds": [1.0, 0.99, 0.98, ...]
  }
}
```

---

### POST /models/compare
Compara dos modelos.

**Request:**
```json
{
  "model_1_id": 1,
  "model_2_id": 2,
  "metric": "f1_score"
}
```

**Response (200 OK):**
```json
{
  "model_1": {
    "name": "beto-v1",
    "f1_score": 0.879
  },
  "model_2": {
    "name": "bilstm-v1",
    "f1_score": 0.862
  },
  "winner": "beto-v1",
  "difference": 0.017,
  "comparison_metric": "f1_score"
}
```

---

## 📊 Experimentos

### GET /experiments
Lista todos los experimentos.

**Query Parameters:**
- `status`: Filtrar por estado (pending, running, completed, failed)
- `model_type`: Filtrar por tipo de modelo

**Request:**
```bash
GET /experiments?status=completed&model_type=transformer
```

**Response (200 OK):**
```json
{
  "experiments": [
    {
      "id": 1,
      "name": "beto-v1",
      "model_type": "transformer",
      "status": "completed",
      "accuracy": 0.892,
      "f1_score": 0.879,
      "training_time_seconds": 3600,
      "created_at": "2024-01-01T00:00:00Z",
      "completed_at": "2024-01-01T01:00:00Z"
    }
  ]
}
```

---

### GET /experiments/{experiment_id}
Obtiene detalles de un experimento.

**Request:**
```bash
GET /experiments/1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "beto-v1",
  "model_type": "transformer",
  "description": "Primer entrenamiento con BETO",
  "status": "completed",
  "accuracy": 0.892,
  "precision": 0.885,
  "recall": 0.873,
  "f1_score": 0.879,
  "auc_roc": 0.945,
  "training_time_seconds": 3600,
  "hyperparameters": {
    "learning_rate": 2e-5,
    "batch_size": 16,
    "epochs": 10
  },
  "created_at": "2024-01-01T00:00:00Z",
  "completed_at": "2024-01-01T01:00:00Z",
  "checkpoint_path": "checkpoints/beto/beto-v1"
}
```

---

## 📈 Analytics

### GET /analytics/summary
Resumen general de la API.

**Request:**
```bash
GET /analytics/summary
```

**Response (200 OK):**
```json
{
  "total_predictions": 12500,
  "total_experiments": 8,
  "active_models": 6,
  "best_model": {
    "name": "beto-v1",
    "f1_score": 0.879
  },
  "predictions_today": 350,
  "average_confidence": 0.87,
  "models_by_type": {
    "transformer": 3,
    "recurrent": 2,
    "convolutional": 1
  }
}
```

---

### GET /analytics/performance-over-time
Rendimiento de predicciones en el tiempo.

**Query Parameters:**
- `model_id`: ID del modelo (opcional)
- `period`: Período de agrupación (day, week, month)
- `days`: Número de días atrás (default: 30)

**Request:**
```bash
GET /analytics/performance-over-time?model_id=1&period=day&days=30
```

**Response (200 OK):**
```json
{
  "model_name": "beto-v1",
  "period": "day",
  "data": [
    {
      "date": "2024-01-01",
      "total_predictions": 150,
      "accuracy": 0.89,
      "average_confidence": 0.87
    },
    {
      "date": "2024-01-02",
      "total_predictions": 175,
      "accuracy": 0.91,
      "average_confidence": 0.88
    }
  ]
}
```

---

## 🔐 Autenticación

Todos los endpoints pueden requerir autenticación mediante API Key (opcional para MVP).

**Header:**
```
Authorization: Bearer <api_key>
```

---

## ❌ Códigos de Error

| Código | Descripción |
|--------|-------------|
| 200 | Éxito |
| 400 | Solicitud inválida |
| 401 | No autenticado |
| 403 | No autorizado |
| 404 | Recurso no encontrado |
| 422 | Error de validación |
| 500 | Error interno del servidor |

---

## 📝 Ejemplo de Uso con curl

```bash
# Obtener lista de modelos
curl -X GET "http://localhost:8000/api/v1/models"

# Realizar una predicción
curl -X POST "http://localhost:8000/api/v1/predictions/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Eres un imbécil",
    "model_id": 1
  }'

# Obtener métricas de un modelo
curl -X GET "http://localhost:8000/api/v1/models/1/metrics"
```

---

## 📚 Documentación Interactiva

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
