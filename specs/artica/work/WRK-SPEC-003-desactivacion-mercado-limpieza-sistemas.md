---
id: WRK-SPEC-003
type: spec
layer: work-spec
scope: ephemeral
status: draft
confidence: medium
version: 1.0.0
created: 2026-03-05
updated: 2026-03-05
owner: tbd
project: artica
activates: [ADR-002, DOM-LIC-002]
tags: [mercado, ASE, sistemas obsoletos]
source_transcript: Deco Algo. ASE para generación del dump - 2026_03_05 17_30 CET - Notas de Gemini.pdf
---

# Desactivación de la instancia de Mercado y limpieza de sistemas obsoletos

## Problem Statement
La instancia de Mercado (versión 453) es obsoleta y su mantenimiento genera costos innecesarios. Además, existen sistemas satélite como Trida y Safari que también requieren limpieza.

## Proposed Change
Desactivar la instancia de Mercado, priorizando la confirmación de la licencia independiente de ASE y su capacidad para generar el dump de datos históricos. Separar la limpieza de sistemas obsoletos como Trida y Safari para fases posteriores.

## Knowledge Context
- ADR-002: Desactivación de la instancia obsoleta de Mercado y su impacto en ASE.
- DOM-LIC-002: Reglas de licenciamiento para sistemas Algoritmics y ASE.

## Constraints
- La desactivación de Mercado depende de la confirmación de la licencia de ASE.
- ASE utiliza datos de mercado diarios de la base de datos IDB de Algoritmics Mercado.

## Acceptance Criteria
- [ ] Confirmar la licencia independiente de ASE.
- [ ] Validar que ASE puede generar el dump sin Mercado.
- [ ] Planificar la limpieza de sistemas obsoletos para fases posteriores.

## Open Questions
- ¿Qué otras dependencias técnicas podrían surgir al desactivar Mercado?
- ¿Qué impacto tendrá la desactivación de Mercado en los sistemas satélite?
