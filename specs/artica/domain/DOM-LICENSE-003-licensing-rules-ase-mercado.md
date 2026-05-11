---
id: DOM-LICENSE-003
type: spec
layer: domain
domain: licensing
subdomain: software
status: draft
confidence: low
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: tbd
project: artica
tags: [licensing, mercado, ase]
source_transcript: Deco Algo. ASE para generación del dump - 2026_03_05 17_30 CET - Notas de Gemini.pdf
---

# Licensing rules for ASE and Mercado systems

## Intent
Define the licensing rules and dependencies for the ASE and Mercado systems to support decision-making regarding their deactivation.

## Definition
### Concept
Licensing rules for the ASE and Mercado systems, including whether ASE has an independent license or is tied to Mercado's global license.

### Rules
1. Mercado (version 453 and version 47) is considered obsolete and its deactivation is prioritized.
2. ASE must remain functional to generate historical data dumps for dependent processes.
3. Confirmation is required to determine if ASE has an independent license or is tied to Mercado's global license.

### Constraints
- ASE's functionality is critical for generating historical data dumps used by counterparty scenario generation processes.
- ASE relies on daily market data exports from the Algoritmics Mercado database (IDB).

### Examples
- If ASE has an independent license, Mercado can be deactivated without impacting ASE's functionality.
- If ASE is tied to Mercado's license, alternative solutions must be explored to maintain ASE's functionality.

## Acceptance Criteria
- [ ] Confirmation of ASE's licensing status.
- [ ] Validation that ASE can generate historical data dumps independently of Mercado.
- [ ] Identification of alternative data sources for ASE if Mercado is deactivated.

## Evidence
- Meeting transcript from 2026-03-05 discussing licensing and dependencies.

## Traceability
- Related ADR: ADR-003 (Decision to prioritize deactivation of Mercado instance).
