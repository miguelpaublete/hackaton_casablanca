# Resumen de la reunion

En la reunión sobre cumplimiento normativo MiFID II y reportes de transacciones, se discutieron los resultados de pruebas, identificando fallos relacionados con el campo 'execution venue'. Se acordó implementar una validación previa al envío para rechazar transacciones con venues desconocidos y se asignó a Diego la tarea de coordinar una sincronización diaria con el equipo de Reference Data. Se destacó el riesgo de reportes erróneos si la tabla de venues no está actualizada.

## Artefactos generados

- `ADR-001` - Validación previa de execution venue
- `WRK-TASK-001` - Sincronización diaria de tabla de venues
- `DOM-MIFID-001` - Regla de venue conocido para reportes MiFID II