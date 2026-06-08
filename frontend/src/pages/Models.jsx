import React from 'react';

import ModelComparison from '../components/ModelComparison.jsx';
import useModelStore from '../stores/modelStore.js';

export default function Models() {
  const { models, loading, error } = useModelStore();

  return (
    <section className="page">
      <header className="page-header">
        <h1>Modelos</h1>
        <p>Consulta y comparacion de arquitecturas disponibles.</p>
      </header>

      {error && <div className="alert">{error}</div>}
      {loading && <div className="card">Cargando modelos...</div>}

      <article className="card">
        <h2>Catalogo</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Tipo</th>
              <th>Accuracy</th>
              <th>F1</th>
            </tr>
          </thead>
          <tbody>
            {models.map((model) => (
              <tr key={model.id}>
                <td>{model.name}</td>
                <td>{model.model_type}</td>
                <td>{model.accuracy ? (model.accuracy * 100).toFixed(2) : 'N/D'}%</td>
                <td>{model.f1_score ? (model.f1_score * 100).toFixed(2) : 'N/D'}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </article>

      <ModelComparison />
    </section>
  );
}
