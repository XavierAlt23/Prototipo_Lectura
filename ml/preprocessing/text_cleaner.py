"""
ml/preprocessing/text_cleaner.py
Módulo para preprocesamiento y limpieza de texto en español
"""

import re
import logging
from typing import List
import unicodedata

logger = logging.getLogger(__name__)


class TextCleaner:
    """
    Limpia y normaliza texto en español para NLP
    """
    
    def __init__(self, lowercase: bool = True, remove_accents: bool = False):
        """
        Args:
            lowercase: Convertir a minúsculas
            remove_accents: Remover acentos
        """
        self.lowercase = lowercase
        self.remove_accents = remove_accents
        
        # Palabras comunes a remover (stopwords en español)
        self.spanish_stopwords = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se',
            'no', 'haber', 'por', 'con', 'su', 'para', 'es', 'lo', 'como',
            'más', 'o', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque',
            'esta', 'son', 'entre', 'está', 'cuando', 'muy', 'sin', 'sobre',
            'ser', 'tiene', 'también', 'me', 'hasta', 'hay', 'donde'
        }
    
    def clean(self, text: str) -> str:
        """
        Pipeline completo de limpieza
        
        Args:
            text: Texto a limpiar
            
        Returns:
            Texto limpio
        """
        if not isinstance(text, str):
            return ""
        
        # 1. Remover URLs
        text = self._remove_urls(text)
        
        # 2. Remover menciones (@usuario)
        text = self._remove_mentions(text)
        
        # 3. Remover hashtags (mantener solo el texto)
        text = self._remove_hashtags(text)
        
        # 4. Remover caracteres especiales y números
        text = self._remove_special_chars(text)
        
        # 5. Remover espacios múltiples
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 6. Remover acentos (opcional)
        if self.remove_accents:
            text = self._remove_accents_func(text)
        
        # 7. Convertir a minúsculas
        if self.lowercase:
            text = text.lower()
        
        return text
    
    def _remove_urls(self, text: str) -> str:
        """Remover URLs"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(url_pattern, '', text)
    
    def _remove_mentions(self, text: str) -> str:
        """Remover menciones (@usuario)"""
        return re.sub(r'@\w+', '', text)
    
    def _remove_hashtags(self, text: str) -> str:
        """Remover # pero mantener la palabra"""
        return re.sub(r'#', '', text)
    
    def _remove_special_chars(self, text: str) -> str:
        """Remover caracteres especiales, mantener puntuación básica"""
        # Mantener letras, números, espacios y puntuación básica
        text = re.sub(r'[^a-záéíóúñüA-ZÁÉÍÓÚÑÜ0-9\s\.\,\!\?\-]', '', text)
        return text
    
    def _remove_accents_func(self, text: str) -> str:
        """Remover acentos del texto"""
        nfd = unicodedata.normalize('NFD', text)
        return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')
    
    def tokenize(self, text: str, remove_stopwords: bool = False) -> List[str]:
        """
        Tokeniza el texto en palabras
        
        Args:
            text: Texto a tokenizar
            remove_stopwords: Remover palabras comunes
            
        Returns:
            Lista de tokens
        """
        tokens = text.split()
        
        if remove_stopwords:
            tokens = [t for t in tokens if t.lower() not in self.spanish_stopwords]
        
        return tokens
    
    def clean_batch(self, texts: List[str]) -> List[str]:
        """
        Limpia un lote de textos
        
        Args:
            texts: Lista de textos
            
        Returns:
            Lista de textos limpios
        """
        return [self.clean(text) for text in texts]


# Ejemplo de uso
if __name__ == "__main__":
    cleaner = TextCleaner(lowercase=True, remove_accents=False)
    
    # Ejemplos de textos
    tweets = [
        "¡Eres un imbécil! @usuario Check this out: https://example.com #cyberbullying",
        "Hola, ¿cómo estás? 😊 #vida",
        "Vete a la mierda, eres un inútil!!!",
        "El clima hoy es hermoso... para algunos",
    ]
    
    print("Textos originales vs limpiados:\n")
    for tweet in tweets:
        cleaned = cleaner.clean(tweet)
        print(f"Original:  {tweet}")
        print(f"Limpio:    {cleaned}\n")
