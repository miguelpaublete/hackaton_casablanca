---
id: ADR-006
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-03-09
updated: 2026-03-09
owner: equipo-reporting
project: Deco Algo
tags: [murex, smart-data, migracion, oasms]
source_transcript: Deco Algo. Weekly Solución de seguimiento de Riesgos de Mercado y análisis de requerimientos integraciones - 2026_03_09 16_49 CET - Notas de Gemini.pdf
---

# Ejecución ad hoc para verificación de datos de Murex en Smart Data

## Context
La migración de reportes OASms de Mentor a Smart Data está bloqueada por la falta de información proveniente de Murex, ya que el circuito de Murex está paralizado y no se reciben datos en Smart Data.

## Decision
Se acordó solicitar y ejecutar una operación ad hoc el próximo fin de semana para verificar si la información de Murex está disponible en Smart Data o si se requiere alguna acción adicional.

## Rationale
La ejecución ad hoc permitirá determinar el estado real de la información y evitar migrar reportes vacíos, asegurando que solo se migren aquellos que están en uso y con datos válidos.

## Consequences
Positivas: Se clarificará el estado de los datos y se podrá avanzar en la migración. Negativas: Si la información sigue sin estar disponible, el bloqueo persistirá. Neutras: _(Not discussed in this meeting)_

## Alternatives Considered
- Esperar a que el circuito de Murex se reactive (pro: menos esfuerzo; con: indefinido el plazo).
- Migrar todos los reportes sin verificación (pro: rapidez; con: riesgo de migrar reportes vacíos).
- Solicitar ejecución ad hoc (pro: validación precisa; con: requiere coordinación y recursos).

## Open Questions
_(Not discussed in this meeting)_