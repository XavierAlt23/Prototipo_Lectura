// frontend/src/components/ModelComparison.jsx
// Componente para comparar modelos

import React, { useState } from 'react';
import useModelStore from '../stores/modelStore';

export default function ModelComparison() {
  const [model1Id, setModel1Id] = useState(null);
  const [model2Id, setModel2Id] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const { models, compareModels } = useModelStore();
  
  const handleCompare = async () => {
    if (!model1Id || !model2Id) return;
    
    setLoading(true);
    try {
      const result = await compareModels(model1Id, model2Id);
      setComparison(result);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-6">Comparar Modelos</h2>
      
      <div className="grid grid-cols-2 gap-4 mb-6">
        {/* Seleccionar Modelo 1 */}
        <div>
          <label className="block text-sm font-medium mb-2">Modelo 1</label>
          <select 
            value={model1Id || ''}
            onChange={(e) => setModel1Id(parseInt(e.target.value))}
            className="w-full px-4 py-2 border rounded-lg"
          >
            <option value="">Seleccionar...</option>
            {models.map(m => (
              <option key={m.id} value={m.id}>{m.name}</option>
            ))}
          </select>
        </div>
        
        {/* Seleccionar Modelo 2 */}
        <div>
          <label className="block text-sm font-medium mb-2">Modelo 2</label>
          <select 
            value={model2Id || ''}
            onChange={(e) => setModel2Id(parseInt(e.target.value))}
            className="w-full px-4 py-2 border rounded-lg"
          >
            <option value="">Seleccionar...</option>
            {models.map(m => (
              <option key={m.id} value={m.id}>{m.name}</option>
            ))}
          </select>
        </div>
      </div>
      
      <button 
        onClick={handleCompare}
        disabled={!model1Id || !model2Id || loading}
        className="w-full px-6 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50"
      >
        {loading ? 'Comparando...' : 'Comparar'}
      </button>
      
      {comparison && (
        <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <p className="font-bold text-lg mb-2">Resultado: <span className="text-blue-600">{comparison.winner}</span></p>
          <p>Diferencia: {(comparison.difference * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}
