---
id: DOM-TRAD-006
type: spec
layer: domain
domain: trading
subdomain: execution
status: draft
confidence: low
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: tbd
project: artica
tags: [execution, trading, rules]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-04 09-45 CEST - Notas de Gemini.pdf
---

# Reglas de ejecución total y parcial en trading

## Intent
Definir las reglas y criterios para considerar equivalentes las ejecuciones totales y parciales en escenarios operativos de trading.

## Definition
### Concept
Las ejecuciones totales y parciales representan escenarios operativos equivalentes en trading cuando implican múltiples ejecuciones.

### Rules
1. Las ejecuciones parciales son el caso más común en entornos previos debido a limitaciones del libro de órdenes y disponibilidad de contrapartes.
2. Las ejecuciones totales con múltiples operaciones no garantizan el escenario deseado y pueden ser descartadas.
3. Desde la perspectiva de trading, las ejecuciones totales y parciales se consideran equivalentes si implican múltiples ejecuciones.

### Constraints
1. Las ejecuciones totales con múltiples operaciones son técnicamente complejas y no deben ser forzadas.
2. Las pruebas deben emular escenarios operativos reales y evitar configuraciones artificiales.

### Examples
- Ejemplo de ejecución parcial: Una orden de compra de Bitcoin se ejecuta en tres partes debido a la disponibilidad limitada de contrapartes.
- Ejemplo de ejecución total: Una orden de venta de Bitcoin se ejecuta completamente en una sola operación.

## Acceptance Criteria
- [ ] Las pruebas deben considerar las ejecuciones parciales como equivalentes a las ejecuciones totales.
- [ ] Las configuraciones de prueba deben evitar forzar escenarios artificiales.

## Evidence
- Revisión de casos C204 en la reunión del 4 de mayo de 2026.
- Alineación de criterios técnicos discutida entre los participantes.

## Traceability
- Relacionado con ADR-006: Descartar ejecuciones totales con múltiples operaciones por complejidad técnica.
