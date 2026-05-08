---
id: ADR-002
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-05-04
updated: 2026-05-04
owner: equipo-integracion-artica
project: artica
tags: [entorno, Bitstamp, archivos, pruebas]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-04 09-45 CEST - Notas de Gemini.pdf
---

# Cambio de entorno de pruebas a Bitstamp para generación de archivos diarios

## Context
Se requiere completar todos los casos de prueba en un solo día para emular la generación del fichero diario de producción, actualmente el entorno apunta a Kraken.

## Decision
Se acordó consolidar los casos regresivos mediante el cambio de entorno a Bitstamp, con el objetivo de emular la generación del fichero diario de producción.

## Rationale
Bitstamp permite una mejor emulación del entorno de producción y facilita la generación de archivos diarios necesarios para las pruebas.

## Consequences
- Positivo: Facilita la generación de archivos diarios y la ejecución de pruebas regresivas.
- Negativo: Requiere coordinación y confirmación de liquidez y configuración en Bitstamp.
- Neutral: El entorno de ejecución se mantiene estable para pruebas.

## Alternatives Considered
- Mantener el entorno en Kraken (pro: continuidad, contra: no permite emular la generación de archivos diarios de producción).
- Cambiar a otro entorno distinto de Bitstamp (pro: posible flexibilidad, contra: no discutido ni evaluado).

## Open Questions
_(Not discussed in this meeting)_