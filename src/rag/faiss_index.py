from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

import numpy as np


@dataclass(frozen=True)
class FaissIndexPaths:
    index_path: str
    chunk_ids_path: str
    chunks_by_id_path: str


def build_flat_ip_index(vectors: np.ndarray):
    """
    Builds FAISS IndexFlatIP for cosine similarity.

    Assumption: vectors are already L2-normalized if you want cosine similarity.
    """
    import faiss  # type: ignore

    x = np.asarray(vectors, dtype=np.float32)
    if x.ndim != 2:
        raise ValueError("vectors must be a 2D array")

    dim = x.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(x)
    return index


def write_index(index, index_path: str) -> None:
    import faiss  # type: ignore

    faiss.write_index(index, index_path)


def save_json(path: str, obj) -> None:
    import json

    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)

