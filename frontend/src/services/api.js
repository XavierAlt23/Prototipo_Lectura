"""
frontend/src/services/api.js
Cliente HTTP para comunicación con el backend
"""

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Health Check
  health: () => apiClient.get('/health'),
  
  // Predicciones
  predict: (text, modelId) => 
    apiClient.post('/predictions/predict', {
      text,
      model_id: modelId,
    }),
  
  batchPredict: (texts, modelId) =>
    apiClient.post('/predictions/batch', {
      texts,
      model_id: modelId,
    }),
  
  getPredictionHistory: (limit = 100, offset = 0, modelId = null) =>
    apiClient.get('/predictions/history', {
      params: { limit, offset, model_id: modelId },
    }),
  
  // Modelos
  getModels: () => apiClient.get('/models'),
  
  getModel: (modelId) => apiClient.get(`/models/${modelId}`),
  
  getModelMetrics: (modelId) => apiClient.get(`/models/${modelId}/metrics`),
  
  compareModels: (model1Id, model2Id, metric = 'f1_score') =>
    apiClient.post('/models/compare', {
      model_1_id: model1Id,
      model_2_id: model2Id,
      metric,
    }),
  
  // Experimentos
  getExperiments: (status = null, modelType = null) =>
    apiClient.get('/experiments', {
      params: { status, model_type: modelType },
    }),
  
  getExperiment: (experimentId) => apiClient.get(`/experiments/${experimentId}`),
};

export default api;
