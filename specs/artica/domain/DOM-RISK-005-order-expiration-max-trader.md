---
id: DOM-RISK-005
type: spec
layer: domain
domain: risk
subdomain: trading
status: draft
confidence: low
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: TBD
project: artica
tags: [max-trader, order-expiration, risk-management]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-05 11-30 CEST - Notas de Gemini.pdf
---

# Business rules for handling order expiration in Max Trader

## Intent
To define the business rules and constraints for handling order expiration in Max Trader.

## Definition
### Concept
Order expiration refers to the automatic cancellation or expiration of purchase orders in Max Trader due to system or market constraints.

### Rules
1. Orders should not expire automatically unless explicitly configured.
2. Orders that cannot be executed due to market constraints should be canceled rather than expired.
3. Expiration behavior must be logged and auditable for compliance purposes.

### Constraints
- Market volatility may impact the ability to execute purchase orders.
- System stability in SIT and Kraken environments must be ensured to prevent unintended expirations.

### Examples
- **Scenario 1**: A purchase order placed during high market volatility is canceled due to system constraints.
- **Scenario 2**: A purchase order expires due to a system restart in Kraken.

## Acceptance Criteria
- [ ] Orders are canceled instead of expired when execution fails.
- [ ] Logs are generated for all canceled or expired orders.
- [ ] System stability is maintained during high market volatility.

## Evidence
- Meeting notes from May 5, 2026.
- Observations from SIT and Kraken environments.

## Traceability
- Related to SIT and Max Trader stability discussions.
- Dependencies: ADR-005.
