# Alloba — System Architecture

Technical architecture of the Alloba gateway. Companion to
`enterprise-architecture.en.md` (why) and `infrastructure.en.md` (where).

## Components

```
┌────────────────────────────── Alloba (port 8582) ─────────────────────────────┐
│                                                                                │
│  fastapi app (alloba/main.py)                                                   │
│   ├─ CORS middleware (allow-list from ALLOBA_ALLOWED_ORIGINS)                   │
│   ├─ /v1/gateway  routers/gateway.py   search + chat + health                   │
│   ├─ /v1/sourcing routers/sourcing.py  run + chat + sessions + tools            │
│   └─ /*           proxy.py             transparent proxy to backend             │
│                                                                                │
│  knowledge engine                     sourcing agent                           │
│  ┌───────────────────────┐           ┌───────────────────────────┐            │
│  │ rag.KnowledgeBase      │           │ sourcing.SourcingAgent     │            │
│  │  lazy safe FAISS load  │◄──────────│  intent → search → ground │            │
│  │  similarity + scores   │           │  → synthesize (LLM)       │            │
│  └───────────┬───────────┘           └────────────┬──────────────┘            │
│              │ faiss_store (index.faiss +         │ tools: search_catalog,     │
│              │ index.safe.json, no pickle)        │ get_product, compare,      │
│              │                                     │ compliance_check            │
│  OllamaEmbeddings ◄───────────── Ollama ──────────► OllamaClient (chat)         │
└────────────────────────────────────────────────────────────────────────────────┘
```

## Data flow — RAG search

1. `POST /v1/gateway/search` → `kb.search(query, k)`.
2. `KnowledgeBase` lazily loads the safe FAISS store from
   `ALLOBA_RAG_INDEX_DIR`.
3. Query is embedded (`OllamaEmbeddings`) and searched via
   `similarity_search_with_scores`.
4. Squared-L2 distances are mapped to 0..1 relevance scores.
5. Response returns `source`, `score`, `snippet` per hit.

## Data flow — grounded chat

1. `POST /v1/gateway/chat` → `kb.chat(query, k)`.
2. Retrieve top-k chunks → build a context block with source citations.
3. Send a system prompt ("answer only from context, cite sources") + the
   context to Ollama at low temperature (0.2).
4. If Ollama fails, `answer` is `None` and only `sources` are returned.
5. Every answer carries its `sources` for auditability.

## Data flow — sourcing

- **pipeline mode**: extract intent (JSON or keyword fallback) → catalog search
  → compliance grounding → LLM or template brief.
- **tools mode**: native tool-calling loop over `_TOOL_SCHEMAS` with
  `search_catalog`, `get_product`, `compare_products`, `compliance_check`.
- **auto mode**: uses tools only when the configured model supports them
  (`ALLOBA_AGENT_TOOL_MODELS`).

## Key decisions (summarised)

| Decision | Choice | ADR |
| --- | --- | --- |
| Serialization | safe FAISS (binary + JSON), refuse pickle | ADR-0002 |
| LLM interface | Ollama only, local-first | ADR-0004 |
| Gateway routing | explicit routes first, catch-all proxy | ADR-0001 |
| Config | pydantic-settings, `ALLOBA_` prefix | ADR-0003 |
| Catalog data | bundled JSON in package data | ADR-0005 |
| Concurrency | thread-safe lazy KB load | ADR-0006 |

See `docs/collaboration/adrs/`.
