# RAG with MCP — Frieren Character Knowledge

Example project implementing **Retrieval-Augmented Generation (RAG)** over structured character data from *Frieren: Beyond Journey’s End* (*Sousou no Frieren*). The stack uses **FAISS** for vector search and an **MCP (Model Context Protocol) server** that retrieves, re-ranks, and returns the most relevant passages for downstream use (e.g. LLM tools or assistants).

## Goals

- Maintain **one source file per character** with narrative and factual text about that character.
- Run a **RAG pipeline** that turns that text into searchable vectors with rich **metadata**.
- Expose retrieval through an **MCP server** that queries FAISS and applies **re-ranking** before responding.

## Data layout

- **Character files** — Plain text (or similarly simple) documents, one file per character, used as the canonical source for indexing.  
  Chunks and metadata are derived from these files so answers stay traceable to specific characters and sections.

## Repository layout

```
rag-with-mcp/
├── data/
│   ├── characters/     # One source file per character (tracked in git)
│   └── index/          # Built FAISS index + serialized metadata (folder tracked; outputs gitignored)
├── src/
│   ├── rag/            # Ingest, chunking, metadata, embeddings, index build
│   └── mcp/            # MCP server: FAISS search, re-rank, return results
├── scripts/            # CLI helpers (e.g. build or refresh the index)
├── tests/
├── LICENSE
└── README.md
```

Generated artifacts under `data/index/` are excluded from version control via `.gitignore` (the directory itself stays in the repo with a `.gitkeep`).

## RAG pipeline

End-to-end flow:

1. **Ingest text** — Load content from the per-character files.
   - Per-character source documents live in `data/characters/`.
   - If the directory is empty, generate them first by running `python scripts/generate_character_files.py`.
2. **Chunking** — Split text into overlapping chunks sized for the embedding model.
   - Implemented by `scripts/build_chunks.py` using `src/rag/chunking.py`.
   - Default parameters: `--chunk-size-words 200` and `--chunk-overlap-words 40`.
   - Output: `data/index/chunks.jsonl` (one JSON record per chunk).
   - Each record includes: `chunk_id`, `character`, `source_file`, `chunk_index`, `start_char`, `end_char`, `text`, and `doc_meta` (the frontmatter metadata from the source character file).
3. **Metadata** — Attach structured fields (e.g. character name, source file, section, optional tags) to each chunk.
   - In this repo, the chunk JSON already contains `doc_meta` extracted from the character frontmatter.
4. **Embeddings** — Encode each chunk from `data/index/chunks.jsonl` with a chosen embedding model.
   - Implemented by `scripts/build_index.py` (uses `src/rag/embeddings.py`).
   - Default embedding model: `sentence-transformers/all-MiniLM-L6-v2` (configurable via `--embedding-model`).
   - Requires Python deps (see `requirements.txt`), including `sentence-transformers` and `faiss-cpu`.
   - Run: `python scripts/build_index.py`
5. **Vector store** — Build and persist the **FAISS** index for retrieval.
   - Implemented by `scripts/build_index.py` (uses `src/rag/faiss_index.py`).
   - Outputs (under `data/index/`):
     - `faiss.index` (FAISS index)
     - `chunk_ids.json` (ordered list of chunk ids)
     - `chunks_by_id.json` (chunk payload + metadata lookup by `chunk_id`)

This repository is intended as a **reference implementation** of that pipeline; adjust models, chunk sizes, and FAISS index parameters to match your environment.

## MCP server

The MCP layer sits on top of FAISS and implements the **retrieval API** for tools and agents:

1. **Search** — Query the FAISS index (embedding the query with the same model used at index time).
2. **Re-rank** — Refine the candidate set with a re-ranker (cross-encoder, score fusion, or another method) to improve ordering versus raw vector similarity alone.
3. **Return** — Respond with the top passages (and metadata) for the caller to ground generation or display.

## Project status

Scaffolding and documentation first; pipeline code, sample character files, and the MCP server will land in this repo as the implementation grows.

## License

Licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Marcelo Almeida
