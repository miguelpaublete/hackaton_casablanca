---
id: DOM-RISK-002
type: spec
layer: domain
domain: risk
subdomain: beneficial-owner
status: draft
confidence: low
version: 1.0.0
created: 2026-05-12
updated: 2026-05-12
owner: TBD
project: sec-lending
tags: [beneficial-owner, risk, codes]
source_transcript: Copia de [Sec. Lending Undisclosed] Seguimiento Riesgos - 2026-05-11 13-30 CEST - Notas de Gemini.pdf
---

# Rules for beneficial owner codes

## Intent
To define the rules and constraints for assigning codes to beneficial owners in the context of lender and vendor relationships.

## Definition
### Concept
Beneficial owner codes are identifiers used to distinguish entities in lending and vendor transactions.

### Rules
1. Beneficial owner codes must be unique per entity.
2. Codes may vary depending on the lender or vendor.
3. If codes are not unique, alternative solutions must be proposed.

### Constraints
- Regulatory compliance for beneficial owner identification.
- Consistency with existing contracts and systems.

### Examples
- Scenario 1: Beneficial owner A has code X under lender Y and code Z under vendor W.
- Scenario 2: Beneficial owner B has the same code under multiple lenders.

## Acceptance Criteria
- [ ] Confirmation of whether beneficial owner codes vary by lender/vendor.
- [ ] Validation of rules against real-world examples.
- [ ] Alignment with regulatory requirements.

## Evidence
- Meeting notes from May 11, 2026.
- Pending confirmation from Isa regarding code uniqueness.

## Traceability
- Related ADR: ADR-002.
- Related contracts: Mentor and Golinx framework agreements.
