---
id: DOM-RISK-001
type: spec
layer: domain
domain: risk
subdomain: data-migration
status: draft
confidence: low
version: 1.0.0
created: 2026-03-09
updated: 2026-03-09
owner: tbd
project: sec-lending
tags: [OASms, Smart Data, migration, Mentor]
source_transcript: Deco Algo. Weekly Solución de seguimiento de Riesgos de Mercado y análisis de requerimientos integraciones - 2026_03_09 16_49 CET - Notas de Gemini.pdf
---

# Confirmación de OASms en Mentor para migración a Smart Data

## Intent
Definir las reglas y criterios para la confirmación de OASms en Mentor antes de proceder con su migración a Smart Data.

## Definition

### Concept
La migración de OASms de Mentor a Smart Data requiere la confirmación de los reportes que están en uso actualmente para evitar la migración de reportes vacíos.

### Rules
1. Solo se migrarán los OASms que estén en uso actualmente.
2. Los OASms que ya se generen desde GSR no serán migrados.
3. Se debe revisar el inventario de reportes actuales de medias algorítmicas para identificar los OASms pendientes.

### Constraints
- La migración depende de la disponibilidad de información de Murex.
- Los OASms deben ser confirmados por Santiago de GR antes de proceder.

### Examples
- OASms confirmados: Reporte 12, 14, 22, 24 y 54.
- OASms no confirmados: Reportes sin datos en el Excel adjunto.

## Acceptance Criteria
- [ ] Confirmación de los OASms en uso por Santiago de GR.
- [ ] Verificación de que los OASms ya generados desde GSR no sean migrados.
- [ ] Inventario de reportes actualizado con los OASms confirmados.

## Evidence
- Excel adjunto con los 50 y pico de OASms a migrar.
- Discusión en la reunión semanal de seguimiento de riesgos de mercado.

## Traceability
- Relacionado con ADR-001: Ejecución ad hoc para desbloquear migración de OASms.
