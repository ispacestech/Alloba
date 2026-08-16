# Alloba — Observability

How the Alloba gateway reports health, logs, metrics and audit trail. The
French version is `observability.fr.md`.

## Health endpoint

`GET /v1/gateway/health` returns:

| Field | Meaning |
| --- | --- |
| `service` | `"alloba"` |
| `version` | package version |
| `rag` | index load state (`loaded` / `missing` / `unsafe`) |
| `backend` | ispaces backend reachability (`ok` / `unreachable`) |
| `endpoints` | list of registered routes |

Used by the Docker healthcheck (interval 10 s, timeout 2 s, retries 3). A
missing index does not fail the healthcheck but is reported so operators can
rebuild.

## Logging

- Structured logs go to stdout (JSON lines), collected by the host platform
  (Docker logs, cloud logger, systemd).
- Request-level events log method, path, status, duration and correlation id.
- Audit entries follow `AuditLogEntry` (`src/alloba/models.py`) and are emitted
  for consequential AI actions: sourcing runs, compliance checks, LLM audit
  triggers.

## Auditability (Ethics by design)

- Every chat and sourcing turn carries a traceable id.
- Sourcing briefs record the tools used and the sources cited.
- The knowledge engine refuses pickle-based indices, so what is indexed is
  exactly what is in `kb/docs/`.

## Metrics (roadmap)

A future `/v1/metrics` (Prometheus format) is planned: RAG latency percentiles,
sourcing run counts by outcome, LLM failure rates. Tracking issue + ADR will
land with the implementation.

## Troubleshooting signals

| Signal | Interpretation | Action |
| --- | --- | --- |
| `rag: missing` in health | index never built | `python ingest.py` |
| `backend: unreachable` | proxy target down | start backend, check CORS/URL |
| repeated `null` chat answers | LLM down or context-poor | check Ollama, refresh KB |
| slow search | large corpus, no limit | verify `k` clamp `[1,20]`, chunk size |
