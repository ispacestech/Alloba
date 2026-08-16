# Contract Terms & Vigilance

Rules for reviewing supplier contracts and purchase orders for abusive,
inconsistent or non-compliant clauses.

## Core principles

1. **Read the whole contract.** Review clauses in context; a standalone clause
   can contradict the body, annexes or the order form.
2. **Red flags.** Flag clauses that shift unlimited liability to the buyer,
   allow unilateral price changes without notice, waive statutory rights, or
   impose excessive penalties.
3. **Consistency.** Verify the contract matches the negotiated order: quantity,
   price, Incoterm, payment terms and delivery window must be identical.
4. **No legal opinion.** The platform highlights risks; it never issues a legal
   opinion. Risk classifications are decision support for the buyer and their
   counsel.

## Review checklist

- [ ] Parties and governing law identified
- [ ] Price and payment terms match the order
- [ ] Incoterm and risk transfer stated consistently
- [ ] Delivery window and delay liability defined
- [ ] Liability caps, exclusions and indemnities explicit
- [ ] Termination and dispute resolution clauses present
- [ ] No clause contradicts statutory protections (buyer jurisdiction)
- [ ] Data protection and confidentiality scope clear

## Output contract

| Field | Meaning |
| --- | --- |
| `risk_level` | LOW / MEDIUM / HIGH |
| `flagged_clauses` | clause numbers with a one-line issue summary |
| `missing_clauses` | checklist items absent from the contract |
| `inconsistencies` | mismatches between contract and order |
| `recommendation` | PROCEED / HOLD / REFER_TO_COUNSEL |
