# ECP Knowledge Engine

The ECP (Ethical Concept Platform) knowledge engine is the conceptual layer that
organises the compliance and business knowledge used by Alloba.

## What ECP is

ECP is a concept-driven engine: instead of only retrieving text chunks, it maps
knowledge onto a graph of ethical concepts (consent, data minimisation,
traceability, African data sovereignty, supplier verification, fair pricing).
Each document in the knowledge base is tagged with the concepts it relates to.

## How Alloba uses it

1. **Ingestion** — documents under `kb/docs/` are chunked and embedded into the
   safe FAISS index, tagged with concept metadata.
2. **Retrieval** — a query is embedded and the index returns the closest chunks,
   ranked by distance, together with the concepts they carry.
3. **Grounding** — answers synthesised by the LLM must reference the retrieved
   chunks; compliance checks return the source documents.
4. **Governance** — documents carry `DocumentMetadata` (status, sensitivity,
   type) so the engine only surfaces approved, auditable material.

## Concept taxonomy (initial)

- `consent` — lawful basis and user consent flows
- `minimisation` — data minimisation and purpose limitation
- `traceability` — audit trails and provenance
- `sovereignty` — African data sovereignty and local processing
- `verification` — supplier identity and compliance verification
- `fairness` — fair pricing and non-discriminatory treatment
- `safety` — product and platform safety obligations
- `security` — ISO 27001, encryption, access control

## Relationship to the ispaces concept engine

The ispaces project ships the reference concept engine (see
`ispaces/docs/architecture.md`). Alloba is the standalone consumer: it embeds the
compliance knowledge so the marketplace gateway can answer compliance questions
without depending on the full ECP service at runtime.
