---
id: DOM-RISK-007
type: spec
layer: domain
domain: risk
subdomain: trading
status: draft
confidence: low
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: tbd
project: artica
tags: [risk, validation, kraken]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-11 09-44 CEST - Notas de Gemini.pdf
---

# Validación de riesgos y conciliación con Kraken

## Intent
Definir los requisitos y procesos necesarios para la validación de riesgos y la conciliación con Kraken.

## Definition
### Concept
La validación de riesgos y la conciliación con Kraken son procesos críticos para garantizar la integridad de las operaciones de trading.

### Rules
1. La conciliación requiere la modificación del TAC 118 en Max Trader.
2. La validación de riesgos debe cubrir todos los casos de prueba relacionados con el patch y accesión a riesgos.

### Constraints
- La modificación del TAC 118 debe ser entregada por el equipo de Max Trader.
- Las pruebas de riesgos requieren un ciclo de verificación de dos semanas.

### Examples
- Caso de prueba: Validación de conciliación con Kraken utilizando el TAC 118.
- Caso de prueba: Verificación de riesgos en operaciones de trading con Kraken.

## Acceptance Criteria
- [ ] Modificación del TAC 118 entregada por Max Trader.
- [ ] Validación completa de riesgos en un plazo de dos semanas.
- [ ] Ejecución exitosa de casos de prueba de conciliación.

## Evidence
- Reunión del 11 de mayo de 2026.
- Documentación técnica de Max Trader.

## Traceability
- Relacionado con los incidentes técnicos y ajustes discutidos en la reunión.
