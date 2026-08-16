# Alloba — Roadmap

Planned evolution of the Alloba gateway, ordered by priority. The French
version is `roadmap.fr.md`. Every implemented item lands with an ADR in
`docs/collaboration/adrs/` and an update to `docs/specs.*`.

## Near term (next)

- **Metrics endpoint.** `GET /v1/metrics` in Prometheus format: RAG latency
  percentiles, sourcing outcome counts, LLM failure rates. Health continues to
  cover readiness; metrics cover performance.
- **Sourcing session persistence.** Store sessions to a bounded local store so
  interrupted runs can be resumed and audited after gateway restarts.
- **Region / language normalisation.** The intent extractor currently maps free
  text regions to codes; normalise the fallback regex so a region such as
  `africa` never arrives with leading whitespace.

## Mid term

- **Vector store options.** Add a second safe backend (Chroma with explicit
  serialization) selectable via `ALLOBA_VECTOR_STORE`, keeping FAISS safe mode
  as default. Both remain pickle-free.
- **Multi-model routing.** Route chat to the strongest available tool-capable
  model (e.g. `qwen3.6`) with fallback to `llama3.2:1b`, selected by
  `ALLOBA_CHAT_MODEL` with automatic health-based degradation.
- **KB versioning.** Tag index builds with the `kb/docs/` git commit and serve
  stale-index warnings in health instead of silent staleness.
- **Rate limiting.** Per-token buckets for `/v1/gateway/*` and
  `/v1/sourcing/*`, configured via environment, disabled by default.

## Long term

- **Marketplace agent.** Expand sourcing to compare suppliers across countries
  using the ECP knowledge engine, with compliance checks per jurisdiction.
- **Model marketplace for users.** Let tenants choose embedding/chat models
  with audited provenance and a "safe model" badge aligned with ispaces Ethics
  by design.
- **Federated deployments.** Multi-tenant gateways with per-tenant KB
  partitions and shared infrastructure, retaining local-first guarantees.

## Decision record

Each roadmap item, once approved, becomes an ADR. Open decision requests and
the RACI for evaluation live in `docs/collaboration/`.
