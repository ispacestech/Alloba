# Alloba — Infrastructure

Hosting and deployment reference for the Alloba gateway and the Alloba
Training engine.

## Target topology

```
Browser / client
      │ HTTPS
      ▼
 Alloba gateway  (alloba/gateway, port 8582)
      │            ├─ /v1/gateway + /v1/sourcing  (local)
      │            └─ /* → proxy
      ▼                     ▼
 ispaces Commerce        Ollama (local LLM)
 backend (8561)          embeddings + chat
      │
      ▼
 PostgreSQL / storage (backend-owned)

Browser / training client
      │ HTTPS
      ▼
 Alloba Training  (alloba/training, port 8020)
      │
      ├─ /api/v1 (modules, enrollments, sessions, certifications, reporting)
      ▼
 PostgreSQL (alloba-training-db)  ·  Ollama (optional generative branching)
```

## Port allocation (workspace registry)

| Port | Service | Owner |
| --- | --- | --- |
| 8080 | ispaces Go backend | ispaces |
| 8561 | ispaces Commerce / AfroMART backend | AfroMART |
| **8582** | **Alloba gateway** | **Alloba** |
| **8020** | **Alloba Training API** | **Alloba** |

8582 falls in the workspace 8500-8599 range reserved for workspace-specific
services; 8020 falls in the 8000-8099 backend range. Both are registered in
`../ispaces-design.md` (Port Allocation section).

## Deployment modes

### 1. Local development

```bash
pip install -e ".[dev]"
python ingest.py
python -m alloba            # 127.0.0.1:8582
```

### 2. Docker Compose (single host)

```bash
docker compose up --build
```

- `ALLOBA_BACKEND_URL` defaults to `http://host.docker.internal:8561` for
  host-run backends; override for a containerised backend.
- The `training` service uses its own `training-db` (PostgreSQL) and reads
  `ALLOBA_TRAINING_*` variables; in local dev it defaults to SQLite.
- `rag_index/` is mounted read-only so the image never needs to rebuild on KB
  refresh.
- Passwords/secrets use `${VAR:-default}` interpolation only (workspace rule).

### 3. Cloud (Docker Hub + GitHub)

- CI: `.github/workflows/ci.yml` runs lint + tests; a release workflow can push
  `alloba/gateway:<tag>` and `alloba/training:<tag>` to Docker Hub (same image,
  different `CMD`).
- The image is minimal (`python:3.12-slim`), secrets injected at runtime via
  environment, no `debug=True`.

## Runtime dependencies

| Dependency | Default | Required |
| --- | --- | --- |
| ispaces Commerce backend | `http://localhost:8561` | yes (proxied routes) |
| Ollama server | `http://127.0.0.1:11434` | yes (RAG + sourcing) |
| Embedding model | `nomic-embed-text` | yes (index build + search) |
| Chat model | `llama3.2:1b` | optional at runtime (fallbacks exist) |
| Prebuilt FAISS index | `./rag_index` | yes for search; build via `python ingest.py` |

## Health and observability

- `GET /v1/gateway/health` reports gateway version, RAG load state, backend
  reachability, and available endpoints.
- Compose healthcheck polls this endpoint.
- Structured logs are emitted to stdout (collected by the host platform).

## Security posture

- CORS allow-list via `ALLOBA_ALLOWED_ORIGINS` (never `*`).
- No pickle-based FAISS indices.
- Secrets only via environment; `.env` git-ignored.
- TLS termination is expected at the ingress/reverse proxy in front of the
  gateway (8582 is internal/trusted).
