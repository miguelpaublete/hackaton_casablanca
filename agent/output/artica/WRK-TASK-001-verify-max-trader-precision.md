---
id: WRK-TASK-001
type: spec
layer: work-task
scope: ephemeral
status: draft
confidence: medium
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: Silvia Menendez Saavedra
project: artica
tags: [precision, max-trader, kraken, bitstamp]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-08 09-45 CEST - Notas de Gemini.pdf
---

# Verify Max Trader Precision Handling

## Objective
Ensure Max Trader can handle precision discrepancies between Kraken and Bitstamp in a one-to-N configuration.

## Implementation Notes
- Double-check how Max Trader manages precision settings for one-to-N configurations.
- Confirm details with Arkaitz Alberdi Pérez.

## Acceptance Criteria
- [ ] Max Trader correctly reconciles transactions with eight decimal places.
- [ ] No errors occur during reconciliation due to precision discrepancies.
- [ ] Configuration changes are documented and shared with relevant teams.

## Test Plan
1. Simulate reconciliation scenarios with eight decimal places.
2. Validate results against expected outcomes.
3. Document findings and share with stakeholders.
