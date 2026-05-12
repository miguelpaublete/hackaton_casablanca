---
id: ADR-008
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-05-12
updated: 2026-05-12
owner: TBD
project: artica
tags: [kraken, integration, execution]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-12 09-45 CEST - Notas de Gemini.pdf
---

# Priorización del enfoque 1N sobre 1:1 en la integración de Kraken

## Intent
Optimizar la ejecución entre Kraken y Bitestam mediante un enfoque activo-activo (1N), minimizando modificaciones futuras en términos y condiciones del cliente.

## Context
El enfoque inicial de integración de Kraken planteaba un modelo 1:1 donde Bitestam sería el proveedor principal y Kraken operaría como respaldo. Sin embargo, la normativa de mejor ejecución y la necesidad de modificar términos y condiciones del cliente motivaron la revisión del enfoque.

## Decision
Se decidió avanzar directamente al enfoque 1N, donde Max Trader balanceará la ejecución entre Kraken y Bitestam de forma indistinta, eliminando la necesidad de implementar el modelo 1:1 en producción.

## Rationale
El enfoque 1N reduce la complejidad normativa al realizar una única modificación de términos y condiciones del cliente. Además, permite una integración más eficiente y flexible entre los proveedores.

## Consequences
- **Positivas**: Menor carga normativa, mayor flexibilidad en la ejecución, reducción de riesgos operativos.
- **Negativas**: Mayor complejidad técnica inicial para implementar el enfoque 1N.
- **Neutrales**: Sin impacto en los plazos generales de producción.

## Alternatives Considered
- **Enfoque 1:1**: Simplicidad inicial, pero requeriría modificaciones adicionales en el futuro.
  - **Pros**: Menor complejidad técnica inicial.
  - **Contras**: Mayor carga normativa y operativa a largo plazo.

## Traceability
- Relacionado con normativa de mejor ejecución (CNMV).
- Dependencias técnicas de Max Trader.
