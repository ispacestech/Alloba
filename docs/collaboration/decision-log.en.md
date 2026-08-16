# Alloba — Decision Log

Chronological summary of architecture and governance decisions. Each entry
points to its ADR. The French version is `decision-log.fr.md`.

| # | Date | Decision | Status | ADR |
| --- | --- | --- | --- | --- |
| 1 | 2026-08-15 | Gateway routing: explicit routes first, transparent proxy for everything else | Accepted | [0001](adrs/0001-gateway-routing.md) |
| 2 | 2026-08-15 | Safe FAISS serialization: binary index + JSON docstore, no pickle, no `allow_dangerous_deserialization` | Accepted | [0002](adrs/0002-safe-faiss-serialization.md) |
| 3 | 2026-08-15 | Configuration via pydantic-settings with `ALLOBA_` env prefix | Accepted | [0003](adrs/0003-configuration-prefix.md) |
| 4 | 2026-08-15 | Local-first LLM interface (Ollama); cloud provider requires a new ADR | Accepted | [0004](adrs/0004-local-first-ollama.md) |
| 5 | 2026-08-15 | Supplier catalog shipped as bundled package data (`data/products.json`, 55 products) | Accepted | [0005](adrs/0005-bundled-catalog.md) |
| 6 | 2026-08-15 | Lazy, thread-safe knowledge base loading; missing index → 503 with rebuild instruction | Accepted | [0006](adrs/0006-lazy-kb-loading.md) |

## Process

New decisions follow the workflow in `system.en.md`: decision request → review
→ ADR → implementation → CI → close.
