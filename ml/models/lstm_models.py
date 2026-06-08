"""
ml/models/lstm_models.py
Modelos LSTM: BiLSTM, Conv1D-LSTM
"""

import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import logging

logger = logging.getLogger(__name__)


class BiLSTMClassifier(nn.Module):
    """
    Clasificador basado en BiLSTM (Bidirectional LSTM)
    """
    
    def __init__(
        self,
        embedding_model: str = "dccuchile/bert-base-spanish-wwm-uncased",
        hidden_size: int = 256,
        num_layers: int = 2,
        num_classes: int = 2,
        dropout: float = 0.3,
        max_length: int = 128
    ):
        """
        Args:
            embedding_model: Modelo pre-entrenado para embeddings
            hidden_size: Tamaño de la capa LSTM
            num_layers: Número de capas LSTM
            num_classes: Número de clases
            dropout: Tasa de dropout
            max_length: Longitud máxima del texto
        """
        super(BiLSTMClassifier, self).__init__()
        
        self.embedding_model_name = embedding_model
        self.max_length = max_length
        self.hidden_size = hidden_size
        
        # Cargar embeddings pre-entrenados
        logger.info(f"Cargando modelo de embeddings: {embedding_model}")
        self.embedding_model = AutoModel.from_pretrained(embedding_model)
        self.tokenizer = AutoTokenizer.from_pretrained(embedding_model)
        
        embedding_dim = self.embedding_model.config.hidden_size
        
        # Congelar embeddings (opcional)
        for param in self.embedding_model.parameters():
            param.requires_grad = False
        
        # Capas LSTM
        self.bilstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_size,
            num_layers=num_layers,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0,
            batch_first=True
        )
        
        # Capa de atención (opcional)
        self.attention = nn.MultiheadAttention(
            embed_dim=hidden_size * 2,  # Por bidireccional
            num_heads=8,
            dropout=dropout,
            batch_first=True
        )
        
        # Cabeza de clasificación
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, num_classes)
        )
        
    def forward(self, input_ids, attention_mask):
        """
        Args:
            input_ids: IDs de tokens
            attention_mask: Máscara de atención
            
        Returns:
            Logits de clasificación
        """
        # Obtener embeddings
        with torch.no_grad():
            embeddings = self.embedding_model(
                input_ids=input_ids,
                attention_mask=attention_mask
            ).last_hidden_state
        
        # Pasar por BiLSTM
        lstm_output, (h_n, c_n) = self.bilstm(embeddings)
        
        # Usar salida final de ambas direcciones
        final_output = torch.cat([h_n[-2], h_n[-1]], dim=1)  # Último layer
        
        # Clasificación
        logits = self.classifier(final_output)
        
        return logits
    
    def tokenize_batch(self, texts, padding=True, truncation=True):
        """Tokeniza un lote de textos"""
        encodings = self.tokenizer(
            texts,
            max_length=self.max_length,
            padding=padding,
            truncation=truncation,
            return_tensors="pt"
        )
        return encodings


class Conv1DLSTMClassifier(nn.Module):
    """
    Combinación de Convolución 1D + LSTM
    Captura patrones locales con Conv1D y contexto secuencial con LSTM
    """
    
    def __init__(
        self,
        embedding_model: str = "dccuchile/bert-base-spanish-wwm-uncased",
        num_filters: int = 100,
        filter_sizes: tuple = (2, 3, 4, 5),
        hidden_size: int = 128,
        num_classes: int = 2,
        dropout: float = 0.3,
        max_length: int = 128
    ):
        """
        Args:
            embedding_model: Modelo pre-entrenado para embeddings
            num_filters: Número de filtros por tamaño
            filter_sizes: Tamaños de filtros convolucionales
            hidden_size: Tamaño de LSTM
            num_classes: Número de clases
            dropout: Tasa de dropout
            max_length: Longitud máxima del texto
        """
        super(Conv1DLSTMClassifier, self).__init__()
        
        self.embedding_model_name = embedding_model
        self.max_length = max_length
        self.num_filters = num_filters
        self.filter_sizes = filter_sizes
        
        # Modelo de embeddings
        logger.info(f"Cargando modelo de embeddings: {embedding_model}")
        self.embedding_model = AutoModel.from_pretrained(embedding_model)
        self.tokenizer = AutoTokenizer.from_pretrained(embedding_model)
        
        embedding_dim = self.embedding_model.config.hidden_size
        
        # Congelar embeddings
        for param in self.embedding_model.parameters():
            param.requires_grad = False
        
        # Capas convolucionales
        self.convs = nn.ModuleList([
            nn.Conv1d(
                in_channels=embedding_dim,
                out_channels=num_filters,
                kernel_size=fs
            ) for fs in filter_sizes
        ])
        
        # LSTM
        conv_output_size = len(filter_sizes) * num_filters
        self.lstm = nn.LSTM(
            input_size=conv_output_size,
            hidden_size=hidden_size,
            num_layers=1,
            bidirectional=True,
            batch_first=True
        )
        
        # Cabeza de clasificación
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, num_classes)
        )
    
    def forward(self, input_ids, attention_mask):
        """Forward pass"""
        # Embeddings
        with torch.no_grad():
            embeddings = self.embedding_model(
                input_ids=input_ids,
                attention_mask=attention_mask
            ).last_hidden_state
        
        # Conv1D: (batch, seq_len, emb_dim) -> (batch, num_filters, seq_len - fs + 1)
        conv_outputs = []
        for conv in self.convs:
            # Transponer para Conv1d: (batch, emb_dim, seq_len)
            x = embeddings.transpose(1, 2)
            x = torch.relu(conv(x))
            # Max pooling
            x = torch.nn.functional.max_pool1d(x, x.size(2))
            x = x.squeeze(2)
            conv_outputs.append(x)
        
        # Concatenar salidas de convoluciones
        conv_concat = torch.cat(conv_outputs, dim=1)
        
        # LSTM
        conv_concat = conv_concat.unsqueeze(1)  # (batch, 1, conv_size)
        lstm_output, (h_n, c_n) = self.lstm(conv_concat)
        final_output = torch.cat([h_n[0], h_n[1]], dim=1)
        
        # Clasificación
        logits = self.classifier(final_output)
        
        return logits
    
    def tokenize_batch(self, texts, padding=True, truncation=True):
        """Tokeniza un lote de textos"""
        encodings = self.tokenizer(
            texts,
            max_length=self.max_length,
            padding=padding,
            truncation=truncation,
            return_tensors="pt"
        )
        return encodings


# Ejemplo de uso
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Crear modelo BiLSTM
    model = BiLSTMClassifier()
    model.to(device)
    model.eval()
    
    # Ejemplo
    texts = ["Eres un imbécil", "Hola, ¿cómo estás?"]
    
    encodings = model.tokenize_batch(texts)
    input_ids = encodings['input_ids'].to(device)
    attention_mask = encodings['attention_mask'].to(device)
    
    with torch.no_grad():
        logits = model(input_ids, attention_mask)
        predictions = torch.softmax(logits, dim=1)
    
    print(f"Predicción: {predictions[0].cpu().numpy()}")
