---
id: ADR-002
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-05-12
updated: 2026-05-12
owner: TBD
project: sec-lending
tags: [example-generation, excel, methodology]
source_transcript: Copia de [Sec. Lending Undisclosed] Seguimiento Riesgos - 2026-05-11 13-30 CEST - Notas de Gemini.pdf
---

# Decision to use Excel for initial example generation

## Intent
To decide the methodology for generating initial examples for development purposes.

## Context
Due to the current state of development and unresolved issues regarding 'beneficial owner' codes, integrated testing is not feasible. The team needs a temporary solution to provide examples for validation and development.

## Decision
The team decided to use Excel for generating initial examples to support development and validation processes.

## Rationale
Excel provides a quick and flexible way to create examples without requiring full integration of systems, which is currently not possible due to unresolved dependencies.

## Consequences
- **Positive**: Enables the team to proceed with development while awaiting resolution of dependencies.
- **Negative**: Examples generated in Excel may require additional effort to transition to integrated systems later.
- **Neutral**: This decision does not impact the final implementation methodology.

## Alternatives Considered
- **Integrated Testing**: Not feasible due to unresolved dependencies.
  - **Pros**: Direct validation within the system.
  - **Cons**: Blocked by unresolved issues.
- **Manual Example Creation**: More time-consuming and error-prone.
  - **Pros**: No dependency on tools.
  - **Cons**: Inefficient and harder to scale.

## Traceability
- Related discussions: Meeting notes from May 11, 2026.
- Dependencies: Confirmation of 'beneficial owner' codes.
