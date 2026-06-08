# config/postgres_init.sql

-- Crear base de datos
CREATE DATABASE cyberbullying_detection OWNER cyberbullying_user;

-- Conectar a la base de datos
\c cyberbullying_detection

-- Crear tablas
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

-- Crear índices
CREATE INDEX idx_experiments_model_type ON experiments(model_type);
CREATE INDEX idx_experiments_status ON experiments(status);
CREATE INDEX idx_predictions_experiment_id ON predictions(experiment_id);
CREATE INDEX idx_predictions_created_at ON predictions(created_at);

-- Asignar permisos
GRANT ALL PRIVILEGES ON DATABASE cyberbullying_detection TO cyberbullying_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO cyberbullying_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cyberbullying_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO cyberbullying_user;
