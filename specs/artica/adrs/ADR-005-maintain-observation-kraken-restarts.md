---
id: ADR-005
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: TBD
project: artica
tags: [kraken, sit, stability]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-05 11-30 CEST - Notas de Gemini.pdf
---

# Decision to maintain observation on Kraken restarts to ensure SIT stability

## Intent
To address the stability issues in the SIT environment caused by frequent restarts in Kraken.

## Context
During the meeting, it was noted that the SIT environment experienced stability issues due to frequent restarts in Kraken. These restarts were suspected to be the root cause of order expiration issues in Max Trader.

## Decision
The team decided to maintain observation on the SIT environment and coordinate with Kraken to minimize restarts in the demo environment to improve stability.

## Rationale
Minimizing restarts in the demo environment is expected to reduce instability and prevent recurrence of the order expiration issue in Max Trader. Continuous observation will help identify if the issue persists and determine the root cause.

## Consequences
- **Positive**: Improved stability in the SIT environment, potentially resolving the order expiration issue.
- **Negative**: Requires ongoing monitoring and coordination with Kraken.
- **Neutral**: No immediate resolution to the underlying issue.

## Alternatives Considered
- **Immediate intervention in Kraken's demo environment**: Rejected due to lack of clear evidence of the root cause.
- **No observation or coordination**: Rejected as it would risk recurrence of the issue.

## Traceability
- Related to SIT environment stability discussions.
- Mentioned in the meeting notes from May 5, 2026.
