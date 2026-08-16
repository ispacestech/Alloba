# Alloba — Collaboration System

A lightweight, docs-based collaboration system for the Alloba project. It is
deliberately not a service: it lives in the repository so decisions travel with
the code.

## Goals

1. Every consequential decision is written down and findable.
2. Responsibilities are explicit (RACI), so nothing waits on a "someone".
3. Changes flow through a repeatable workflow with clear decision gates.
4. The decision history is bilingual at the summary level and precise in ADRs.

## Artifacts

| Artifact | Location | Purpose |
| --- | --- | --- |
| ADR | `docs/collaboration/adrs/NNNN-*.md` | Architecture decision record |
| Decision request | `docs/collaboration/templates/decision-request-template.md` | Proposal template |
| RACI | `docs/collaboration/templates/raci-template.md` | Responsibility matrix |
| ADR template | `docs/collaboration/templates/adr-template.md` | ADR skeleton |
| Decision log | `docs/collaboration/decision-log.{en,fr}.md` | Summary index (bilingual) |
| System doc | this file (system.en.md / system.fr.md) | Process definition |

## Workflow

```
1. Decide  → author writes a decision request using the template
2. Review  → relevant owners review; gate: owner approval required
3. Record  → ADR merged (scripts/new-adr.py), decision log updated
4. Build   → implementation branches off the decision
5. Verify  → CI (lint + tests) must pass before merge
6. Close   → implementation PR references the ADR number
```

## Decision gates

| Gate | Trigger | Who decides | Recorded as |
| --- | --- | --- | --- |
| Proposal accepted | decision request complete | ADR owner | new ADR |
| Architecture change | affects components/flow | architecture owner | ADR + architecture doc |
| Security posture | affects security rules | security owner | ADR (mandatory) |
| Spec change | changes behaviour | product owner | specs update + ADR |
| Release | CI green, image built | maintainer | git tag + Docker Hub |

## RACI (high level)

| Activity | R | A | C | I |
| --- | --- | --- | --- | --- |
| ADR authoring | author | architecture owner | tech leads | team |
| Security decisions | security owner | architecture owner | legal | team |
| Spec changes | product owner | product owner | tech leads | team |
| KB content | content owner | security owner | DPO | team |
| Code changes | developer | tech lead | reviewers | team |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## Language rule

- ADRs and templates: **English** (canonical technical records).
- Decision log and process docs: **EN + FR** side by side.

## New decision how-to

```bash
python scripts/new-adr.py "Title of the decision"
# → creates docs/collaboration/adrs/NNNN-title-of-the-decision.md
```

## Conventions

- One ADR per decision. Superseded ADRs keep their number and point to the
  replacement.
- Commit messages on decision artifacts reference the ADR id (e.g.
  `docs: record ADR-0002`).
- Decisions are never buried in chat; they must end up in the decision log.
