# Customs & Tariff Classification

Rules for classifying products and computing landed cost for cross-border
sourcing on the platform.

## Core principles

1. **HS codes first.** Every product must carry an HS (Harmonized System) code
   at the six-digit level before cross-border quotes are produced. Two-digit
   chapters alone are insufficient for duty estimation.
2. **Single classification per order line.** Each order line is classified once;
   the code is recorded with the supplier and reused for quotes, unless the
   buyer's declared use changes the chapter.
3. **Landed cost transparency.** Quoted prices must separate: FOB price, freight,
   insurance, duty estimate and clearance fees. Never merge them into a single
   opaque number.
4. **No legal advice.** Classification output is an estimate for sourcing
   decisions, not a binding customs ruling. Flag items as
   `ESTIMATE` unless backed by a ruling document in the knowledge base.

## Classification workflow

1. Parse the product description and declared use.
2. Match to the HS nomenclature via the knowledge engine.
3. Apply chapter notes and exclusions for the destination country.
4. Attach a confidence level: `HIGH` when the match is unambiguous,
   `MEDIUM` when the description is ambiguous, `LOW` when a ruling is advised.

## Output contract

| Field | Meaning |
| --- | --- |
| `hs_code` | six-digit code (or eight when locally required) |
| `hs_chapter` | two-digit chapter |
| `confidence` | HIGH / MEDIUM / LOW |
| `duty_estimate_pct` | estimated ad valorem duty range |
| `notes` | exclusions, ruling advice, documentation required |

## Guardrails

- Never claim a binding ruling without a cited source document.
- Never compute duty for a product whose HS code confidence is LOW without
  surfacing the uncertainty to the buyer.
- Audit every classification used in a quote (`AuditLogEntry`).
