from __future__ import annotations

from typing import Optional

import numpy as np


def embed_with_sentence_transformers(
    texts: list[str],
    model_name: str,
    batch_size: int = 32,
    normalize_embeddings: bool = True,
) -> np.ndarray:
    """
    Embeds texts using sentence-transformers.

    Returns: float32 numpy array of shape (len(texts), dim)
    """
    # Local import so the module can be imported even if deps are missing.
    from sentence_transformers import SentenceTransformer  # type: ignore

    model = SentenceTransformer(model_name)

    # Newer versions support `normalize_embeddings`.
    try:
        emb = model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=normalize_embeddings,
        )
    except TypeError:
        emb = model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
        )
        if normalize_embeddings:
            emb = _l2_normalize(emb)

    return np.asarray(emb, dtype=np.float32)


def _l2_normalize(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    return x / (norms + eps)

