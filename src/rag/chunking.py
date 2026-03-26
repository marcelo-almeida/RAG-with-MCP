from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


_WORD_RE = re.compile(r"\S+")


def parse_markdown_frontmatter(md_text: str) -> Tuple[Dict[str, str], str]:
    """
    Parses a simple YAML-like frontmatter block:
    ---
    key: "value"
    ...
    ---
    body...

    This is intentionally lightweight (no PyYAML dependency) since our generated
    character files follow a consistent format.
    """
    if not md_text.startswith("---"):
        return {}, md_text

    # Find frontmatter delimiters ('---' on its own line).
    delimiters = list(re.finditer(r"^---\s*$", md_text, flags=re.MULTILINE))
    if len(delimiters) < 2:
        return {}, md_text

    start_delim = delimiters[0]
    end_delim = delimiters[1]

    # Body starts *after* the ending delimiter line.
    fm_block = md_text[start_delim.end() : end_delim.start()].strip("\n")
    body = md_text[end_delim.end() :].lstrip("\n")

    meta: Dict[str, str] = {}
    for line in fm_block.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')

    return meta, body


def _word_spans(text: str) -> List[Tuple[int, int]]:
    """
    Returns list of (start_char, end_char) for each whitespace-separated token.
    """
    spans: List[Tuple[int, int]] = []
    for m in _WORD_RE.finditer(text):
        spans.append((m.start(), m.end()))
    return spans


def chunk_text_by_words(
    text: str,
    chunk_size_words: int = 200,
    chunk_overlap_words: int = 40,
    min_words: int = 1,
) -> List[Dict[str, Any]]:
    """
    Chunking strategy: word windows with overlap.

    - Deterministic and simple to reason about.
    - Provides start/end char offsets using token spans.
    """
    tokens = _WORD_RE.findall(text)
    if not tokens:
        return []

    spans = _word_spans(text)
    assert len(tokens) == len(spans)

    if chunk_overlap_words >= chunk_size_words:
        raise ValueError("chunk_overlap_words must be smaller than chunk_size_words")

    step = chunk_size_words - chunk_overlap_words
    chunks: List[Dict[str, Any]] = []

    for i, start_idx in enumerate(range(0, len(tokens), step)):
        end_idx = min(start_idx + chunk_size_words, len(tokens))
        if end_idx - start_idx < min_words:
            continue

        start_char = spans[start_idx][0]
        end_char = spans[end_idx - 1][1]

        chunk_text = text[start_char:end_char].strip()
        if not chunk_text:
            continue

        chunks.append(
            {
                "chunk_index": i,
                "text": chunk_text,
                "start_char": start_char,
                "end_char": end_char,
            }
        )

        if end_idx == len(tokens):
            break

    return chunks


def iter_markdown_files(directory: Path) -> Iterable[Path]:
    yield from sorted(directory.glob("*.md"))


def generate_chunks_from_character_files(
    characters_dir: Path,
    output_jsonl_path: Path,
    chunk_size_words: int = 200,
    chunk_overlap_words: int = 40,
) -> int:
    """
    Reads `data/characters/*.md` files and generates `chunks.jsonl`.

    Each line includes:
    - chunk_id
    - character metadata from frontmatter
    - text and chunk offsets
    """
    output_jsonl_path.parent.mkdir(parents=True, exist_ok=True)

    total_chunks = 0
    with output_jsonl_path.open("w", encoding="utf-8") as f:
        for md_path in iter_markdown_files(characters_dir):
            md_text = md_path.read_text(encoding="utf-8")
            meta, body = parse_markdown_frontmatter(md_text)

            # Some earlier/handwritten files might have no frontmatter.
            char_name = meta.get("name") or md_path.stem

            chunks = chunk_text_by_words(
                body,
                chunk_size_words=chunk_size_words,
                chunk_overlap_words=chunk_overlap_words,
            )

            for c in chunks:
                chunk_index = c["chunk_index"]
                chunk_id = f"{md_path.stem}_chunk_{chunk_index}"

                record = {
                    "chunk_id": chunk_id,
                    "character": char_name,
                    "source_file": md_path.name,
                    "chunk_index": chunk_index,
                    "start_char": c["start_char"],
                    "end_char": c["end_char"],
                    "text": c["text"],
                    "doc_meta": meta,
                }

                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                total_chunks += 1

    return total_chunks

