# Alloba — Documentation

Documentation is published bilingually: every document has an English (EN) and
a French (FR) version, kept side by side. La documentation est publiée en
bilingue : chaque document a une version anglaise (EN) et française (FR).

## Index

| Document | EN | FR |
| --- | --- | --- |
| Brand identity | [brand.en.md](brand.en.md) | [brand.fr.md](brand.fr.md) |
| Enterprise architecture | [enterprise-architecture.en.md](enterprise-architecture.en.md) | [enterprise-architecture.fr.md](enterprise-architecture.fr.md) |
| Infrastructure | [infrastructure.en.md](infrastructure.en.md) | [infrastructure.fr.md](infrastructure.fr.md) |
| System architecture | [architecture.en.md](architecture.en.md) | [architecture.fr.md](architecture.fr.md) |
| Specifications | [specs.en.md](specs.en.md) | [specs.fr.md](specs.fr.md) |
| Knowledge management | [knowledge-management.en.md](knowledge-management.en.md) | [knowledge-management.fr.md](knowledge-management.fr.md) |
| Operations runbook | [operations.en.md](operations.en.md) | [operations.fr.md](operations.fr.md) |
| Observability | [observability.en.md](observability.en.md) | [observability.fr.md](observability.fr.md) |
| Roadmap | [roadmap.en.md](roadmap.en.md) | [roadmap.fr.md](roadmap.fr.md) |
| Collaboration system | [collaboration/system.en.md](collaboration/system.en.md) | [collaboration/system.fr.md](collaboration/system.fr.md) |
| Decision log | [collaboration/decision-log.en.md](collaboration/decision-log.en.md) | [collaboration/decision-log.fr.md](collaboration/decision-log.fr.md) |
| CI scaffold (PipelineConfig release workflow) | [ci-scaffold/README.md](ci-scaffold/README.md) | same runbook (FR) |

## Architecture Record / ADR

Architecture decisions are recorded as ADRs in
[docs/collaboration/adrs/](collaboration/adrs/). ADRs are written in English
only (canonical technical records); their outcomes are summarised in the
bilingual decision log.

## Related external references

- ispaces platform: `../ispaces/docs/architecture.md`, `../ispaces/docs/SPECS.md`
- ispaces brand & design: `../ispaces-brand.md`, `../ispaces-design.md`
- Commerce backend specs: `../afromart/architecture.md`, `../afromart/specs.md`

## Conventions

- **Source of truth**: EN versions are authoritative for technical content;
  FR versions are faithful translations.
- **Docs-to-code**: any change that alters behaviour updates
  `docs/specs.*`, `docs/architecture.*` and, when it matters, an ADR.
