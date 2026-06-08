import React from 'react';

import usePredictionStore from '../stores/predictionStore.js';

export default function Analytics() {
  const { predictions } = usePredictionStore();
  const positives = predictions.filter((item) => item.prediction === 1).length;
  const negatives = predictions.length - positives;

  return (
    <section className="page">
      <header className="page-header">
        <h1>Analitica</h1>
        <p>Lectura rapida de las predicciones generadas en la sesion.</p>
      </header>

      <div className="grid two">
        <article className="card metric">
          Cyberbullying
          <strong>{positives}</strong>
        </article>
        <article className="card metric">
          No cyberbullying
          <strong>{negatives}</strong>
        </article>
      </div>

      <article className="card">
        <h2>Historial</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Texto</th>
              <th>Clase</th>
              <th>Confianza</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map((prediction, index) => (
              <tr key={`${prediction.text || prediction.model_name}-${index}`}>
                <td>{prediction.text || 'Prediccion individual'}</td>
                <td>{prediction.class_label}</td>
                <td>{(prediction.confidence * 100).toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </article>
    </section>
  );
}
