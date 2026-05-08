---
id: DOM-PRUEB-001
type: spec
layer: domain
domain: pruebas
subdomain: ordenes
status: draft
confidence: low
version: 1.0.0
created: 2026-05-04
updated: 2026-05-04
owner: equipo-integracion-artica
project: artica
tags: [cantidades, pruebas, órdenes]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-04 09-45 CEST - Notas de Gemini.pdf
---

# Estandarización de cantidades exactas en pruebas de órdenes

## Intent
Este documento existe para definir la regla de estandarizar las cantidades exactas en las pruebas de órdenes, evitando términos ambiguos.

## Definition
### Concept
Las pruebas de órdenes deben especificar cantidades exactas (ejemplo: 5, 10, 15) en lugar de términos ambiguos como "menos operativa".

### Rules
- Todas las pruebas deben incluir cantidades exactas.
- No se permiten términos ambiguos en la definición de casos de prueba.

### Constraints
- Las cantidades deben ser acordadas y documentadas por los equipos involucrados.

### Examples
- Prueba de compra de 10 BTC.
- Prueba de venta de 5 ETH.

## Acceptance Criteria
- [ ] Todas las pruebas de órdenes documentadas incluyen cantidades exactas.
- [ ] No existen términos ambiguos en los casos de prueba.
- [ ] Los equipos han revisado y acordado las cantidades.

## Evidence
- Reunión del 4 de mayo de 2026 donde se acordó estandarizar cantidades exactas.
- Documento de casos de prueba actualizado.

## Open Questions
_(Not discussed in this meeting)_