---
id: WRK-SPEC-006
type: spec
layer: work-spec
scope: ephemeral
status: draft
confidence: medium
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: TBD
project: artica
activates: []
tags: [max-trader, pruebas, kraken, sit]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-05 11-30 CEST - Notas de Gemini.pdf
---

# Revisión técnica de incidencias en Max Trader y coordinación de pruebas

## Problem Statement
La imposibilidad de ejecutar compras en Max Trader bloquea pruebas críticas y afecta la generación de sets de pruebas necesarios para integraciones externas.

## Proposed Change
Resolver las incidencias en Max Trader relacionadas con la expiración de órdenes de compra y ajustar los decimales para permitir la ejecución de pruebas críticas y avanzar con las integraciones externas.

## Knowledge Context
- _(Not discussed in this meeting)_

## Constraints
- La volatilidad del mercado dificulta la realización de pruebas.
- La intervención programada en el backoffice de Ártica limita la operativa entre las 3 y las 4 PM en los entornos previos de la base de datos.

## Acceptance Criteria
- [ ] Las órdenes de compra en Max Trader no deben expirar ni cancelarse.
- [ ] Confirmación de la estabilidad ambiental para pruebas de liquidación.
- [ ] Ajuste de decimales aplicado correctamente en Max Trader.
- [ ] Generación exitosa de sets de pruebas para integraciones externas.

## Open Questions
- ¿Cuál es la causa raíz de la expiración de órdenes de compra en Max Trader?
- ¿Cuándo se podrá confirmar la aplicación del ajuste de decimales por parte de Alejandro de Max Trader?
- ¿Qué impacto tendrá la intervención en el backoffice de Ártica en las pruebas programadas?
