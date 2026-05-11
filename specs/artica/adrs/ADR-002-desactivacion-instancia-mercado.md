---
id: ADR-002
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-03-05
updated: 2026-03-05
owner: tbd
project: artica
tags: [mercado, ASE, licencias]
source_transcript: Deco Algo. ASE para generación del dump - 2026_03_05 17_30 CET - Notas de Gemini.pdf
---

# Desactivación de la instancia obsoleta de Mercado y su impacto en ASE

## Intent
Evaluar la viabilidad de desactivar la instancia obsoleta de Mercado (versión 453) y garantizar que el sistema ASE pueda seguir generando el dump de datos históricos necesario para otros procesos.

## Context
La instancia de Mercado (versión 453) se considera obsoleta y su desactivación podría generar ahorros en licencias. Sin embargo, ASE depende de esta instancia para generar el dump de datos históricos, que es utilizado como input para otros procesos críticos como el generador de escenarios de contrapartida (Yase).

## Decision
Se decidió priorizar la desactivación de la instancia de Mercado como el camino crítico del proyecto, siempre y cuando se confirme que ASE tiene una licencia independiente y que puede seguir generando el dump de datos históricos sin Mercado.

## Rationale
La desactivación de Mercado permitirá ahorrar costos de licencias y simplificar la infraestructura. La confirmación de la independencia de la licencia de ASE es crucial para garantizar que los procesos dependientes del dump de datos históricos no se vean afectados.

## Consequences
- **Positivas**: Reducción de costos de licencias y simplificación de la infraestructura.
- **Negativas**: Riesgo de interrupción en procesos dependientes del dump de datos históricos si ASE no tiene una licencia independiente.
- **Neutrales**: Las tareas de limpieza técnica de sistemas obsoletos como Trida o Safari se pospondrán para fases posteriores.

## Alternatives Considered
- **Mantener la instancia de Mercado activa**: No se lograría el ahorro en licencias, pero se evitarían riesgos relacionados con la generación del dump.
- **Desactivar Mercado sin confirmar la licencia de ASE**: Alto riesgo de interrupción en procesos críticos.

## Traceability
- Relacionado con la instancia de Mercado (versión 453).
- Dependencias técnicas identificadas con la base de datos IDB de Algoritmics Mercado.
