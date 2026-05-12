---
id: ADR-009
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-05-12
updated: 2026-05-12
owner: tbd
project: artica
tags: [asset-allocation, testing, liquidity]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-04-29 10-00 CEST - Notas de Gemini.pdf
---

# Allow temporary asset allocation changes to unblock test execution

## Intent
Unblock test execution by allowing temporary changes in asset allocation between exchanges.

## Context
The testing environment for Kraken integration has been hindered by a lack of liquidity in Bitstamp, preventing the execution of necessary test cases. Current asset allocation assigns Bitcoin to Kraken and Ethereum to Bitstamp, which limits flexibility.

## Decision
Allow temporary changes in asset allocation, such as pointing Bitcoin to Bitstamp, to enable the continuation of testing without blocking.

## Rationale
This approach provides immediate relief to the testing team, enabling progress in the absence of liquidity in Bitstamp. It avoids delays in critical test cases while maintaining operational flexibility.

## Consequences
- **Positive**: Enables testing to proceed without waiting for liquidity improvements.
- **Negative**: Temporary changes may introduce inconsistencies in test results.
- **Neutral**: No long-term impact expected as changes are temporary.

## Alternatives Considered
1. **Wait for liquidity to improve**
   - **Pros**: Maintains consistency in asset allocation.
   - **Cons**: Delays testing indefinitely.
2. **Use a simulated environment for testing**
   - **Pros**: Avoids dependency on real liquidity.
   - **Cons**: Results may not reflect real-world conditions.

## Traceability
- Related to discussions on liquidity issues in Bitstamp during the meeting.
- Dependencies: None explicitly mentioned.
