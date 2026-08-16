# RACI matrix — <domain>

Legend: **R** = Responsible (does the work) · **A** = Accountable (answers for
it, one per row) · **C** = Consulted (inputs before) · **I** = Informed (told
after).

Roles: Arch = architecture owner · Sec = security owner · Prod = product owner
· TechLead = technical lead · DPO = data protection officer · Legal · Dev ·
Ops · KB = knowledge base content owner.

| Activity | Dev | TechLead | Arch | Sec | Prod | DPO | Legal | Ops | KB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADR authoring | R | C | A | C | C | C | C | I | I |
| Security decisions | C | C | A | R | C | C | C | I | I |
| Spec changes | C | C | C | C | A | — | C | I | I |
| KB content changes | I | I | C | A | I | C | C | I | R |
| Data transfer/hosting | C | C | C | A | I | R | C | C | I |
| Releases / tags | R | A | C | C | C | — | — | I | I |
| Incident response | R | A | C | C | I | C | C | R | — |
