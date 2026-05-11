---
id: ADR-003
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: tbd
project: artica
tags: [mercado, licensing, deactivation]
source_transcript: Deco Algo. ASE para generación del dump - 2026_03_05 17_30 CET - Notas de Gemini.pdf
---

# Decision to prioritize deactivation of Mercado instance

## Intent
Prioritize the deactivation of the obsolete Mercado instance (version 453) as the critical path for the project.

## Context
The Mercado instance (version 453) is considered obsolete and its deactivation is necessary to reduce licensing costs. However, the ASE system, which depends on Mercado for historical data dumps, must remain functional. Additionally, the licensing status of ASE needs to be clarified to ensure it can operate independently of Mercado.

## Decision
The deactivation of the Mercado instance will be prioritized as the critical path of the project. Cleaning up other obsolete systems, such as Trida and Safari, will be deferred to later phases.

## Rationale
Deactivating Mercado will lead to significant cost savings by eliminating its licensing fees. Ensuring ASE's functionality is critical for dependent processes like counterparty scenario generation. Delaying the cleanup of other systems allows the team to focus resources on the most impactful task.

## Consequences
- **Positive:** Reduced licensing costs and streamlined system architecture.
- **Negative:** Potential delays in addressing dependencies and cleaning up other obsolete systems.
- **Neutral:** Requires confirmation of ASE's licensing status and analysis of technical dependencies.

## Alternatives Considered
- **Deactivating all obsolete systems simultaneously:** Rejected due to resource constraints and the complexity of dependencies.
- **Maintaining Mercado instance:** Rejected due to high licensing costs and its obsolescence.

## Traceability
- Related discussions: Meeting on 2026-03-05 regarding Algoritmics decomissioning.
- Dependencies: ASE system functionality and licensing status.
