// frontend/src/pages/Prediction.jsx
// Página para realizar predicciones

import React, { useState } from 'react';
import usePredictionStore from '../stores/predictionStore';
import useModelStore from '../stores/modelStore';

export default function Prediction() {
  const [text, setText] = useState('');
  const [selectedModelId, setSelectedModelId] = useState(1);
  
  const { predict, currentPrediction, loading, error } = usePredictionStore();
  const { models } = useModelStore();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    await predict(text, selectedModelId);
  };
  
  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-8">Predictor de Ciberbullying</h1>
      
      <form onSubmit={handleSubmit} className="mb-8 space-y-4">
        {/* Selector de modelo */}
        <div>
          <label className="block text-sm font-medium mb-2">Seleccionar Modelo</label>
          <select 
            value={selectedModelId}
            onChange={(e) => setSelectedModelId(parseInt(e.target.value))}
            className="w-full px-4 py-2 border rounded-lg"
          >
            {models.map(model => (
              <option key={model.id} value={model.id}>
                {model.name} - Accuracy: {(model.accuracy * 100).toFixed(2)}%
              </option>
            ))}
          </select>
        </div>
        
        {/* Textarea */}
        <div>
          <label className="block text-sm font-medium mb-2">Texto a Analizar</label>
          <textarea 
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Ingresa el texto a clasificar..."
            rows={6}
            className="w-full px-4 py-2 border rounded-lg"
            disabled={loading}
          />
        </div>
        
        {/* Botón */}
        <button 
          type="submit"
          disabled={loading || !text}
          className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg disabled:opacity-50"
        >
          {loading ? 'Analizando...' : 'Analizar Texto'}
        </button>
      </form>
      
      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
          {error}
        </div>
      )}
      
      {/* Resultado */}
      {currentPrediction && (
        <div className={`border rounded-lg p-6 ${
          currentPrediction.prediction === 1 
            ? 'bg-red-50 border-red-200' 
            : 'bg-green-50 border-green-200'
        }`}>
          <h2 className="text-2xl font-bold mb-4">Resultado</h2>
          
          <div className="space-y-3">
            <p className="text-lg">
              <strong>Clasificación:</strong> 
              <span className={`ml-2 font-bold ${
                currentPrediction.prediction === 1 
                  ? 'text-red-600' 
                  : 'text-green-600'
              }`}>
                {currentPrediction.class_label}
              </span>
            </p>
            
            <p className="text-lg">
              <strong>Confianza:</strong> 
              <span className="ml-2">{(currentPrediction.confidence * 100).toFixed(2)}%</span>
            </p>
            
            <p className="text-lg">
              <strong>Modelo Usado:</strong> 
              <span className="ml-2">{currentPrediction.model_name}</span>
            </p>
            
            <p className="text-sm text-gray-600">
              <strong>Tiempo de procesamiento:</strong> {currentPrediction.execution_time_ms}ms
            </p>
          </div>
          
          {/* Barra de confianza */}
          <div className="mt-6">
            <label className="text-sm font-medium">Confianza Visual</label>
            <div className="w-full bg-gray-200 rounded-full h-4 mt-2">
              <div 
                className={`h-4 rounded-full ${
                  currentPrediction.prediction === 1 
                    ? 'bg-red-500' 
                    : 'bg-green-500'
                }`}
                style={{ width: `${currentPrediction.confidence * 100}%` }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
