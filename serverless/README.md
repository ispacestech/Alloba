# Serverless deployment notes — Alloba knowledge engine

Alloba deploys as a container gateway (see `docs/infrastructure.en.md`). This
folder documents how parts of the knowledge engine can run serverless on
platforms such as Vercel or Supabase Edge Functions.

## What can be serverless

- **Compliance search** (`/v1/gateway/search`): retrieval-only, no LLM
  dependency at runtime beyond the embedding model — a good candidate for an
  edge function backed by a prebuilt FAISS index on object storage.
- **Static catalog metadata** (`/v1/sourcing/catalog`): pure data, trivially
  cacheable.
- **Ingestion triggers**: `scripts/build_index.py` can be scheduled (cron /
  scheduled edge function) to rebuild the index whenever `kb/docs/` changes.

## What should stay containerised

- **Grounded chat** (`/v1/gateway/chat`) and **agentic sourcing** depend on
  Ollama for local-first inference (ADR-0004). Keep them behind the gateway.
- Anything that proxies platform transactions.

## Recommended split

```
edge (serverless)   → search, catalog info, static docs, ingest schedule
gateway (container) → chat, sourcing agent, proxy, health
```

## Security reminders

- Never ship FAISS index artifacts that require pickle; use the safe binary +
  JSON format from `src/alloba/faiss_store.py`.
- Environment secrets only; keep `.env` out of version control.
- CORS restricted to the frontend origin(s), never `*`.
