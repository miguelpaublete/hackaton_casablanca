---
id: ADR-001
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-03-09
updated: 2026-03-09
owner: tbd
project: sec-lending
tags: [OASms, Murex, Smart Data, migration]
source_transcript: Deco Algo. Weekly Solución de seguimiento de Riesgos de Mercado y análisis de requerimientos integraciones - 2026_03_09 16_49 CET - Notas de Gemini.pdf
---

# Ejecución ad hoc para desbloquear migración de OASms

## Intent
Desbloquear la migración de OASms de Mentor a Smart Data, que actualmente está paralizada debido a la falta de información proveniente de Murex.

## Context
La migración de OASms está bloqueada porque la información de Murex no está llegando a Smart Data debido a problemas en el circuito de Murex. Esto impide la migración de reportes, algunos de los cuales ya se generan desde GSR.

## Decision
Se decidió realizar una ejecución ad hoc el próximo fin de semana para verificar si la información de Murex está disponible y, en caso contrario, determinar si se necesita algo nuevo.

## Rationale
La ejecución ad hoc permitirá identificar si los datos necesarios están disponibles o si es necesario tomar medidas adicionales para solucionar el bloqueo. Esto asegura que la migración de OASms pueda continuar sin retrasos adicionales.

## Consequences
- **Positivo**: Posibilidad de desbloquear la migración de OASms y avanzar en el proyecto.
- **Negativo**: Requiere coordinación adicional con el equipo de reporting y recursos para la ejecución ad hoc.
- **Neutral**: No se identificaron consecuencias adicionales.

## Alternatives Considered
- **Esperar a que Murex reactive el circuito**: Rechazado debido a la incertidumbre sobre el tiempo necesario y el impacto en el cronograma del proyecto.
- **Buscar una solución alternativa sin Murex**: Rechazado debido a la dependencia crítica de los datos de Murex para la migración.

## Traceability
- Relacionado con el inventario de reportes actuales de medias algorítmicas y la migración de OASms a Smart Data.
