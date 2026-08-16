# Payment Terms & Dispute Handling

Reference rules for payment terms, escrow and dispute escalation on the
sourcing platform.

## Payment terms

1. **Default terms by tier.** Standard terms are defined per supplier tier and
   recorded with each order: advance payment percentage, balance against
   documents, and credit terms where approved.
2. **Payment methods.** Supported methods are the ones the ECP fee schedule
   documents; any method outside it must be flagged before checkout.
3. **No off-platform settlement.** The platform must never encourage payments
   outside its settlement rails; that is a compliance violation.

## Dispute handling

1. **Escalation ladder.** Dispute → merchant conversation → platform mediation →
   recorded decision. Each step is timestamped and audited.
2. **Evidence based.** Decisions reference order data, messages, tracking and
   inspection results. A decision without cited evidence is never final.
3. **Time limits.** Each ladder step has a documented deadline; expiry escalates
   automatically.
4. **LLM audit.** Any AI-assisted dispute assessment logs an `LLM Audit` entry
   (ISO 42001 requirement) and is reviewable by a human.

## Escrow rules

- Escrow funds are released only against the release condition stated at order
  creation (e.g. inspection pass, goods received).
- Partial release requires documented agreement between both parties.
- Refunds follow the same evidence path as disputes.

## Output contract

| Field | Meaning |
| --- | --- |
| `payment_terms` | summary of the agreed terms for the order |
| `escrow_state` | HELD / RELEASED / PARTIAL / REFUNDED |
| `dispute_status` | NONE / IN_MEDIATION / ESCALATED / DECIDED |
| `evidence_refs` | order, message and inspection ids backing the decision |
