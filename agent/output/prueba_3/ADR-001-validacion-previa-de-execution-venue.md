---
id: ADR-001
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: 2026-03-22
updated: 2026-03-22
owner: equipo-dev
project: prueba_3
tags: [MiFIDII, execution-venue]
source_transcript: 2026-03-22_pruebas.txt
---

# Validación previa de execution venue

## Contexto
El campo 'execution venue' está generando fallos en los reportes de transacciones debido a valores desconocidos. La tabla de venues es mantenida por el equipo de Reference Data.

## Decisión
Se implementará una validación previa al envío de reportes que rechace transacciones con execution venue desconocido.

## Razonamiento
La validación evitará que se envíen reportes erróneos a la CNMV y reducirá el riesgo de incumplimiento normativo. Otras opciones no garantizan la calidad de los datos.

## Consecuencias
Positivas: Se mejora la calidad de los reportes y se reduce el riesgo de sanciones. Negativas: Puede aumentar el número de transacciones rechazadas si la tabla de venues no está actualizada.

## Alternativas Consideradas
- Permitir el envío de transacciones con venue desconocido (pro: menos rechazos; contra: riesgo regulatorio).
- Validación posterior al envío (pro: menor impacto en el flujo; contra: reportes erróneos).

## Open Questions
(No se discutieron preguntas abiertas en esta reunión.)