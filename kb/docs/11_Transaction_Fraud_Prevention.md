# Transaction Fraud Prevention

Reference for detecting and responding to transaction fraud on the sourcing
platform.

## Common patterns

1. **Fake supplier fronts.** New suppliers with no verifiable registration,
   no tax id and a short operating history claiming urgent large orders.
2. **Payment diversion.** Instructions change at the last minute to a new
   account or wallet with an "urgent" narrative.
3. **Phishing around documents.** Requests for login credentials, private keys
   or full identity documents outside the onboarding checklist.
4. **Money-laundering signals.** Structuring, mismatched declaration vs payment,
   or payments routed through unrelated entities.

## Detection rules

- Payment instructions that differ from the registered settlement details
  trigger a hold and a verification challenge.
- Document requests outside the jurisdiction checklist trigger a warning and a
  refusal path.
- Unusual velocity (many new orders, same IP/device across accounts) escalates
  to human review.
- Any flagged action is logged with an audit id before the block decision.

## Response escalation

1. **AUTO_BLOCK** for clear fraud signals (payment diversion, credential
   phishing).
2. **MANUAL_REVIEW** for ambiguous signals (velocity, mismatches) — always a
   human decision, never a silent AI block.
3. **NOTIFY** for benign-but-suspicious behavior that only warrants a warning.

## Guardrails

- Never expose detection heuristics in user-facing messages.
- AI assessments are always reviewable and logged; no silent auto-blocks.
- Minimise data: only the fields needed for the fraud check are processed.
