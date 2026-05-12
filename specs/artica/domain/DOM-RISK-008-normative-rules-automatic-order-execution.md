---
id: DOM-RISK-008
type: spec
layer: domain
domain: risk
subdomain: trading
status: draft
confidence: low
version: 1.0.0
created: 2026-05-12
updated: 2026-05-12
owner: tbd
project: artica
tags: [automatic-orders, connectivity, compliance]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-04-29 10-00 CEST - Notas de Gemini.pdf
---

# Normative rules for automatic order execution in Yulink

## Intent
Define the rules and constraints for automatic order execution in Yulink to ensure compliance with connectivity standards.

## Definition
### Concept
Automatic order execution in Yulink ensures periodic submission of orders to maintain connectivity and compliance with established norms.

### Rules
1. Orders beginning with '92' are automatically generated every two hours.
2. Automatic orders are queued and executed based on system availability.
3. Failed or expired orders must be logged and reviewed.

### Constraints
- Connectivity standards require periodic submission of orders.
- Orders must adhere to the established queueing and execution protocols.

### Examples
- An automatic order generated at 10:00 AM is queued and executed at 10:02 AM.
- A failed order due to system downtime is logged for review.

## Acceptance Criteria
- [ ] Automatic orders are generated every two hours.
- [ ] Orders comply with connectivity standards.
- [ ] Failed or expired orders are logged and reviewed.

## Evidence
- Meeting discussion confirming compliance with connectivity standards.
- Execution logs of automatic orders in Yulink.

## Traceability
- Related to discussions on automatic order execution during the meeting.
