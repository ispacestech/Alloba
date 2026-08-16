# Infrastructure stack (intended toolchain)

The lean, open-source stack considered for the platform's non-gateway layers.
Alloba itself requires only Ollama + a backend (see `docs/infrastructure.en.md`).

| Tool | Role | Status in Alloba |
| --- | --- | --- |
| Ollama | Local LLM runtime (chat + embeddings) | Used (ADR-0004) |
| Strapi | Headless CMS (content) | Platform layer (optional) |
| Appwrite | Backend-as-a-service (auth, DB, storage) | Platform layer (optional) |
| Novu | Notifications | Platform layer (optional) |
| ToolJet | Low-code internal tooling | Platform layer (optional) |
| Medusa | Headless commerce engine | Platform layer (optional) |

## Plan

1. Keep Alloba thin: only FastAPI + Ollama + safe FAISS.
2. Push content/commerce/notifications to the platform backend (8561) and the
   optional services above.
3. Register each new service's port in the workspace port table
   (`ispaces-design.md`) when it goes live.

## GETI (guidance)

"GETI" here refers to generating, evaluating, testing and iterating on the
infrastructure decisions — record each change as an ADR before wiring new
services into compose files.
