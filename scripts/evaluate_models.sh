#!/bin/bash
# scripts/evaluate_models.sh
# Script para evaluar todos los modelos

echo "📊 Evaluando modelos..."

cd ml

python evaluation/evaluate_all_models.py

echo "✅ Evaluación completada!"
echo "📈 Generando reportes..."

python evaluation/generate_comparison_report.py

echo "✅ Reportes generados en ml/experiments/results/"
