---
id: ADR-001
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: TBD
project: artica
tags: [precision, kraken, bitstamp]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-08 09-45 CEST - Notas de Gemini.pdf
---

# Precision Adjustment for Kraken and Bitstamp

## Intent
Align precision handling between Kraken and Bitstamp to resolve discrepancies in decimal precision during trading and reconciliation.

## Context
Kraken uses eight decimal places for Ethereum, while Bitstamp uses six. This discrepancy has caused inconsistencies in reconciliation processes. Adjustments have been made to align Kraken's precision to eight decimals, but concerns remain regarding how Max Trader will handle disparate precisions in a one-to-N configuration.

## Decision
Adjust Kraken's precision to eight decimals and verify Max Trader's handling of precision discrepancies in the one-to-N configuration.

## Rationale
Aligning precision ensures consistency in reconciliation processes and avoids errors caused by mismatched decimal places. Eight decimals were chosen to match Kraken's existing standard.

## Consequences
- **Positive**: Improved consistency in reconciliation processes.
- **Negative**: Potential complexity in Max Trader's configuration for handling disparate precisions.
- **Neutral**: No impact on other systems outside Kraken and Bitstamp.

## Alternatives Considered
- **Keep existing precision settings**: Rejected due to ongoing reconciliation issues.
- **Standardize to six decimals across both platforms**: Rejected as it would require significant changes to Kraken's existing processes.

## Traceability
- Related discussions: May 8, 2026 meeting notes.
- Related systems: Max Trader, Kraken, Bitstamp.
