# Alloba — Enterprise Architecture

This document maps business capability to IT capability. It is the "why" layer
above `architecture.en.md` and `infrastructure.en.md`.

## Business context

The business operates a Pan-African B2B marketplace (ispaces Commerce /
AfroMART). Buyers and suppliers transact cross-border; trust and compliance are
the two business-critical assets.

## Capability map

| Business capability | IT capability | Owning component |
| --- | --- | --- |
| Discover products | Search + filter catalog | Alloba `catalog.py` / backend search |
| Source intelligently | Agentic sourcing briefs | Alloba `sourcing.py` |
| Buy with confidence | Supplier verification | Backend + `kb/docs/05` |
| Stay compliant | Compliance knowledge engine | Alloba RAG (`rag.py`) |
| Integrate partners | Open API + transparent proxy | Alloba `main.py` / `proxy.py` |
| Govern the platform | Decision records, RACI, ADRs | `docs/collaboration/` |
| Operate ethically | AI guardrails + audit trail | `kb/docs/01`, `models.py` |

## Guiding principles

1. **Single entry point** — the gateway is the one contract for clients; the
   platform backend is interchangeable behind it.
2. **Grounded AI** — no AI output without citable sources.
3. **Compliance first** — security and data-protection decisions are made before
   features, and recorded.
4. **Progressive integration** — Alloba is standalone today and integrates with
   the ispaces concept engine when it is available.
5. **Bilingual operations** — business documents are maintained in EN and FR.

## Stakeholders and concerns

| Stakeholder | Concern | Where it is handled |
| --- | --- | --- |
| Buyers | Trustworthy, fast sourcing | Sourcing agent, catalog |
| Suppliers | Fair listing and verification | `kb/docs/05_Supplier_Verification.md` |
| Regulators | GDPR, ISO 27001, AI Act | `kb/docs/00`, `12`, `04` |
| Engineers | Clear, tested code | `pyproject.toml`, CI, tests |
| Ops | Reproducible cloud deployment | `infrastructure.en.md`, compose |

## Decision flow

All decisions that shape these capabilities are recorded through the
collaboration system: proposal → review → ADR → implementation. See
`docs/collaboration/system.en.md`.
