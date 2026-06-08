# Sistema de Detección Automática de Ciberbullying en Redes Sociales en Español

## 📋 Descripción del Proyecto

Sistema académico de investigación y desarrollo para detectar automáticamente mensajes de ciberbullying escritos en español utilizando técnicas avanzadas de Procesamiento de Lenguaje Natural (NLP) y modelos de Deep Learning.

### Objetivo Principal
Desarrollar y evaluar un conjunto de modelos de machine learning capaces de clasificar automáticamente tweets en español como cyberbullying o no-cyberbullying, comparando el rendimiento de diferentes arquitecturas de redes neuronales y modelos transformers.

---

## 📊 Dataset

**Fuente:** "A Labeled Spanish Twitter Dataset for Binary Cyberbullying Detection"

- **Cantidad de registros:** ~83,400 tweets etiquetados
- **Clasificación:** Binaria (0: No Cyberbullying, 1: Cyberbullying)
- **Idioma:** Español
- **Plataforma:** Twitter

---

## 🧠 Modelos a Implementar

### Transformers
- **BETO**: BERT optimizado para español
- **DistilBETO**: Versión destilada de BETO (más eficiente)
- **BERT-M**: Modelo multilingual

### Redes Neuronales Recurrentes
- **BiLSTM**: Bidirectional Long Short-Term Memory
- **Conv1D-LSTM**: Convolución 1D + LSTM
- **CNN**: Red neuronal convolucional para clasificación de texto

---

## 📈 Métricas de Evaluación

- **Accuracy**: Precisión general del modelo
- **Precision**: Capacidad de no generar falsos positivos
- **Recall**: Capacidad de detectar todos los casos positivos
- **F1-Score**: Media armónica de precisión y recall
- **Matriz de Confusión**: Distribución de predicciones vs. etiquetas reales
- **Curvas ROC**: Análisis del trade-off entre tasa de verdaderos positivos y falsos positivos
- **AUC-ROC**: Área bajo la curva ROC

---

## 🛠️ Tecnologías

### Backend
```
Python 3.11
FastAPI (Framework web asincrónico)
SQLAlchemy (ORM)
Pydantic (Validación de datos)
```

### Machine Learning
```
PyTorch (Framework de deep learning)
Hugging Face Transformers (Modelos pre-entrenados)
Scikit-Learn (Métricas y utilidades ML)
SpaCy (Procesamiento avanzado de NLP)
Pandas (Manipulación de datos)
NumPy (Computación numérica)
```

### Base de Datos
```
PostgreSQL (BD relacional)
Alembic (Migraciones de base de datos)
```

### Frontend
```
React 18+
Vite (Build tool)
Tailwind CSS (Estilos)
React Router (Enrutamiento)
Zustand (State management)
Axios (HTTP client)
```

### DevOps & Testing
```
Docker (Containerización)
Docker Compose (Orquestación de servicios)
pytest (Testing)
Git/GitHub (Control de versiones)
```

---

## 📁 Estructura del Proyecto

```
Prototipo_Lectura/
├── backend/                     # Backend FastAPI
│   ├── app/
│   │   ├── api/                # Endpoints REST
│   │   │   ├── __init__.py
│   │   │   ├── predictions.py  # Endpoint de predicciones
│   │   │   ├── models.py       # Endpoint de gestión de modelos
│   │   │   └── health.py       # Health check
│   │   ├── core/               # Configuración central
│   │   │   ├── __init__.py
│   │   │   ├── config.py       # Variables de ambiente
│   │   │   └── security.py     # Autenticación y autorización
│   │   ├── schemas/            # Modelos Pydantic (validación)
│   │   │   ├── __init__.py
│   │   │   ├── prediction.py   # Schema de predicción
│   │   │   └── model_info.py   # Schema de info de modelos
│   │   ├── models/             # Modelos SQLAlchemy (BD)
│   │   │   ├── __init__.py
│   │   │   ├── prediction.py   # Modelo BD de predicciones
│   │   │   └── experiment.py   # Modelo BD de experimentos
│   │   ├── db/                 # Base de datos
│   │   │   ├── __init__.py
│   │   │   ├── database.py     # Configuración de conexión
│   │   │   ├── session.py      # Session factory
│   │   │   └── migrations/     # Migraciones Alembic
│   │   ├── services/           # Lógica de negocio
│   │   │   ├── __init__.py
│   │   │   ├── ml_service.py   # Servicio de ML
│   │   │   └── prediction_service.py  # Servicio de predicciones
│   │   ├── utils/              # Funciones utilitarias
│   │   │   ├── __init__.py
│   │   │   ├── logger.py       # Configuración de logging
│   │   │   └── validators.py   # Validadores personalizados
│   │   ├── main.py             # Aplicación principal
│   │   └── __init__.py
│   ├── tests/                  # Tests unitarios e integración
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   ├── test_services.py
│   │   └── conftest.py
│   ├── requirements.txt        # Dependencias Python
│   ├── .env.example           # Ejemplo de variables de ambiente
│   └── Dockerfile            # Imagen Docker para backend
│
├── ml/                        # Módulo de Machine Learning
│   ├── data/                 # Gestión de datasets
│   │   ├── __init__.py
│   │   ├── loader.py         # Carga de datasets
│   │   ├── splitter.py       # División train/val/test
│   │   └── raw/              # Datos crudos
│   │
│   ├── preprocessing/        # Preprocesamiento de texto
│   │   ├── __init__.py
│   │   ├── text_cleaner.py   # Limpieza de texto
│   │   ├── tokenizer.py      # Tokenización
│   │   ├── embeddings.py     # Generación de embeddings
│   │   └── utils.py
│   │
│   ├── models/              # Definición de modelos
│   │   ├── __init__.py
│   │   ├── transformer_models.py   # BETO, DistilBETO, BERT-M
│   │   ├── lstm_models.py          # BiLSTM, Conv1D-LSTM
│   │   ├── cnn_model.py            # CNN para texto
│   │   └── base_model.py           # Clase base
│   │
│   ├── training/            # Scripts de entrenamiento
│   │   ├── __init__.py
│   │   ├── trainer.py        # Clase entrenadora
│   │   ├── train_beto.py     # Entrenamiento específico BETO
│   │   ├── train_bilstm.py   # Entrenamiento específico BiLSTM
│   │   ├── train_cnn.py      # Entrenamiento específico CNN
│   │   └── callbacks.py      # Callbacks (early stopping, etc.)
│   │
│   ├── evaluation/          # Evaluación de modelos
│   │   ├── __init__.py
│   │   ├── metrics.py        # Cálculo de métricas
│   │   ├── plots.py          # Visualizaciones
│   │   ├── comparator.py     # Comparación de modelos
│   │   └── reports.py        # Generación de reportes
│   │
│   ├── experiments/         # Gestión de experimentos
│   │   ├── __init__.py
│   │   ├── config.yaml       # Configuración de experimentos
│   │   ├── runner.py         # Ejecutor de experimentos
│   │   └── results/          # Resultados de experimentos
│   │
│   ├── checkpoints/         # Modelos entrenados guardados
│   │   ├── beto/
│   │   ├── bilstm/
│   │   └── cnn/
│   │
│   ├── requirements.txt      # Dependencias ML
│   └── config.yaml          # Configuración global ML
│
├── frontend/               # Frontend React + Vite
│   ├── src/
│   │   ├── components/     # Componentes reutilizables
│   │   │   ├── Layout/
│   │   │   ├── Forms/
│   │   │   ├── Charts/
│   │   │   └── Common/
│   │   ├── pages/          # Páginas principales
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Prediction.jsx
│   │   │   ├── Models.jsx
│   │   │   └── Analytics.jsx
│   │   ├── services/       # Clientes HTTP
│   │   │   ├── api.js      # Configuración base
│   │   │   ├── predictions.js
│   │   │   └── models.js
│   │   ├── stores/         # Estado global (Zustand)
│   │   │   ├── predictionStore.js
│   │   │   └── modelStore.js
│   │   ├── utils/          # Utilidades
│   │   │   ├── formatters.js
│   │   │   └── validators.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── public/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── .env.example
│   └── Dockerfile
│
├── docs/                   # Documentación
│   ├── ARCHITECTURE.md     # Arquitectura del sistema
│   ├── DATABASE.md         # Diseño de BD
│   ├── API.md             # Documentación de endpoints
│   ├── MODELS.md          # Descripción de modelos
│   ├── SETUP.md           # Guía de instalación
│   ├── WORKFLOW.md        # Flujo de trabajo
│   └── ROADMAP.md         # Hoja de ruta del proyecto
│
├── config/                 # Archivos de configuración
│   ├── docker-compose.yml  # Orquestación de servicios
│   ├── nginx.conf         # Configuración Nginx (opcional)
│   └── postgres_init.sql  # Script inicial de BD
│
├── scripts/               # Scripts de utilidad
│   ├── download_dataset.sh      # Descarga dataset
│   ├── setup_environment.sh     # Setup inicial
│   ├── train_all_models.sh      # Entrena todos los modelos
│   ├── evaluate_models.sh       # Evalúa modelos
│   └── generate_reports.sh      # Genera reportes
│
├── .gitignore
├── .env.example
└── docker-compose.yml
```

---

## 🗄️ Diseño de Base de Datos PostgreSQL

### Tabla: `experiments`
```sql
CREATE TABLE experiments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    model_type VARCHAR(100) NOT NULL,  -- 'beto', 'bilstm', 'cnn', etc.
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),  -- 'running', 'completed', 'failed'
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT
);
```

### Tabla: `predictions`
```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    text VARCHAR(500) NOT NULL,
    model_id INT REFERENCES experiments(id),
    prediction INT NOT NULL,  -- 0 o 1
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_correct BOOLEAN
);
```

### Tabla: `model_metrics`
```sql
CREATE TABLE model_metrics (
    id SERIAL PRIMARY KEY,
    experiment_id INT REFERENCES experiments(id),
    metric_name VARCHAR(100),  -- 'accuracy', 'precision', etc.
    metric_value FLOAT,
    threshold FLOAT DEFAULT 0.5
);
```

### Tabla: `confusion_matrix`
```sql
CREATE TABLE confusion_matrix (
    id SERIAL PRIMARY KEY,
    experiment_id INT REFERENCES experiments(id),
    true_negatives INT,
    false_positives INT,
    false_negatives INT,
    true_positives INT
);
```

---

## 🔌 Endpoints REST (FastAPI)

### Health Check
```
GET /api/v1/health
Respuesta: { "status": "healthy", "timestamp": "2024-01-01T12:00:00Z" }
```

### Predicción Simple
```
POST /api/v1/predictions/predict
Body: { "text": "Eres un imbécil", "model_id": 1 }
Respuesta: {
    "prediction": 1,
    "confidence": 0.95,
    "model": "beto",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### Predicción por Lotes
```
POST /api/v1/predictions/batch
Body: {
    "texts": ["texto1", "texto2"],
    "model_id": 1
}
Respuesta: {
    "predictions": [
        {"text": "texto1", "prediction": 0, "confidence": 0.92},
        {"text": "texto2", "prediction": 1, "confidence": 0.87}
    ]
}
```

### Listar Modelos
```
GET /api/v1/models
Respuesta: [
    {
        "id": 1,
        "name": "beto-v1",
        "type": "transformer",
        "accuracy": 0.89,
        "f1_score": 0.87
    }
]
```

### Métricas de Modelo
```
GET /api/v1/models/{model_id}/metrics
Respuesta: {
    "accuracy": 0.89,
    "precision": 0.88,
    "recall": 0.86,
    "f1_score": 0.87,
    "confusion_matrix": {
        "tn": 1200, "fp": 150, "fn": 180, "tp": 1070
    }
}
```

---

## 🔄 Flujo Completo del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    FASE 1: DATOS                             │
├─────────────────────────────────────────────────────────────┤
│  Dataset Raw (83.4k tweets) → Loader → Split (70/15/15)    │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              FASE 2: PREPROCESAMIENTO                        │
├─────────────────────────────────────────────────────────────┤
│  Limpieza → Tokenización → Embeddings → Vectorización       │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│            FASE 3: ENTRENAMIENTO (Paralelo)                │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ BETO         │  │ BiLSTM       │  │ CNN          │      │
│  │ DistilBETO   │  │ Conv1D-LSTM  │  │              │      │
│  │ BERT-M       │  └──────────────┘  └──────────────┘      │
│  └──────────────┘                                           │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│             FASE 4: EVALUACIÓN Y COMPARACIÓN               │
├─────────────────────────────────────────────────────────────┤
│  Métricas → Matriz de Confusión → Curvas ROC → Reportes   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  FASE 5: API (FastAPI)                      │
├─────────────────────────────────────────────────────────────┤
│  Carga de Modelos → Inferencia → Base de Datos            │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              FASE 6: FRONTEND (React + Vite)               │
├─────────────────────────────────────────────────────────────┤
│  Dashboard → Predicción Individual → Análisis de Modelos   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Roadmap por Fases

### **Fase 1: Preparación de Datos (Semana 1-2)**
- [ ] Descargar y explorar dataset
- [ ] Análisis exploratorio de datos (EDA)
- [ ] Implementar data loader
- [ ] Implementar splitting (train/val/test)
- [ ] Análisis de distribución de clases

### **Fase 2: Preprocesamiento y Features (Semana 2-3)**
- [ ] Implementar text cleaner
- [ ] Implementar tokenizador
- [ ] Crear embeddings pre-entrenados
- [ ] Implementar data augmentation
- [ ] Guardar features preprocessados

### **Fase 3: Entrenamiento de Modelos (Semana 4-6)**
- [ ] Implementar base model class
- [ ] Entrenar BETO
- [ ] Entrenar DistilBETO
- [ ] Entrenar BERT-M
- [ ] Entrenar BiLSTM
- [ ] Entrenar Conv1D-LSTM
- [ ] Entrenar CNN
- [ ] Guardar checkpoints

### **Fase 4: Evaluación (Semana 7)**
- [ ] Implementar métricas
- [ ] Generar matrices de confusión
- [ ] Generar curvas ROC
- [ ] Comparar modelos
- [ ] Generar reportes

### **Fase 5: API y Backend (Semana 8)**
- [ ] Configurar FastAPI
- [ ] Implementar base de datos
- [ ] Implementar endpoints de predicción
- [ ] Implementar endpoints de modelos
- [ ] Implementar autenticación (opcional)
- [ ] Tests de API

### **Fase 6: Frontend (Semana 9-10)**
- [ ] Configurar React + Vite
- [ ] Implementar dashboard
- [ ] Implementar formulario de predicción
- [ ] Implementar tabla de resultados
- [ ] Implementar gráficos de métricas
- [ ] Integración con API

### **Fase 7: Despliegue (Semana 11)**
- [ ] Dockerizar backend y frontend
- [ ] Configurar docker-compose
- [ ] Tests de integración
- [ ] Desplegar en servidor
- [ ] Documentación final

---

## ✨ Buenas Prácticas Implementadas

### Clean Architecture
- Separación clara de capas: `api`, `services`, `models`, `db`
- Dependencias apuntan hacia el centro
- Lógica de negocio independiente de frameworks

### SOLID
- **S**ingle Responsibility: Cada clase tiene una única responsabilidad
- **O**pen/Closed: Extensible sin modificación
- **L**iskov Substitution: Base model intercambiable
- **I**nterface Segregation: Interfaces específicas por use case
- **D**ependency Inversion: Inyección de dependencias

### Modularidad
- Módulos independientes: `ml`, `backend`, `frontend`
- Servicios reutilizables
- Componentes aislados

### Reproducibilidad
- Seeds fijos para random
- Versiones de dependencias fijas
- Configuración centralizada
- Logging detallado de experimentos
- Checkpoints guardados con metadatos

### Configuración
- Variables de ambiente en `.env`
- Archivos `config.yaml` para experimentos
- Configuración por entorno (dev, test, prod)

---

## 🚀 Primeros Pasos

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd Prototipo_Lectura

# 2. Ejecutar setup inicial
bash scripts/setup_environment.sh

# 3. Descargar dataset
bash scripts/download_dataset.sh

# 4. Entrenar modelos
bash scripts/train_all_models.sh

# 5. Evaluar modelos
bash scripts/evaluate_models.sh

# 6. Generar reportes
bash scripts/generate_reports.sh

# 7. Iniciar API y frontend
docker-compose up
```

---

**Documento generado:** 8 de junio de 2024  
**Versión:** 1.0  
**Estado:** En desarrollo
