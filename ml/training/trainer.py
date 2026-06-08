"""
Entrenador base para experimentos.
"""


class Trainer:
    def __init__(self, model, optimizer=None, loss_fn=None):
        self.model = model
        self.optimizer = optimizer
        self.loss_fn = loss_fn

    def train(self, train_loader, validation_loader=None, epochs: int = 1):
        return {"epochs": epochs, "status": "not_implemented"}
