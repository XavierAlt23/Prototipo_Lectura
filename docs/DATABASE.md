# 🗄️ Diseño de Base de Datos PostgreSQL

## Descripción General

La base de datos está diseñada para almacenar:
1. Información de experimentos (entrenamientos)
2. Resultados de predicciones
3. Métricas de evaluación
4. Historias de modelos entrenados

---

## 📊 Esquema de Tablas

### Tabla: `experiments`

Almacena información sobre cada experimento de entrenamiento.

```sql
CREATE TABLE experiments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    model_type VARCHAR(100) NOT NULL,  -- 'beto', 'distilbeto', 'bert-m', 'bilstm', 'conv1d_lstm', 'cnn'
    description TEXT,
    hyperparameters JSONB,  -- Almacenar parámetros en JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'running', 'completed', 'failed'
    checkpoint_path VARCHAR(500),  -- Ruta al modelo guardado
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT,
    auc_roc FLOAT,
    training_time_seconds INT
);

CREATE INDEX idx_experiments_model_type ON experiments(model_type);
CREATE INDEX idx_experiments_status ON experiments(status);
```

---

### Tabla: `predictions`

Almacena cada predicción realizada.

```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    experiment_id INT NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    input_text VARCHAR(500) NOT NULL,
    prediction INT NOT NULL CHECK (prediction IN (0, 1)),  -- 0: No-cyberbullying, 1: Cyberbullying
    confidence FLOAT CHECK (confidence >= 0 AND confidence <= 1),
    execution_time_ms INT,  -- Tiempo de inferencia en ms
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_correct BOOLEAN,  -- NULL si no se conoce la etiqueta real
    actual_label INT CHECK (actual_label IN (0, 1))
);

CREATE INDEX idx_predictions_experiment_id ON predictions(experiment_id);
CREATE INDEX idx_predictions_created_at ON predictions(created_at);
```

---

### Tabla: `model_metrics`

Almacena métricas calculadas para cada experimento.

```sql
CREATE TABLE model_metrics (
    id SERIAL PRIMARY KEY,
    experiment_id INT NOT NULL UNIQUE REFERENCES experiments(id) ON DELETE CASCADE,
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT,
    auc_roc FLOAT,
    specificity FLOAT,
    sensitivity FLOAT,
    mcc FLOAT,  -- Matthews Correlation Coefficient
    threshold FLOAT DEFAULT 0.5,
    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Tabla: `confusion_matrices`

Almacena matrices de confusión.

```sql
CREATE TABLE confusion_matrices (
    id SERIAL PRIMARY KEY,
    experiment_id INT NOT NULL UNIQUE REFERENCES experiments(id) ON DELETE CASCADE,
    true_negatives INT,
    false_positives INT,
    false_negatives INT,
    true_positives INT,
    total_samples INT,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Tabla: `roc_curves`

Almacena datos para curvas ROC.

```sql
CREATE TABLE roc_curves (
    id SERIAL PRIMARY KEY,
    experiment_id INT NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    fpr FLOAT ARRAY,  -- False Positive Rate
    tpr FLOAT ARRAY,  -- True Positive Rate
    thresholds FLOAT ARRAY,
    auc FLOAT,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Tabla: `model_comparisons`

Comparativa entre modelos.

```sql
CREATE TABLE model_comparisons (
    id SERIAL PRIMARY KEY,
    comparison_name VARCHAR(255) NOT NULL,
    model_1_id INT NOT NULL REFERENCES experiments(id),
    model_2_id INT NOT NULL REFERENCES experiments(id),
    winner_id INT REFERENCES experiments(id),  -- ID del modelo ganador
    comparison_metric VARCHAR(100),  -- Métrica usada para comparación
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);
```

---

## 🔄 Relaciones

```
experiments (1) ──→ (many) predictions
experiments (1) ──→ (one)  model_metrics
experiments (1) ──→ (one)  confusion_matrices
experiments (1) ──→ (many) roc_curves
experiments (many) ──→ (many) model_comparisons
```

---

## 📝 Script de Inicialización

```sql
-- Crear base de datos
CREATE DATABASE cyberbullying_detection OWNER postgres;

-- Conectar a la base de datos
\c cyberbullying_detection

-- Crear esquema
CREATE SCHEMA IF NOT EXISTS public;

-- Crear tabla de experiments
CREATE TABLE experiments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    model_type VARCHAR(100) NOT NULL,
    description TEXT,
    hyperparameters JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    checkpoint_path VARCHAR(500),
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT,
    auc_roc FLOAT,
    training_time_seconds INT
);

CREATE INDEX idx_experiments_model_type ON experiments(model_type);
CREATE INDEX idx_experiments_status ON experiments(status);

-- Crear tabla de predictions
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    experiment_id INT NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    input_text VARCHAR(500) NOT NULL,
    prediction INT NOT NULL CHECK (prediction IN (0, 1)),
    confidence FLOAT CHECK (confidence >= 0 AND confidence <= 1),
    execution_time_ms INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_correct BOOLEAN,
    actual_label INT CHECK (actual_label IN (0, 1))
);

CREATE INDEX idx_predictions_experiment_id ON predictions(experiment_id);
CREATE INDEX idx_predictions_created_at ON predictions(created_at);

-- Crear tabla de model_metrics
CREATE TABLE model_metrics (
    id SERIAL PRIMARY KEY,
    experiment_id INT NOT NULL UNIQUE REFERENCES experiments(id) ON DELETE CASCADE,
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT,
    auc_roc FLOAT,
    specificity FLOAT,
    sensitivity FLOAT,
    mcc FLOAT,
    threshold FLOAT DEFAULT 0.5,
    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de confusion_matrices
CREATE TABLE confusion_matrices (
    id SERIAL PRIMARY KEY,
    experiment_id INT NOT NULL UNIQUE REFERENCES experiments(id) ON DELETE CASCADE,
    true_negatives INT,
    false_positives INT,
    false_negatives INT,
    true_positives INT,
    total_samples INT,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de roc_curves
CREATE TABLE roc_curves (
    id SERIAL PRIMARY KEY,
    experiment_id INT NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    fpr FLOAT ARRAY,
    tpr FLOAT ARRAY,
    thresholds FLOAT ARRAY,
    auc FLOAT,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de model_comparisons
CREATE TABLE model_comparisons (
    id SERIAL PRIMARY KEY,
    comparison_name VARCHAR(255) NOT NULL,
    model_1_id INT NOT NULL REFERENCES experiments(id),
    model_2_id INT NOT NULL REFERENCES experiments(id),
    winner_id INT REFERENCES experiments(id),
    comparison_metric VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

-- Crear usuario para la aplicación
CREATE USER cyberbullying_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE cyberbullying_detection TO cyberbullying_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO cyberbullying_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cyberbullying_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO cyberbullying_user;
```

---

## 🔍 Consultas Útiles

### Top 5 modelos por F1-Score
```sql
SELECT name, model_type, f1_score, accuracy, precision, recall
FROM experiments
WHERE status = 'completed'
ORDER BY f1_score DESC
LIMIT 5;
```

### Predicciones incorrectas
```sql
SELECT p.*, e.name, e.model_type
FROM predictions p
JOIN experiments e ON p.experiment_id = e.id
WHERE p.is_correct = FALSE
LIMIT 10;
```

### Estadísticas por modelo
```sql
SELECT 
    model_type,
    COUNT(*) as total_experiments,
    AVG(accuracy) as avg_accuracy,
    AVG(f1_score) as avg_f1,
    MAX(accuracy) as max_accuracy
FROM experiments
WHERE status = 'completed'
GROUP BY model_type
ORDER BY avg_f1 DESC;
```

### Predicciones por día
```sql
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_predictions,
    SUM(CASE WHEN is_correct = TRUE THEN 1 ELSE 0 END) as correct,
    ROUND(100.0 * SUM(CASE WHEN is_correct = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as accuracy_pct
FROM predictions
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

---

## 🛡️ Seguridad

- Validación de constraints en nivel de base de datos
- Índices en columnas frecuentemente consultadas
- ON DELETE CASCADE para mantener integridad referencial
- Separación de usuarios y permisos
