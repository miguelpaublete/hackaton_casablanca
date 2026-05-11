---
id: ADR-007
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-05-11
updated: 2026-05-11
owner: tbd
project: artica
tags: [testing, repository, integration]
source_transcript: Copia de [Artica] Integración Kraken - Follow up - SIT  - 2026-05-11 09-44 CEST - Notas de Gemini.pdf
---

# Integración de casos de prueba en un repositorio común

## Intent
Optimizar la planificación de pruebas de aceptación del usuario mediante la centralización de todos los casos de prueba en un único repositorio común.

## Context
Actualmente, los casos de prueba de trading, regresivas y órdenes limitadas están dispersos en diferentes ubicaciones, lo que dificulta la planificación y ejecución eficiente de las pruebas.

## Decision
Se decidió integrar todos los casos de prueba de trading, regresivas y órdenes limitadas en un repositorio común.

## Rationale
La centralización de los casos de prueba permitirá una mejor organización, facilitará el acceso a la información y optimizará el tiempo necesario para la planificación y ejecución de las pruebas.

## Consequences
- **Positivas**: Mayor eficiencia en la planificación y ejecución de pruebas, reducción de duplicidades, y mejora en la colaboración entre equipos.
- **Negativas**: Requiere tiempo inicial para consolidar y migrar los casos de prueba existentes al repositorio común.
- **Neutrales**: No se prevén impactos en el rendimiento del sistema.

## Alternatives Considered
- **Mantener los casos de prueba dispersos**: No optimiza la planificación ni la ejecución.
- **Utilizar múltiples repositorios organizados por tipo de prueba**: Facilita la organización pero no resuelve completamente los problemas de acceso y duplicidad.

## Traceability
- Relacionado con los casos de prueba discutidos en la reunión del 11 de mayo de 2026.
