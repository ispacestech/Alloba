# Shipping Terms & Incoterms

Reference for Incoterms selection, freight booking and delivery promises on the
sourcing platform.

## Incoterms basics

1. **Incoterms 2020 are the default** for all quotes unless a local rule is
   explicitly documented and recorded per order.
2. **Risk transfer.** Each Incoterm defines exactly where risk passes from
   seller to buyer. The platform must state the chosen term and its risk point
   on every quote and order.
3. **Cost split.** Every Incoterm implies a cost split (carriage, insurance,
   terminal handling, clearance). The quote must show the cost items the term
   includes.

## Term selection guidance

| Need | Preferred term |
| --- | --- |
| Buyer controls freight | FOB / FCA |
| Seller organizes carriage to destination | CFR / CPT / CIP / DAP |
| Door delivery with import cleared | DDP (only when seller can clear legally) |
| Buyer handles import clearance locally | DAP |

## Delivery promises

1. **No unsupported guarantees.** Never promise a shipping window that the 3PL
   partner (e.g. DHL/Maersk API) cannot confirm. Promises must be traceable to a
   partner quotation.
2. **Tracking required.** Every shipment carries a tracking number and status
   sourced from the logistics partner API.
3. **Delay handling.** Delay beyond the confirmed window triggers an automatic
   buyer notification and opens a dispute track (see Payment Terms & Disputes).

## Guardrails

- Quote with an Incoterm and its risk/cost point, never a bare "shipping
  included".
- Surface uncertainty when the destination clearance regime is unknown.
- Audit every delivery promise (cite partner and quotation id).
