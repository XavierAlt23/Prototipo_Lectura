"""
frontend/src/stores/predictionStore.js
Zustand store para estado de predicciones
"""

import { create } from 'zustand';
import api from '../services/api';

export const usePredictionStore = create((set) => ({
  predictions: [],
  currentPrediction: null,
  loading: false,
  error: null,
  
  // Acciones
  predict: async (text, modelId) => {
    set({ loading: true, error: null });
    try {
      const response = await api.predict(text, modelId);
      set((state) => ({
        currentPrediction: response.data,
        predictions: [response.data, ...state.predictions],
        loading: false,
      }));
      return response.data;
    } catch (error) {
      set({ 
        error: error.message, 
        loading: false 
      });
      throw error;
    }
  },
  
  batchPredict: async (texts, modelId) => {
    set({ loading: true, error: null });
    try {
      const response = await api.batchPredict(texts, modelId);
      set((state) => ({
        predictions: [...response.data.predictions, ...state.predictions],
        loading: false,
      }));
      return response.data;
    } catch (error) {
      set({ 
        error: error.message, 
        loading: false 
      });
      throw error;
    }
  },
  
  loadHistory: async (limit = 50, offset = 0) => {
    set({ loading: true, error: null });
    try {
      const response = await api.getPredictionHistory(limit, offset);
      set({ 
        predictions: response.data.predictions,
        loading: false 
      });
      return response.data;
    } catch (error) {
      set({ 
        error: error.message, 
        loading: false 
      });
    }
  },
  
  clearPredictions: () => set({ predictions: [], currentPrediction: null }),
}));

export default usePredictionStore;
