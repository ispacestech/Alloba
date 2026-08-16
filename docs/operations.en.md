# Alloba — Operations Runbook

Operational procedures for building, testing, running, updating and backing up
the Alloba gateway. The French version is `operations.fr.md`.

## Build & test loop

```bash
pip install -e ".[dev]"
ruff check .            # lint
ruff format --check .   # format
pytest                  # suite (must stay green)
```

Wheel build (cloud readiness):

```bash
pip wheel . --no-deps -w dist/
```

## Local run

```bash
python ingest.py            # rebuild the FAISS index from kb/docs/
python -m alloba            # serve on 127.0.0.1:8582
```

Health check: `curl http://127.0.0.1:8582/v1/gateway/health`

## Docker

```bash
docker compose up --build
docker compose ps
docker compose logs -f gateway
```

- `rag_index/` is mounted read-only, so a KB refresh never forces a rebuild.
- Stop: `docker compose down` (add `-v` only when you intend to drop data).

## Knowledge base refresh

1. Add or edit documents in `kb/docs/`.
2. Rebuild the index:

```bash
python ingest.py
```

3. Verify the chunk count and that the new docs are reachable:

```bash
python -c "from alloba.rag import KnowledgeBase; kb=KnowledgeBase(); print(kb.search('your topic', k=3))"
```

4. The index uses safe serialization only (`index.faiss` + `index.safe.json`);
   never replace it with a pickle-based FAISS store.

## Upgrades

- Version bumps live in `pyproject.toml` (single source of truth).
- Behaviour changes must update `docs/specs.*`, `docs/architecture.*` and, when
  relevant, a new ADR (see `docs/collaboration/adrs/`).
- After a change: lint, format, pytest, rebuild wheel, re-ingest if the KB
  schema or chunking changed.

## Backup

The gateway is stateless — nothing to back up at runtime. The durable assets
are:

| Asset | Location | Action |
| --- | --- | --- |
| Knowledge corpus | `kb/docs/` | version-controlled |
| Built index | `rag_index/` | rebuildable via `python ingest.py` |
| Catalog | `src/alloba/data/products.json` | version-controlled |

No SQL database is owned by the gateway itself; transactional data lives in the
backend it proxies to.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| 503 on search/chat | missing or unsafe index | run `python ingest.py` |
| 502 on unmatched route | backend down | start ispaces Commerce backend |
| LLM chat returns `null` answer | Ollama down | check `127.0.0.1:11434`; fallbacks serve sources only |
| Wrong/incomplete grounding | stale index | rebuild index, verify `kb/docs/` |
