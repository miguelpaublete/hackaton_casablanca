---
id: DOM-RISK-004
type: spec
layer: domain
domain: risk
subdomain: reconciliation
status: draft
confidence: low
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: TBD
project: artica
tags: [precision, decimals, reconciliation]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-06 09-59 CEST - Notas de Gemini.pdf
---

# Reglas de conciliación y precisión decimal en órdenes con términos

## Intent
Definir las reglas y restricciones relacionadas con la precisión decimal en órdenes con términos para garantizar la correcta conciliación en los sistemas.

## Definition
### Concept
La precisión decimal en órdenes con términos es crítica para la validación de casos de conciliación y liquidación en sistemas financieros.

### Rules
1. Las órdenes directas deben cumplir con una precisión decimal de al menos 6 dígitos.
2. Las órdenes con términos deben implementar correcciones técnicas en Max Trader para garantizar la misma precisión.

### Constraints
- La precisión decimal debe cumplir con los estándares regulatorios aplicables.
- Las correcciones técnicas deben ser implementadas antes de la validación completa de los casos de conciliación.

### Examples
- Una orden directa con precisión decimal de 6 dígitos se valida correctamente.
- Una orden con términos que no cumple con la precisión requerida genera errores en la conciliación.

## Acceptance Criteria
- [ ] Validación exitosa de órdenes directas con precisión decimal adecuada.
- [ ] Implementación de correcciones técnicas en Max Trader para órdenes con términos.
- [ ] Validación completa de casos de conciliación y liquidación.

## Evidence
- Discusión en la reunión del 6 de mayo de 2026 sobre el problema de precisión decimal TAC 118.
- Reportes de pruebas SIT que identificaron errores en órdenes con términos.

## Traceability
- Relacionado con el problema TAC 118.
- Relacionado con el ADR-004 sobre apuntamiento de dos Elpis.
