# Alloba

Alloba is the gateway and agentic sourcing service for **ispaces Commerce**
(AfroMART) — a Pan-African B2B marketplace. It is the rebranded successor of
the standalone Afromart server, organised into a clean, cloud-ready monorepo.
It also hosts **Alloba Training**, the immersive micro-training / certification
engine (rebranded successor of the OnboardXR service).

> Version: 0.3.0 · License: MIT · Français : voir [README.fr.md](README.fr.md)

## What it does

- **API gateway** — a single entry point that transparently proxies every
  platform route to the ispaces Commerce backend (default `http://localhost:8561`).
- **Ethical AI compliance knowledge engine** — grounded RAG over compliance
  documents (`kb/docs/`) using a **safe** FAISS index (binary + JSON, no pickle,
  no `allow_dangerous_deserialization`).
- **Agentic sourcing** — orchestrated pipeline and (optional) native tool-calling
  loop that builds sourcing briefs grounded in the catalog and compliance
  context.
- **Alloba Training** — immersive VR/AR micro-training and certification engine
  (scenario branching, per-skill scoring, telemetry engagement, HR export).

## Repository layout

```
.
├── src/alloba/          # gateway + knowledge engine + sourcing agent (rebranded)
│   ├── faiss_store.py   # safe FAISS store (no pickle — security requirement)
│   ├── rag.py           # KnowledgeBase (lazy load, grounded chat)
│   ├── ingestion.py     # index builder (chunk → embed → safe save)
│   ├── context.py       # token-budget context trimming
│   ├── models.py        # governance models (DocumentMetadata, RAGResponse, AuditLogEntry)
│   ├── catalog.py       # bundled supplier catalog (55 products)
│   ├── sourcing.py      # SourcingAgent (pipeline + tools loop)
│   ├── proxy.py         # transparent backend proxy
│   ├── routers/         # /v1/gateway and /v1/sourcing endpoints
│   └── training/        # Alloba Training — immersive micro-training/certification API
├── kb/docs/             # compliance knowledge documents (ingested by RAG)
├── prompts/             # bilingual (en/fr) prompt library (incl. agent prompts)
├── docs/                # brand, architecture, collaboration — EN + FR versions
│   └── ci-scaffold/     # PipelineConfig release workflow (runbook + templates)
├── scripts/             # new-adr.py, build_index.py
├── serverless/          # notes for serverless deployment of the knowledge engine
├── tests/               # pytest suite (gateway + training)
├── brand/               # brand SVG marks (ispaces + Alloba/AfroMART)
├── ssl/                 # local TLS material for Ollama (git-ignored)
└── archive/original/    # provenance copy of the pre-rebrand sources
```

## Quick start

Prerequisites: Python 3.11+, [Ollama](https://ollama.com) running with
`llama3.2:1b` and `nomic-embed-text`.

```bash
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -e ".[dev]"
python ingest.py          # build the FAISS knowledge index from kb/docs
python -m alloba          # start the gateway on 127.0.0.1:8582
```

Start the Alloba Training API separately (SQLite in dev):

```bash
uvicorn alloba.training.main:app --reload --port 8020   # docs at /docs
```

Or with Docker:

```bash
docker compose up --build
```

Open <http://127.0.0.1:8582/v1/docs> for the interactive API docs.

## Configuration

All settings are read from environment variables prefixed with `ALLOBA_` (see
[`.env.example`](.env.example)). Never hardcode secrets — copy `.env.example` to
`.env` and keep `.env` out of version control.

| Variable | Default | Purpose |
| --- | --- | --- |
| `ALLOBA_BACKEND_URL` | `http://localhost:8561` | Platform backend to proxy |
| `ALLOBA_PORT` | `8582` | Gateway port |
| `ALLOBA_RAG_INDEX_DIR` | `./rag_index` | FAISS index location |
| `ALLOBA_RAG_DOCS_DIR` | `./kb/docs` | Knowledge documents to index |
| `ALLOBA_OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Ollama endpoint |
| `ALLOBA_LLM_MODEL` | `llama3.2:1b` | Chat/sourcing model |
| `ALLOBA_EMBEDDING_MODEL` | `nomic-embed-text` | Embedding model |
| `ALLOBA_AGENT_MODE` | `auto` | `pipeline` \| `tools` \| `auto` |
| `ALLOBA_ALLOWED_ORIGINS` | comma-separated list | CORS allow-list — never `*` |

Alloba Training reads its own variables under the `ALLOBA_TRAINING_` prefix
(`ALLOBA_TRAINING_DATABASE_URL`, `ALLOBA_TRAINING_ALLOWED_ORIGINS`,
`ALLOBA_TRAINING_API_KEY`, `ALLOBA_TRAINING_OLLAMA_BASE_URL`,
`ALLOBA_TRAINING_OLLAMA_MODEL` — see [`.env.example`](.env.example)).

## Tests

```bash
python -m pytest -q        # gateway + training suites
python -m ruff check src tests ingest.py scripts
python -m ruff format --check src tests ingest.py scripts
```

## Security notes (workspace policy)

- FAISS indices are serialised **without pickle** (`index.faiss` +
  `index.safe.json`). Unsafe indices are refused and must be rebuilt.
- CORS is always restricted via `ALLOBA_ALLOWED_ORIGINS` — never `*`.
- No `debug=True`, no committed secrets, docker-compose passwords use
  `${VAR:-default}` interpolation.
- Env var naming uses the project prefix `ALLOBA_`; shared infrastructure vars
  (`OLLAMA_BASE_URL`, etc.) stay bare where they appear in shared compose files.

## Cloud publishing

- GitHub Actions CI: `.github/workflows/ci.yml` runs lint + tests on push/PR.
- The image is built with `docker build -t alloba/gateway:0.3.0 .` and can be
  pushed to Docker Hub under an `alloba/*` namespace (`alloba/gateway` and
  `alloba/training` share the same image; only the `CMD` differs).

## Documentation index

- [docs/README.md](docs/README.md) — index of the EN/FR documentation set.
- [docs/architecture.en.md](docs/architecture.en.md) — system architecture.
- [docs/enterprise-architecture.en.md](docs/enterprise-architecture.en.md) —
  business/IT alignment.
- [docs/infrastructure.en.md](docs/infrastructure.en.md) — hosting and deployment.
- [docs/specs.en.md](docs/specs.en.md) — functional and technical specifications.
- [docs/knowledge-management.en.md](docs/knowledge-management.en.md) — RAG KB lifecycle.
- [docs/collaboration/system.en.md](docs/collaboration/system.en.md) — the
  collaboration system (workflow, RACI, ADRs).

## Acknowledgements

Brand system by **ispaces** ("Ethics by design.") and **AfroMART** ("Trade that
grows Africa.") — see `brand/` and `docs/brand.en.md`.
