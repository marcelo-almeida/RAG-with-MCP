from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def load_chunks_jsonl(chunks_jsonl_path: Path) -> list[dict]:
    records: list[dict] = []
    with chunks_jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Build FAISS index from chunks.jsonl embeddings.")
    parser.add_argument("--chunks-jsonl", type=Path, default=Path("data/index/chunks.jsonl"))
    parser.add_argument("--index-path", type=Path, default=Path("data/index/faiss.index"))
    parser.add_argument("--chunk-ids-path", type=Path, default=Path("data/index/chunk_ids.json"))
    parser.add_argument("--chunks-by-id-path", type=Path, default=Path("data/index/chunks_by_id.json"))
    parser.add_argument("--embedding-model", type=str, default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--no-normalize", action="store_true", help="Disable L2 normalization (less accurate cosine).")
    parser.add_argument("--limit", type=int, default=0, help="Optional: embed only first N chunks.")
    args = parser.parse_args()

    if not args.chunks_jsonl.exists():
        raise FileNotFoundError(f"Missing chunks file: {args.chunks_jsonl}")

    # Add repo root to sys.path for local imports
    import sys

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))

    from src.rag.embeddings import embed_with_sentence_transformers  # noqa: E402
    from src.rag.faiss_index import build_flat_ip_index, write_index, save_json  # noqa: E402

    chunks = load_chunks_jsonl(args.chunks_jsonl)
    if args.limit and args.limit > 0:
        chunks = chunks[: args.limit]

    texts = [c["text"] for c in chunks]

    normalize = not args.no_normalize
    embeddings = embed_with_sentence_transformers(
        texts=texts,
        model_name=args.embedding_model,
        batch_size=args.batch_size,
        normalize_embeddings=normalize,
    )

    index = build_flat_ip_index(embeddings)

    args.index_path.parent.mkdir(parents=True, exist_ok=True)
    write_index(index, str(args.index_path))

    chunk_ids = [c["chunk_id"] for c in chunks]
    save_json(str(args.chunk_ids_path), chunk_ids)
    save_json(str(args.chunks_by_id_path), {c["chunk_id"]: c for c in chunks})

    # quick sanity check: verify dimensions match FAISS index dim (for debugging)
    try:
        dim = index.d
        if embeddings.shape[1] != dim:
            raise RuntimeError(f"Embedding dim mismatch: {embeddings.shape[1]} != FAISS dim {dim}")
    except Exception:
        pass

    print(f"Built FAISS index with {len(chunks)} chunks -> {args.index_path}")


if __name__ == "__main__":
    main()

