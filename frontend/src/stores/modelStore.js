"""
frontend/src/stores/modelStore.js
Zustand store para estado de modelos
"""

import { create } from 'zustand';
import api from '../services/api';

export const useModelStore = create((set) => ({
  models: [],
  selectedModel: null,
  modelMetrics: null,
  loading: false,
  error: null,
  
  // Acciones
  loadModels: async () => {
    set({ loading: true, error: null });
    try {
      const response = await api.getModels();
      set({ 
        models: response.data.models,
        loading: false 
      });
    } catch (error) {
      set({ 
        error: error.message, 
        loading: false 
      });
    }
  },
  
  selectModel: (modelId) => {
    set((state) => ({
      selectedModel: state.models.find(m => m.id === modelId)
    }));
  },
  
  loadModelMetrics: async (modelId) => {
    set({ loading: true, error: null });
    try {
      const response = await api.getModelMetrics(modelId);
      set({ 
        modelMetrics: response.data,
        loading: false 
      });
    } catch (error) {
      set({ 
        error: error.message, 
        loading: false 
      });
    }
  },
  
  compareModels: async (model1Id, model2Id) => {
    try {
      const response = await api.compareModels(model1Id, model2Id);
      return response.data;
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },
}));

export default useModelStore;
