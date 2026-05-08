---
id: ADR-001
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-05-04
updated: 2026-05-04
owner: equipo-integracion-artica
project: artica
tags: [pruebas, C204, ejecución, criterios]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-04 09-45 CEST - Notas de Gemini.pdf
---

# Unificación de criterios de ejecución total y parcial en pruebas C204

## Context
Se revisaron los casos de prueba C204 en el contexto de la integración Kraken, observando que la mayoría de las ventas se ejecutan completamente y las compras suelen ser parciales debido a limitaciones del libro de órdenes y disponibilidad de contrapartes.

## Decision
Se acordó considerar las ejecuciones totales y parciales como el mismo escenario operativo en las pruebas C204, descartando las ejecuciones totales con múltiples operaciones por su complejidad técnica.

## Rationale
La ejecución parcial es el caso más común y replicar escenarios de compras con ejecución total es difícil. Forzar órdenes con importes altos no garantiza el escenario deseado y ambas ejecuciones implican múltiples ejecuciones desde la perspectiva de trading.

## Consequences
- Positivo: Simplificación de los casos de prueba y reducción de complejidad técnica.
- Negativo: No se cubrirán escenarios de ejecución total con múltiples operaciones.
- Neutral: Se mantiene la validez operativa de las pruebas.

## Alternatives Considered
- Mantener casos de ejecución total con múltiples operaciones (pro: mayor cobertura, contra: complejidad técnica y dificultad de replicación).
- Considerar ejecuciones parciales y totales como escenarios separados (pro: mayor especificidad, contra: redundancia y dificultad técnica).

## Open Questions
_(Not discussed in this meeting)_