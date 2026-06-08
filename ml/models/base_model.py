"""
Clase base ligera para modelos del proyecto.
"""

from abc import ABC, abstractmethod


class BaseTextClassifier(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def predict(self, texts):
        raise NotImplementedError
