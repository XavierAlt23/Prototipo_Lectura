import React from 'react';

import useModelStore from '../stores/modelStore.js';
import usePredictionStore from '../stores/predictionStore.js';

export default function Dashboard() {
  const { models } = useModelStore();
  const { predictions } = usePredictionStore();

  return (
    <section className="page">
      <header className="page-header">
        <h1>Panel de control</h1>
        <p>Resumen operativo del prototipo de deteccion en espanol.</p>
      </header>

      <div className="grid three">
        <article className="card metric">
          Modelos disponibles
          <strong>{models.length}</strong>
        </article>
        <article className="card metric">
          Predicciones en sesion
          <strong>{predictions.length}</strong>
        </article>
        <article className="card metric">
          Mejor F1 registrado
          <strong>{models[0]?.f1_score ? `${(models[0].f1_score * 100).toFixed(1)}%` : 'N/D'}</strong>
        </article>
      </div>

      <article className="card">
        <h2>Flujo actual</h2>
        <p>Datos, preprocesamiento, entrenamiento, evaluacion, API y frontend quedan separados por modulo para facilitar experimentacion y despliegue.</p>
      </article>
    </section>
  );
}
