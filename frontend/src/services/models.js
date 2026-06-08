import api from './api.js';

export const fetchModels = () => api.getModels();
export const fetchModelMetrics = (modelId) => api.getModelMetrics(modelId);
