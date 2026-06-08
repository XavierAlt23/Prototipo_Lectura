import React, { useEffect } from 'react';
import { NavLink, Route, Routes } from 'react-router-dom';

import Analytics from './pages/Analytics.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Models from './pages/Models.jsx';
import Prediction from './pages/Prediction.jsx';
import useModelStore from './stores/modelStore.js';

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/prediction', label: 'Prediccion' },
  { to: '/models', label: 'Modelos' },
  { to: '/analytics', label: 'Analitica' },
];

export default function App() {
  const { loadModels } = useModelStore();

  useEffect(() => {
    loadModels();
  }, [loadModels]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">CB</span>
          <div>
            <strong>Cyberbullying</strong>
            <small>Deteccion NLP</small>
          </div>
        </div>
        <nav className="nav">
          {links.map((link) => (
            <NavLink key={link.to} to={link.to} end={link.to === '/'}>
              {link.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <main className="main-panel">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/prediction" element={<Prediction />} />
          <Route path="/models" element={<Models />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </main>
    </div>
  );
}
