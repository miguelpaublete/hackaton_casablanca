---
id: ADR-006
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: tbd
project: artica
tags: [execution, trading, complexity]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-04 09-45 CEST - Notas de Gemini.pdf
---

# Descartar ejecuciones totales con múltiples operaciones por complejidad técnica

## Intent
Descartar el uso de ejecuciones totales con múltiples operaciones debido a su complejidad técnica y considerar las ejecuciones parciales como equivalentes en el escenario operativo.

## Context
Durante la revisión de los casos C204, se identificó que las ejecuciones totales con múltiples operaciones presentan una complejidad técnica que dificulta su implementación en los entornos de prueba. Además, se concluyó que las ejecuciones totales y parciales representan el mismo escenario operativo desde la perspectiva de trading.

## Decision
Se decidió descartar las ejecuciones totales con múltiples operaciones en los casos de prueba y considerar las ejecuciones parciales como equivalentes para simplificar el proceso.

## Rationale
La complejidad técnica de las ejecuciones totales con múltiples operaciones no garantiza el escenario deseado y puede generar problemas operativos innecesarios. Las ejecuciones parciales son más comunes y representan adecuadamente el escenario operativo.

## Consequences
- **Positivas**: Simplificación del proceso de pruebas, reducción de problemas técnicos y mayor alineación con los escenarios operativos reales.
- **Negativas**: No se cubrirán escenarios de ejecuciones totales con múltiples operaciones.
- **Neutrales**: No se espera impacto significativo en los resultados de las pruebas.

## Alternatives Considered
- **Mantener ejecuciones totales con múltiples operaciones**: Rechazado por su complejidad técnica y falta de garantía de resultados deseados.
- **Considerar ejecuciones parciales como equivalentes**: Aceptado por su simplicidad y representatividad del escenario operativo.

## Traceability
- Relacionado con la revisión de casos C204 y coordinación de pruebas en entornos distintos.
