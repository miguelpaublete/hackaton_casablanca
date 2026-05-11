---
id: DOM-LIC-002
type: spec
layer: domain
domain: licensing
subdomain: software
status: draft
confidence: low
version: 1.0.0
created: 2026-03-05
updated: 2026-03-05
owner: tbd
project: artica
tags: [licencias, ASE, Mercado, Algoritmics]
source_transcript: Deco Algo. ASE para generación del dump - 2026_03_05 17_30 CET - Notas de Gemini.pdf
---

# Reglas de licenciamiento para sistemas Algoritmics y ASE

## Intent
Documentar las reglas y dependencias de licenciamiento entre los sistemas Algoritmics Mercado y ASE.

## Definition
### Concept
El licenciamiento de los sistemas Algoritmics Mercado y ASE determina las condiciones bajo las cuales pueden ser desactivados o mantenidos de manera independiente.

### Rules
1. La instancia de Mercado (versión 453) y ASE podrían compartir una licencia global de Algoritmics Mercado.
2. ASE podría requerir una licencia independiente para operar sin Mercado.

### Constraints
- La confirmación de las licencias debe ser obtenida de Algoritmics o Compras del BBVA.
- ASE utiliza datos de mercado diarios de la base de datos IDB de Algoritmics Mercado.

### Examples
- Si ASE tiene una licencia independiente, Mercado puede ser desactivado sin afectar la generación del dump.
- Si ASE depende de la licencia global de Mercado, su desactivación podría interrumpir procesos críticos.

## Acceptance Criteria
- [ ] Confirmar si ASE tiene una licencia independiente.
- [ ] Validar que ASE puede generar el dump sin Mercado.

## Evidence
- Reunión del 5 de marzo de 2026.
- Notas internas de Algoritmics.

## Traceability
- Relacionado con ADR-002.
