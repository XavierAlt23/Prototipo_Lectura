"""
Callbacks de entrenamiento.
"""


class EarlyStopping:
    def __init__(self, patience: int = 3):
        self.patience = patience
        self.best_score = None
        self.counter = 0
