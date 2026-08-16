# Alloba — Knowledge Management

Lifecycle and governance of the compliance knowledge base (`kb/`) and the FAISS
index.

## Purpose

The knowledge base is the single source of truth the AI grounds on. It is
governed, versioned and rebuildable from `kb/docs/` at any time.

## Content policy

- Only approved, citable documents live in `kb/docs/`. Draft material is not
  indexed.
- Every document carries governance metadata (see `models.py`
  `DocumentMetadata`): `type`, `status`, `sensitivity_level`.
- Sources referenced by tests and compliance answers must exist in `kb/docs/`
  (e.g. `00_Conformite_Plateforme.md`, `12_Checklist_Conformite_ISO.md`).

## Index lifecycle

```
edit kb/docs/* → python ingest.py (or scripts/build_index.py)
     → split (800/150) → embed (nomic-embed-text) → safe save
     → rag_index/{index.faiss, index.safe.json}
     → gateway loads lazily and caches for process lifetime
```

- **Idempotent**: rebuilding replaces the index atomically.
- **Safe only**: pickle-based indices are refused at load time; if `index.pkl`
  appears, rebuild with `python ingest.py`.
- **Refresh**: changing `kb/docs/` requires re-running ingestion; the running
  gateway picks up the new index on restart.

## Chunking parameters

| Parameter | Value | Rationale |
| --- | --- | --- |
| chunk_size | 800 | good balance for compliance prose |
| chunk_overlap | 150 | preserves context across chunk borders |
| retrieval k | 4 (chat), 3 (grounding) | short enough for low-token models |

## Context trimming

`context.optimize_context(snippets, token_limit)` keeps only the most relevant
snippets within a budget, so low-context models (e.g. `llama3.2:1b`) are not
overwhelmed.

## Query routing

- `/v1/gateway/search` — raw retrieval, no LLM.
- `/v1/gateway/chat` — grounded synthesis with citations.
- `/v1/sourcing/tools/compliance` — compliance check used by the sourcing agent.

## Retention and audit

- Every grounded answer returns `sources` (audit trail).
- `AuditLogEntry` models each interaction (`read`, `edit`, `generate`).
- Documents follow the governance statuses `draft → approved → deprecated`;
  `audited` marks a document that passed a formal review.

## References

- Safe FAISS store: `src/alloba/faiss_store.py`
- Ingestion: `src/alloba/ingestion.py`
- Governance models: `src/alloba/models.py`
