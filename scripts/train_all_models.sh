#!/bin/bash
# scripts/train_all_models.sh
# Script para entrenar todos los modelos

echo "🚀 Iniciando entrenamiento de todos los modelos..."

cd ml

# Entrenar BETO
echo "📍 Entrenando BETO..."
python training/train_beto.py

# Entrenar DistilBETO
echo "📍 Entrenando DistilBETO..."
python training/train_distilbeto.py

# Entrenar BERT-M
echo "📍 Entrenando BERT-M..."
python training/train_bert_m.py

# Entrenar BiLSTM
echo "📍 Entrenando BiLSTM..."
python training/train_bilstm.py

# Entrenar Conv1D-LSTM
echo "📍 Entrenando Conv1D-LSTM..."
python training/train_conv1d_lstm.py

# Entrenar CNN
echo "📍 Entrenando CNN..."
python training/train_cnn.py

echo "✅ Entrenamiento completado!"
echo "📊 Evaluando modelos..."
bash ../scripts/evaluate_models.sh
