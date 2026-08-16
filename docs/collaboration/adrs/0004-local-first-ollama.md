# ADR-0004: Local-first LLM interface (Ollama)

- **Status**: Accepted
- **Date**: 2026-08-15
- **Owner**: Architecture

## Context

Grounded chat and sourcing briefs need an LLM. Cloud LLMs would send
marketplace/compliance data to third parties, conflicting with data sovereignty
and the "Ethics by design" brand position.

## Decision

- The only LLM interface is a local Ollama server
  (`ALLOBA_OLLAMA_BASE_URL`, default `http://127.0.0.1:11434`).
- Embeddings: `OllamaEmbeddings` (default `nomic-embed-text`).
- Chat/sourcing: `ollama.Client` with low temperature (0.2).
- Every LLM call has a deterministic fallback (template brief, `answer: null`).

## Consequences

- No data leaves the host for inference; sovereignty claims stay credible.
- Capability depends on local models; tool-calling is auto-gated to models that
  support it (`ALLOBA_AGENT_TOOL_MODELS`).
- A future remote provider is possible but requires a new ADR and a data-flow
  impact review.

## Compliance

- `src/alloba/rag.py`, `src/alloba/sourcing.py`, `src/alloba/ingestion.py`.
