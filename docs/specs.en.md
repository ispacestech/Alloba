# Alloba — Specifications

Functional and technical specification baseline. Changes to behaviour update
this document and `architecture.en.md`, and are recorded as ADRs.

## Functional requirements

### FR-1 Gateway proxy
- **FR-1.1** The gateway exposes a single origin and transparently forwards any
  unmatched route to `ALLOBA_BACKEND_URL`.
- **FR-1.2** Responses preserve status, headers and body; 502 is returned with a
  JSON error when the backend is unreachable.
- **FR-1.3** `GET /` returns `{service, version, docs}`.

### FR-2 RAG search
- **FR-2.1** `POST /v1/gateway/search` returns ranked hits with `source`,
  `score`, `snippet`.
- **FR-2.2** `k` is clamped to `[1, 20]`; empty queries are rejected (422).
- **FR-2.3** Missing or unsafe index → 503 with a rebuild instruction.

### FR-3 Grounded chat
- **FR-3.1** `POST /v1/gateway/chat` returns `answer`, `model`, `sources`.
- **FR-3.2** The answer must be grounded: the system prompt forbids
  out-of-context answers; on LLM failure `answer` is `null` and `sources` are
  still returned.

### FR-4 Sourcing
- **FR-4.1** `POST /v1/sourcing/run` returns intent, results, sources and a
  brief. Brief falls back to a deterministic template when the LLM is down.
- **FR-4.2** `POST /v1/sourcing/chat` supports sessions; `GET
  /v1/sourcing/sessions/{id}` retrieves one (404 if missing).
- **FR-4.3** Tool endpoints `search`, `product`, `compare`, `compliance` are
  callable directly and by the agent.

### FR-5 Compliance engine
- **FR-5.1** Compliance answers cite their source documents.
- **FR-5.2** The index is built from `kb/docs/` by `python ingest.py` (or
  `scripts/build_index.py`) and stored with safe serialization only.

## Non-functional requirements

### NFR-1 Security (workspace policy)
- No pickle FAISS; no `allow_dangerous_deserialization`.
- CORS restricted to the allow-list; never `*`.
- No committed secrets; docker-compose uses `${VAR:-default}`.
- No `debug=True` in production entry points.

### NFR-2 Performance
- Gateway proxy timeout: 60 s; health check timeout: 2 s.
- KB is loaded lazily once and cached for the process lifetime.

### NFR-3 Reliability
- LLM outage degrades to templates, never to a crash.
- Backend outage degrades to 502 JSON, never to a hung connection.

### NFR-4 Bilingualism
- All user-facing documents exist in EN and FR.
- The assistant answers in the user's language.

### NFR-5 Testing
- The suite (29 tests) must stay green; CI runs ruff + pytest on every PR.

## Configuration contract

Prefix `ALLOBA_`. See `.env.example` for the full table. Invalid values must
fail fast at startup (pydantic-settings validation).

## API surface (summary)

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | service info |
| GET | `/v1/gateway/health` | health + RAG + backend state |
| POST | `/v1/gateway/search` | RAG search |
| POST | `/v1/gateway/chat` | grounded chat |
| POST | `/v1/sourcing/run` | full sourcing run |
| POST | `/v1/sourcing/chat` | conversational sourcing |
| GET | `/v1/sourcing/sessions/{id}` | session state |
| GET | `/v1/sourcing/catalog` | catalog metadata |
| POST | `/v1/sourcing/tools/*` | agent tools |
| /* | any | proxy to backend |
