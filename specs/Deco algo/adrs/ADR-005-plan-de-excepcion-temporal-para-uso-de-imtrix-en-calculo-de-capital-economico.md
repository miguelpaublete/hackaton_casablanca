---
id: ADR-005
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-03-23
updated: 2026-03-23
owner: Juan Luis Garcia Garcia
project: Deco Algo
tags: [IMTRIX, excepción, capital económico]
source_transcript: Deco Algo. Weekly Solución de seguimiento de Riesgos de Mercado y análisis de requerimientos integraciones - 2026_03_23 16_58 CET - Notas de Gemini.pdf
---

# Plan de excepción temporal para uso de IMTRIX en cálculo de capital económico

## Context
El nivel de riesgo de IMTRIX ha aumentado, y su uso para el cálculo de capital económico requiere una excepción regulatoria. El comité RCA exige un plan de resolución para aceptar el riesgo o buscar una excepción temporal mientras se exploran alternativas como Murex.

## Decision
Se acordó presentar un plan de excepción temporal al comité Ciro para permitir el uso de IMTRIX en el cálculo de capital económico hasta que se implemente una solución corporativa estratégica o se ajuste el planteamiento para usar Murex como fuente de agregaciones.

## Rationale
La excepción es necesaria debido a que IMTRIX es un desarrollo nuevo y su uso para el cálculo de capital económico es considerado crítico por RCA. La alternativa de usar Murex está en evaluación, pero se requiere una solución inmediata para la gestión diaria.

## Consequences
- Positivo: Permite continuar con el cálculo de capital económico sin interrupciones.
- Negativo: Riesgo regulatorio temporal y necesidad de seguimiento por parte del comité.
- Neutral: El uso de IMTRIX no afecta otros procesos ya establecidos.

## Alternatives Considered
- Excepción temporal para IMTRIX (pro): Solución rápida, pero implica riesgo regulatorio.
- Migrar a Murex como fuente (pro): Solución estratégica, pero requiere desarrollo y validación.
- No usar IMTRIX (con): Puede afectar la agilidad y flexibilidad en la gestión diaria.

## Open Questions
- ¿Cómo se presentará el plan de excepción al comité Ciro?
- ¿Qué criterios debe cumplir IMTRIX para ser aceptado temporalmente?
- ¿Cuándo estará disponible la solución corporativa definitiva?
