#!/bin/bash
# scripts/setup_environment.sh
# Script para configurar el entorno de desarrollo

set -e

echo "🔧 Configurando entorno de Cyberbullying Detection..."

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p ml/checkpoints/beto
mkdir -p ml/checkpoints/bilstm
mkdir -p ml/checkpoints/cnn
mkdir -p ml/data/raw
mkdir -p ml/data/processed
mkdir -p ml/experiments/results

# Backend
echo "🐍 Configurando Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Frontend
echo "📦 Configurando Frontend..."
cd frontend
npm install
cd ..

# ML
echo "🤖 Configurando ML..."
cd ml
python3 -m venv venv_ml
source venv_ml/bin/activate
pip install -r requirements.txt
cd ..

# Descargar modelos pre-entrenados (opcional)
echo "📥 Descargando modelos pre-entrenados..."
python3 ml/models/download_pretrained.py 2>/dev/null || true

echo "✅ Setup completado!"
echo ""
echo "Próximos pasos:"
echo "1. Configurar variables de entorno: cp .env.example .env"
echo "2. Descargar dataset: bash scripts/download_dataset.sh"
echo "3. Entrenar modelos: bash scripts/train_all_models.sh"
echo "4. Iniciar servicios: docker-compose up"
