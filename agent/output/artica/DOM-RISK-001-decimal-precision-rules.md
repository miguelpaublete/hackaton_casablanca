---
id: DOM-RISK-001
type: spec
layer: domain
domain: risk
subdomain: reconciliation
status: draft
confidence: low
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: TBD
project: artica
tags: [precision, reconciliation, kraken, bitstamp]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-08 09-45 CEST - Notas de Gemini.pdf
---

# Decimal Precision Rules for Reconciliation

## Intent
Define rules for handling decimal precision discrepancies during reconciliation processes between trading platforms.

## Definition
### Concept
Decimal precision refers to the number of digits after the decimal point used in financial calculations.

### Rules
1. Kraken must use eight decimal places for Ethereum transactions.
2. Bitstamp must use six decimal places for Ethereum transactions.
3. Reconciliation systems must align precision settings to the higher standard (eight decimals).

### Constraints
- Regulatory requirements for precision handling must be adhered to.
- Systems must ensure no data loss or rounding errors during reconciliation.

### Examples
- Kraken transaction: 0.12345678 ETH.
- Bitstamp transaction: 0.123456 ETH.
- Reconciled transaction: 0.12345678 ETH.

## Acceptance Criteria
- [ ] Reconciliation processes handle eight decimal places without errors.
- [ ] Max Trader configuration supports one-to-N precision handling.
- [ ] No rounding errors occur during reconciliation.

## Evidence
- May 8, 2026 meeting notes.
- Test results from Kraken and Bitstamp.

## Traceability
- Related ADR: ADR-001.
- Related systems: Max Trader, Kraken, Bitstamp.
