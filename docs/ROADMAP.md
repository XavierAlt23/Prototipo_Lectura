# 📋 Roadmap del Proyecto - Detección de Ciberbullying

## 🎯 Visión General

Este documento describe el plan de desarrollo del sistema de detección automática de ciberbullying, dividido en 7 fases secuenciales que van desde la preparación de datos hasta el despliegue en producción.

---

## 📅 Fases del Proyecto

### **Fase 1: Preparación de Datos (Semana 1-2)**

**Objetivo:** Obtener, explorar y preparar el dataset

**Tareas:**
- [ ] Descargar dataset "A Labeled Spanish Twitter Dataset for Binary Cyberbullying Detection"
- [ ] Verificar integridad: 83,400 tweets etiquetados
- [ ] Realizar Análisis Exploratorio de Datos (EDA)
  - Distribución de clases (0: No Cyberbullying, 1: Cyberbullying)
  - Estadísticas de longitud de textos
  - Palabras más frecuentes por clase
  - Detectar desbalance de clases
- [ ] Implementar `DatasetLoader` en `ml/data/loader.py`
- [ ] Realizar split: 70% train, 15% val, 15% test
- [ ] Guardar datos procesados en `ml/data/processed/`
- [ ] Documentar hallazgos en `docs/DATA_ANALYSIS.md`

**Deliverables:**
- Dataset dividido en train/val/test
- Reporte EDA con visualizaciones
- Código de carga reutilizable

**Métricas:**
- ✓ Dataset intacto y verificado
- ✓ EDA completo
- ✓ Distribución conocida

---

### **Fase 2: Preprocesamiento y Features (Semana 2-3)**

**Objetivo:** Limpiar y normalizar textos, crear features

**Tareas:**
- [ ] Implementar `TextCleaner` en `ml/preprocessing/text_cleaner.py`
  - Remover URLs
  - Remover menciones (@usuario)
  - Remover caracteres especiales
  - Normalizar espacios
  - Opcional: remover acentos
- [ ] Implementar tokenización
- [ ] Implementar pipeline de embeddings pre-entrenados
- [ ] Probar diferentes estrategias de preprocesamiento
- [ ] Crear dataset procesado
- [ ] Implementar data augmentation (opcional)

**Deliverables:**
- Módulo de preprocesamiento robusto
- Dataset procesado y listo para ML
- Notebook con análisis de impacto del preprocesamiento

**Métricas:**
- ✓ Consistencia en limpieza
- ✓ Pérdida mínima de información

---

### **Fase 3: Entrenamiento de Modelos (Semana 4-6)**

**Objetivo:** Entrenar 6 modelos diferentes bajo condiciones experimentales controladas

#### Subtarea 3.1: Setup de Entrenamiento
- [ ] Crear clase base `BaseModel` en `ml/models/base_model.py`
- [ ] Implementar `Trainer` en `ml/training/trainer.py`
- [ ] Configurar logging y checkpointing
- [ ] Implementar callbacks (early stopping, learning rate scheduling)
- [ ] Fijar seeds para reproducibilidad

#### Subtarea 3.2: Entrenar Transformers
- [ ] **BETO** en `ml/training/train_beto.py`
  - Modelo: dccuchile/bert-base-spanish-wwm-uncased
  - Parámetros: learning_rate=2e-5, epochs=10, batch_size=16
  - Checkpoint: `ml/checkpoints/beto/beto-v1`
  
- [ ] **DistilBETO** en `ml/training/train_distilbeto.py`
  - Modelo: dccuchile/distilbert-base-spanish-uncased
  - Parámetros: learning_rate=2e-5, epochs=10, batch_size=32
  - Checkpoint: `ml/checkpoints/distilbeto/distilbeto-v1`
  
- [ ] **BERT-M** en `ml/training/train_bert_m.py`
  - Modelo: bert-base-multilingual-uncased
  - Parámetros: learning_rate=2e-5, epochs=10, batch_size=16
  - Checkpoint: `ml/checkpoints/bert-m/bert-m-v1`

#### Subtarea 3.3: Entrenar RNN
- [ ] **BiLSTM** en `ml/training/train_bilstm.py`
  - Embeddings pre-entrenados de BETO
  - Hidden size: 256, num_layers: 2
  - Dropout: 0.3, Learning rate: 1e-3
  - Checkpoint: `ml/checkpoints/bilstm/bilstm-v1`
  
- [ ] **Conv1D-LSTM** en `ml/training/train_conv1d_lstm.py`
  - Conv filters: 100, sizes: (2,3,4,5)
  - LSTM hidden: 128, bidirectional: True
  - Checkpoint: `ml/checkpoints/conv1d_lstm/conv1d_lstm-v1`

#### Subtarea 3.4: Entrenar CNN
- [ ] **CNN** en `ml/training/train_cnn.py`
  - Conv layers: 3, kernel sizes: 3,4,5
  - Channels: 100
  - Checkpoint: `ml/checkpoints/cnn/cnn-v1`

**Deliverables:**
- 6 modelos entrenados con checkpoints guardados
- Logs de entrenamiento con métricas por epoch
- Configuración reproducible de cada modelo

**Métricas:**
- ✓ Convergencia observada en validación
- ✓ Sin overfitting evidente

---

### **Fase 4: Evaluación y Comparación (Semana 7)**

**Objetivo:** Evaluar todos los modelos bajo métricas consistentes y compararlos

**Tareas:**
- [ ] Implementar cálculo de métricas en `ml/evaluation/metrics.py`
  - Accuracy, Precision, Recall, F1-Score
  - Matriz de Confusión
  - ROC-AUC
  - Specificity, Sensitivity
  
- [ ] Generar matrices de confusión para cada modelo
  
- [ ] Generar curvas ROC para cada modelo
  
- [ ] Implementar comparador en `ml/evaluation/comparator.py`
  - Crear tabla comparativa
  - Identificar mejor modelo
  - Análisis de fortalezas/debilidades
  
- [ ] Guardar resultados en base de datos
  
- [ ] Generar reporte de evaluación en `docs/EVALUATION_RESULTS.md`
  - Tablas comparativas
  - Gráficos
  - Análisis de resultados
  - Recomendaciones

**Deliverables:**
- Tabla comparativa de todos los modelos
- Gráficos de ROC y matrices de confusión
- Reporte de evaluación detallado
- Datos en base de datos para consultas posteriores

**Métricas:**
- ✓ Todas las métricas calculadas correctamente
- ✓ Resultados documentados

---

### **Fase 5: API y Backend (Semana 8)**

**Objetivo:** Crear API REST para servir predicciones

**Tareas:**
- [ ] Configurar FastAPI en `backend/app/main.py`
  
- [ ] Implementar modelos SQLAlchemy en `backend/app/models/`
  - Experiments
  - Predictions
  - ModelMetrics
  - ConfusionMatrices
  
- [ ] Crear endpoints en `backend/app/api/`
  - `/health` - Health check
  - `POST /predictions/predict` - Predicción individual
  - `POST /predictions/batch` - Predicción en lote
  - `GET /predictions/history` - Historial
  - `GET /models` - Listar modelos
  - `GET /models/{id}/metrics` - Métricas
  - `POST /models/compare` - Comparar modelos
  
- [ ] Implementar `MLService` para predicciones
  
- [ ] Configurar CORS
  
- [ ] Crear schemas Pydantic para validación
  
- [ ] Implement autenticación básica (opcional)
  
- [ ] Tests de API con pytest

**Deliverables:**
- API REST funcional
- Endpoints documentados con Swagger
- Tests de cobertura

**Métricas:**
- ✓ Todos los endpoints funcionan
- ✓ Predicciones consistentes
- ✓ Tests pasando

---

### **Fase 6: Frontend (Semana 9-10)**

**Objetivo:** Crear interfaz de usuario con React

**Tareas:**
- [ ] Configurar React + Vite
  
- [ ] Crear estructura de componentes
  
- [ ] Implementar páginas principales
  - Dashboard: Resumen general
  - Prediction: Interfaz de predicción
  - Models: Comparativa de modelos
  - Analytics: Análisis de resultados
  
- [ ] Implementar stores con Zustand
  - `predictionStore.js`
  - `modelStore.js`
  
- [ ] Crear cliente HTTP con Axios
  
- [ ] Diseñar interfaz con Tailwind CSS
  - Form de entrada
  - Resultados con visualización
  - Tablas de comparación
  - Gráficos
  
- [ ] Implementar error handling
  
- [ ] Tests con Vitest

**Deliverables:**
- Frontend funcional y responsive
- Integración completa con API
- Tests de componentes

**Métricas:**
- ✓ UI funcional y usable
- ✓ Integración correcta con backend

---

### **Fase 7: Despliegue (Semana 11)**

**Objetivo:** Preparar sistema para producción

**Tareas:**
- [ ] Dockerizar backend
  - Crear `backend/Dockerfile`
  - Probar construcción y ejecución
  
- [ ] Dockerizar frontend
  - Crear `frontend/Dockerfile`
  - Probar construcción y ejecución
  
- [ ] Crear `docker-compose.yml`
  - Servicio PostgreSQL
  - Servicio Backend
  - Servicio Frontend
  - Volúmenes persistentes
  
- [ ] Tests de integración
  - Verificar conectividad entre servicios
  - Verificar base de datos
  - Predicciones end-to-end
  
- [ ] Documentación final
  - `SETUP.md` - Cómo instalar
  - `DEPLOYMENT.md` - Cómo desplegar
  - `TROUBLESHOOTING.md` - Problemas comunes
  
- [ ] Optimizaciones de performance (opcional)

**Deliverables:**
- Sistema totalmente containerizado
- Documentación de despliegue
- Checklist de verificación

**Métricas:**
- ✓ Sistema funcional en Docker
- ✓ Documentación completa

---

## 📊 Timeline Visual

```
Semana 1  |████| Fase 1: Preparación Datos
Semana 2  |████| Fase 2: Preprocesamiento (inicio)
Semana 3  |████| Fase 2: Preprocesamiento (fin) + Fase 3 (inicio)
Semana 4  |████| Fase 3: Entrenamiento Transformers
Semana 5  |████| Fase 3: Entrenamiento RNN/CNN
Semana 6  |████| Fase 3: Ajustes finales
Semana 7  |████| Fase 4: Evaluación
Semana 8  |████| Fase 5: Backend/API
Semana 9  |████| Fase 6: Frontend (inicio)
Semana 10 |████| Fase 6: Frontend (fin)
Semana 11 |████| Fase 7: Despliegue
```

---

## 🔄 Dependencias Entre Fases

```
Fase 1 (Datos)
    ↓
Fase 2 (Preprocesamiento)
    ↓
Fase 3 (Entrenamiento) ←────────────┐
    ↓                                │
Fase 4 (Evaluación) ────────────────┤ (Puede iterarse)
    ↓                                │
Fase 5 (API) ─────────────────────────┤
    ↓                                │
Fase 6 (Frontend) ──────────────────────→ usa modelos y API
    ↓
Fase 7 (Despliegue)
```

---

## ✅ Criterios de Éxito

### Fase 1
- [ ] Dataset de 83.4k tweets completamente descargado
- [ ] Distribución de clases documentada
- [ ] Split train/val/test realizado correctamente

### Fase 2
- [ ] Textos limpios sin artefactos
- [ ] Tokens generados correctamente
- [ ] Embeddings funcionales

### Fase 3
- [ ] 6 modelos convergidos
- [ ] Checkpoints guardados y verificados
- [ ] Logs de entrenamiento completos

### Fase 4
- [ ] Todos los modelos evaluados
- [ ] Tabla comparativa generada
- [ ] Modelo ganador identificado

### Fase 5
- [ ] API respondiendo a predicciones
- [ ] Base de datos funcionando
- [ ] Tests pasando

### Fase 6
- [ ] Frontend cargando correctamente
- [ ] Predicciones mostradas en UI
- [ ] Integración API-Frontend funcional

### Fase 7
- [ ] Docker Compose levanta todos los servicios
- [ ] Sistema accesible en localhost
- [ ] Documentación lista

---

## 🎓 Documentación a Generar

1. **README.md** - Descripción general (✓ Completado)
2. **DATABASE.md** - Esquema de BD (✓ Completado)
3. **API.md** - Documentación de endpoints (✓ Completado)
4. **ARCHITECTURE.md** - Arquitectura del sistema
5. **DATA_ANALYSIS.md** - Análisis exploratorio
6. **EVALUATION_RESULTS.md** - Resultados de evaluación
7. **SETUP.md** - Guía de instalación
8. **DEPLOYMENT.md** - Guía de despliegue
9. **TROUBLESHOOTING.md** - Problemas comunes
10. **CONTRIBUTING.md** - Guía para contribuciones

---

## 📌 Notas Importantes

- **Reproducibilidad**: Fijar seeds en toda etapa
- **Versionado**: Guardar checkpoints con versión
- **Logging**: Registrar todo para debugging
- **Testing**: Escribir tests mientras se desarrolla
- **Documentación**: Documentar durante desarrollo
- **Control de Versiones**: Commits frecuentes y descriptivos

---

**Última actualización:** 8 de junio de 2024  
**Estado:** En Desarrollo  
**Versión:** 1.0
