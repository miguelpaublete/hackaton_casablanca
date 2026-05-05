---
id: DOM-RISK-001
type: spec
layer: domain
domain: Riesgos de Mercado
subdomain: Gestión de Tesorería
status: draft
confidence: low
version: 1.0.0
created: 2026-03-23
updated: 2026-03-23
owner: Noni Calvo Fernandez
project: Deco Algo
tags: [Mentor, Bar, carga manual]
source_transcript: Deco Algo. Weekly Solución de seguimiento de Riesgos de Mercado y análisis de requerimientos integraciones - 2026_03_23 16_58 CET - Notas de Gemini.pdf
---

# Regla de carga manual preliminar del Bar en Mentor

## Intent
Esta especificación define la regla de carga manual preliminar del Bar en Mentor para la gestión diaria de tesorería.

## Definition
### Concept
La cifra diaria preliminar del Bar se carga manualmente en Mentor mediante un archivo CSV, antes de la difusión automática de la cifra oficial desde Reda.

### Rules
- La carga manual se realiza cada día antes de la 1 p.m.
- La cifra oficial se difunde automáticamente posteriormente desde Reda a Mentor.

### Constraints
- La cifra preliminar puede no coincidir con la cifra oficial.
- El proceso automático solo aplica a geografías de Europa.

### Examples
- Ejemplo: El equipo de tesorería carga el archivo CSV con la cifra preliminar del Bar en Mentor a las 12:30 p.m.

## Acceptance Criteria
- [ ] La cifra preliminar del Bar se carga manualmente en Mentor antes de la 1 p.m.
- [ ] La cifra oficial se difunde automáticamente desde Reda a Mentor.
- [ ] El proceso manual está documentado y auditado.

## Evidence
- Reunión del 23 de marzo de 2026.
- Confirmación por Noni Calvo Fernandez y Eduardo Lopez de Dicastillo Perez.
- Proceso descrito por Javier Garcia Retuerta.
