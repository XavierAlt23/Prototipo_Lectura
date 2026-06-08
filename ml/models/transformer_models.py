"""
ml/models/transformer_models.py
Modelos Transformer: BETO, DistilBETO, BERT-M
"""

import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import logging

logger = logging.getLogger(__name__)


class TransformerClassifier(nn.Module):
    """
    Clasificador de ciberbullying basado en Transformers
    """
    
    def __init__(
        self,
        model_name: str = "dccuchile/bert-base-spanish-wwm-uncased",
        num_classes: int = 2,
        max_length: int = 128,
        dropout: float = 0.1
    ):
        """
        Args:
            model_name: Nombre del modelo en HuggingFace
            num_classes: Número de clases (2 para clasificación binaria)
            max_length: Longitud máxima del texto
            dropout: Tasa de dropout
        """
        super(TransformerClassifier, self).__init__()
        
        self.model_name = model_name
        self.max_length = max_length
        self.num_classes = num_classes
        
        # Cargar modelo pre-entrenado
        logger.info(f"Cargando modelo: {model_name}")
        self.transformer = AutoModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Cabeza de clasificación
        hidden_size = self.transformer.config.hidden_size
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, num_classes)
        )
        
    def forward(self, input_ids, attention_mask, token_type_ids=None):
        """
        Forward pass
        
        Args:
            input_ids: IDs de tokens
            attention_mask: Máscara de atención
            token_type_ids: IDs de tipo de token (para BERT)
            
        Returns:
            Logits de clasificación
        """
        # Obtener embeddings del transformer
        outputs = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids
        )
        
        # Usar el embeddings del token [CLS] (primer token)
        cls_output = outputs.last_hidden_state[:, 0, :]
        
        # Pasar por la cabeza de clasificación
        logits = self.classifier(cls_output)
        
        return logits
    
    def tokenize_batch(self, texts, padding=True, truncation=True):
        """
        Tokeniza un lote de textos
        
        Args:
            texts: Lista de textos
            padding: Aplicar padding
            truncation: Truncar textos largos
            
        Returns:
            Dict con input_ids, attention_mask, token_type_ids
        """
        encodings = self.tokenizer(
            texts,
            max_length=self.max_length,
            padding=padding,
            truncation=truncation,
            return_tensors="pt"
        )
        return encodings


class BETOClassifier(TransformerClassifier):
    """BETO: BERT en Español - Modelo base para español"""
    def __init__(self, num_classes: int = 2, max_length: int = 128):
        super().__init__(
            model_name="dccuchile/bert-base-spanish-wwm-uncased",
            num_classes=num_classes,
            max_length=max_length
        )


class DistilBETOClassifier(TransformerClassifier):
    """DistilBETO: Versión destilada y optimizada de BETO"""
    def __init__(self, num_classes: int = 2, max_length: int = 128):
        super().__init__(
            model_name="dccuchile/distilbert-base-spanish-uncased",
            num_classes=num_classes,
            max_length=max_length
        )


class BERTMultilingualClassifier(TransformerClassifier):
    """BERT Multilingual: Modelo que soporta múltiples idiomas incluyendo español"""
    def __init__(self, num_classes: int = 2, max_length: int = 128):
        super().__init__(
            model_name="bert-base-multilingual-uncased",
            num_classes=num_classes,
            max_length=max_length
        )


# Ejemplo de uso
if __name__ == "__main__":
    import torch
    
    logging.basicConfig(level=logging.INFO)
    
    # Crear modelo BETO
    model = BETOClassifier(num_classes=2, max_length=128)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    # Ejemplo de predicción
    texts = [
        "Eres un imbécil, no sirves para nada",
        "¡Hola! ¿Cómo estás? Espero que bien"
    ]
    
    # Tokenizar
    encodings = model.tokenize_batch(texts)
    
    # Mover a dispositivo
    input_ids = encodings['input_ids'].to(device)
    attention_mask = encodings['attention_mask'].to(device)
    
    # Predicción
    with torch.no_grad():
        logits = model(input_ids, attention_mask)
        predictions = torch.softmax(logits, dim=1)
    
    print("Texto:", texts[0])
    print("Predicción (No CB, CB):", predictions[0].cpu().numpy())
    print("Clase predicha:", predictions[0].argmax().item())
