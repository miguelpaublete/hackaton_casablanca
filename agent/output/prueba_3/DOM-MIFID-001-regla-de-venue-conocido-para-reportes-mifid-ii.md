---
id: DOM-MIFID-001
type: spec
layer: domain
domain: MiFIDII
subdomain: reportes-transacciones
status: draft
confidence: low
version: 1.0.0
created: 2026-03-22
updated: 2026-03-22
owner: equipo-compliance
project: prueba_3
tags: [MiFIDII, venue]
source_transcript: 2026-03-22_pruebas.txt
---

# Regla de venue conocido para reportes MiFID II

## Intento
Esta especificación existe para asegurar que solo se reporten transacciones con execution venue reconocido, cumpliendo con la normativa MiFID II.

## Definición
### Concepto
'Execution venue' es el lugar donde se ejecuta una transacción financiera y debe ser reconocido por la CNMV.

### Reglas
- Solo se reportan transacciones cuyo execution venue esté presente en la tabla oficial mantenida por Reference Data.

### Restricciones
- No se permite reportar transacciones con venue desconocido.

### Ejemplos
- Transacción con venue 'XMAD' (válido).
- Transacción con venue 'ZZZZ' (rechazado).

## Acceptance Criteria
- [ ] Todas las transacciones reportadas tienen execution venue reconocido.
- [ ] Se rechazan transacciones con venue no listado.

## Evidence
- Resultados de pruebas QA.
- Normativa MiFID II.
- Tabla de venues de Reference Data.

## Open Questions
(No se discutieron preguntas abiertas en esta reunión.)