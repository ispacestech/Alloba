# ADR-0006: Lazy, thread-safe knowledge base loading

- **Status**: Accepted
- **Date**: 2026-08-15
- **Owner**: Architecture

## Context

Loading the FAISS index at import time would slow startup and crash the gateway
on machines where Ollama or the index is not ready (e.g. CI, health probes).
Loading on every request would be wasteful.

## Decision

- `KnowledgeBase` loads the index lazily on first use, guarded by a lock so
  concurrent requests trigger a single load.
- The loaded store is cached for the process lifetime; health reports
  `rag.loaded` and `rag.chunks`.
- Missing/corrupt/unsafe index raises `RagIndexError`, surfaced as HTTP 503 with
  a rebuild instruction.

## Consequences

- Fast, resilient startup; graceful degradation.
- Index refreshes require a process restart (documented in knowledge management).
- Thread-safety cost is negligible (one-time lock).

## Compliance

- `src/alloba/rag.py` (`_ensure_loaded`), `src/alloba/faiss_store.py`
  (`load_vector_store`), `tests/test_gateway.py` (503 on missing index).
