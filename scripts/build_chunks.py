from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.rag.chunking import generate_chunks_from_character_files  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Build RAG chunks from character markdown files.")
    parser.add_argument("--characters-dir", type=Path, default=Path("data/characters"))
    parser.add_argument("--output", type=Path, default=Path("data/index/chunks.jsonl"))
    parser.add_argument("--chunk-size-words", type=int, default=200)
    parser.add_argument("--chunk-overlap-words", type=int, default=40)
    args = parser.parse_args()

    total = generate_chunks_from_character_files(
        characters_dir=args.characters_dir,
        output_jsonl_path=args.output,
        chunk_size_words=args.chunk_size_words,
        chunk_overlap_words=args.chunk_overlap_words,
    )

    print(f"Generated {total} chunks -> {args.output}")


if __name__ == "__main__":
    main()

