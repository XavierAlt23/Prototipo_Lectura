"""
Helpers para embeddings.
"""


def build_embedding_metadata(name: str, dimension: int) -> dict:
    return {"name": name, "dimension": dimension}
