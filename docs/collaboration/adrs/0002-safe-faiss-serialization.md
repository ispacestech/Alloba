# ADR-0002: Safe FAISS serialization — binary index + JSON docstore, no pickle

- **Status**: Accepted
- **Date**: 2026-08-15
- **Owner**: Security

## Context

The original standalone server persisted its FAISS index through
`langchain_community.vectorstores.FAISS`, which writes `index.pkl` and requires
`allow_dangerous_deserialization=True` to reload. The workspace security policy
explicitly forbids both. `langchain-community` is also being sunset.

## Decision

- Implement a minimal in-repo vector store (`src/alloba/faiss_store.py`):
  - `index.faiss` persisted via `faiss.write_index` / `read_index`;
  - docstore and `index_to_docstore_id` persisted as JSON (`index.safe.json`).
- Loading refuses any index that does not ship both files, and never unpickles.
- `allow_dangerous_deserialization` is never set anywhere in the codebase.
- Indices must be rebuilt with `python ingest.py`.

## Consequences

- Attack surface removed: no code execution from index files.
- Slightly larger index artifacts (JSON docstore) — acceptable for this scale.
- The old `index.pkl` indices are not loadable and must be rebuilt.

## Compliance

- `src/alloba/faiss_store.py`, `src/alloba/ingestion.py`, `src/alloba/rag.py`.
- No `pickle` import anywhere in `src/`.
