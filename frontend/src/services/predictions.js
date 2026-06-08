import api from './api.js';

export const predictText = (text, modelId) => api.predict(text, modelId);
export const predictBatch = (texts, modelId) => api.batchPredict(texts, modelId);
