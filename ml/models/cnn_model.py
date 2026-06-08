"""
Modelo CNN para clasificacion de texto.
"""

try:
    import torch
    from torch import nn
except ImportError:
    torch = None
    nn = None


if nn:
    class TextCNN(nn.Module):
        def __init__(self, vocab_size: int, embedding_dim: int = 128, num_classes: int = 2):
            super().__init__()
            self.embedding = nn.Embedding(vocab_size, embedding_dim)
            self.conv = nn.Conv1d(embedding_dim, 128, kernel_size=3, padding=1)
            self.pool = nn.AdaptiveMaxPool1d(1)
            self.classifier = nn.Linear(128, num_classes)

        def forward(self, input_ids):
            x = self.embedding(input_ids).transpose(1, 2)
            x = self.pool(torch.relu(self.conv(x))).squeeze(-1)
            return self.classifier(x)
else:
    class TextCNN:
        def __init__(self, *args, **kwargs):
            raise ImportError("PyTorch es requerido para usar TextCNN.")
