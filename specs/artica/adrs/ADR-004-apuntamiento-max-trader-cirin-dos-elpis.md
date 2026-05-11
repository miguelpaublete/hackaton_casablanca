---
id: ADR-004
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: TBD
project: artica
tags: [integration, elpis, max-trader, cirin]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-06 09-59 CEST - Notas de Gemini.pdf
---

# Apuntamiento de Max Trader y Cirin a dos Elpis diferentes

## Intent
Para completar las pruebas restantes de liquidación en el SIT, se requiere configurar Max Trader y Cirin para apuntar a dos Elpis diferentes.

## Context
Durante las pruebas SIT, se identificó que la validación de casos de liquidación requería que los sistemas Max Trader y Cirin estuvieran configurados para apuntar a dos Elpis distintos. Esto permitirá validar casos específicos de liquidación y conciliación.

## Decision
Se decidió configurar Max Trader y Cirin para apuntar a dos Elpis diferentes, sugiriendo Bitstamp y Kraken como ejemplos.

## Rationale
La configuración de dos Elpis distintos es necesaria para validar los casos de liquidación pendientes y garantizar la cobertura completa de las pruebas. Bitstamp y Kraken fueron sugeridos por su capacidad de proporcionar la liquidez necesaria para las pruebas.

## Consequences
- **Positivas**: Permite finalizar las pruebas SIT y validar los casos pendientes de liquidación.
- **Negativas**: Requiere ajustes técnicos en los sistemas Max Trader y Cirin, lo que podría generar retrasos si surgen problemas.
- **Neutrales**: No se espera impacto en otros sistemas fuera de los mencionados.

## Alternatives Considered
- **Mantener la configuración actual**: No viable, ya que no permite validar los casos pendientes.
- **Apuntar a otros Elpis**: Bitstamp y Kraken fueron seleccionados por su capacidad de proporcionar liquidez adecuada.

## Traceability
- Relacionado con el problema de precisión decimal TAC 118.
- Relacionado con los casos pendientes de liquidación discutidos en la reunión.
