"""
test_local.py — Prueba local del pipeline sin necesidad de GCP.

Simula la respuesta de Vertex AI con artefactos realistas extraídos
del acta de ejemplo, y lanza Streamlit para validación.

Uso:
    python test_local.py
"""

import json
from pathlib import Path
from datetime import date

# Añadir el directorio actual al path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from extractor import ExtractionResult, Artifact, save_artifacts

TODAY = date.today().isoformat()

# ─────────────────────────────────────────────────────────────
# ARTEFACTOS SIMULADOS (como si Gemini los hubiera generado)
# ─────────────────────────────────────────────────────────────

MOCK_ARTIFACTS = [
    Artifact(
        id="ADR-001",
        type="adr",
        title="Kafka como broker para mensajería SWIFT",
        filename="ADR-001-kafka-swift-messaging.md",
        content=f"""---
id: ADR-001
type: adr
layer: architecture
status: proposed
confidence: medium
version: 1.0.0
created: {TODAY}
updated: {TODAY}
owner: maria-arquitecta
source_transcript: sample_transcript.txt
tags:
  - swift
  - kafka
  - messaging
  - payments
---

# ADR-001 — Kafka como broker para mensajería SWIFT

## Context

La nueva plataforma de Pagos Internacionales necesita enviar mensajes SWIFT (MT103) al gateway.
Se evaluaron dos opciones: conexión directa al gateway o uso de un broker de mensajería intermedio.

Con conexión directa hay menor latencia, pero si el gateway se cae se pierden mensajes.

## Decision

Usar **Apache Kafka** como broker intermedio entre la plataforma y el gateway SWIFT.

## Rationale

- **Persistencia garantizada**: los mensajes no se pierden si el gateway está caído
- **Replay**: posibilidad de reenviar mensajes en caso de error
- **Desacoplamiento**: el módulo de compliance queda desacoplado del de ejecución
- **Escalabilidad**: Kafka soporta alto throughput para picos de operaciones

## Consequences

- Mayor complejidad operativa (gestión del cluster Kafka)
- Latencia ligeramente mayor (~100ms adicionales) — dentro del SLA de 30s para pagos urgentes
- Necesidad de monitorización adicional del lag de los consumers
""",
    ),
    Artifact(
        id="DOM-PAY-001",
        type="dom",
        title="Reglas anti-fraude para transferencias internacionales",
        filename="DOM-PAY-001-anti-fraud-rules.md",
        content=f"""---
id: DOM-PAY-001
type: spec
layer: domain
domain: Payments
subdomain: International Transfers
status: draft
confidence: low
version: 1.0.0
created: {TODAY}
updated: {TODAY}
owner: carlos-riesgos
source_transcript: sample_transcript.txt
tags:
  - anti-fraud
  - compliance
  - sanctions
  - payments
---

# DOM-PAY-001 — Reglas anti-fraude para transferencias internacionales

## Intent

Define las reglas de negocio obligatorias para el chequeo anti-fraude de transferencias
internacionales, según requisitos regulatorios.

## Definition

### Concept

Toda transferencia internacional debe pasar por un proceso de validación anti-fraude
antes de ser enviada al gateway SWIFT.

### Rules

1. **Umbral de chequeo**: Toda transferencia superior a **50.000 EUR** debe pasar por
   chequeo anti-fraude obligatorio antes del envío.
2. **Países sancionados**: Las transferencias a países incluidos en la lista de sanciones
   deben **bloquearse automáticamente** sin excepción.
3. **Lista de sanciones**: Se utiliza la lista actualizada proporcionada por el departamento
   de Riesgos (Carlos).

### Constraints

- **Regulatorio**: Requisito no negociable — cumplimiento normativo obligatorio.
- **Latencia**: El chequeo anti-fraude debe completarse dentro del SLA de 30 segundos
  para pagos urgentes.

### Examples

| Transferencia | Importe | País destino | Resultado |
|--------------|---------|--------------|-----------|
| TX-001 | 25.000 EUR | Francia | ✅ Sin chequeo (< 50K) |
| TX-002 | 75.000 EUR | Alemania | ⚠️ Chequeo anti-fraude obligatorio |
| TX-003 | 10.000 EUR | País sancionado | ❌ Bloqueada automáticamente |

## Acceptance Criteria

- [ ] Transferencias > 50.000 EUR pasan por chequeo anti-fraude
- [ ] Transferencias a países sancionados se bloquean automáticamente
- [ ] Lista de países sancionados se actualiza periódicamente desde Riesgos
- [ ] Chequeo completo en < 30 segundos para pagos urgentes

## Open Questions

- ¿Con qué frecuencia se actualiza la lista de países sancionados?
- ¿Qué pasa con transferencias justo en el umbral de 50.000 EUR (inclusive/exclusive)?
""",
    ),
    Artifact(
        id="WRK-TASK-001",
        type="wrk-task",
        title="PoC del producer SWIFT con Kafka",
        filename="WRK-TASK-001-poc-swift-producer.md",
        content=f"""---
id: WRK-TASK-001
type: spec
layer: work-task
scope: ephemeral
status: draft
confidence: medium
version: 1.0.0
created: {TODAY}
updated: {TODAY}
owner: pedro-tech-lead
source_transcript: sample_transcript.txt
dependencies:
  - id: ADR-001
    relation: implements
tags:
  - swift
  - kafka
  - poc
  - producer
---

# WRK-TASK-001 — PoC del producer SWIFT con Kafka

## Objective

Montar una prueba de concepto (PoC) del producer Kafka que envía mensajes SWIFT MT103
al gateway. Validar que el patrón de mensajería asíncrona funciona dentro del SLA
de latencia definido.

## Implementation Notes

- Implementar un Kafka producer que publique mensajes MT103 en un topic dedicado
- El consumer leerá del topic y reenviará al gateway SWIFT
- Integrar el filtro de países sancionados (lista proporcionada por Carlos/Riesgos)
- Medir latencia end-to-end para verificar SLA de 30 segundos

## Acceptance Criteria

- [ ] Producer Kafka funcional enviando mensajes MT103
- [ ] Consumer que reenvía al gateway SWIFT
- [ ] Filtro de países sancionados integrado
- [ ] Latencia end-to-end < 30 segundos para pagos urgentes
- [ ] Mensajes no se pierden ante caída del gateway (replay desde Kafka)

## Test Plan

1. Enviar 100 mensajes MT103 de prueba y verificar entrega
2. Simular caída del gateway y verificar que los mensajes se retienen en Kafka
3. Medir latencia con carga de 1000 mensajes/minuto
""",
    ),
    Artifact(
        id="WRK-TASK-002",
        type="wrk-task",
        title="Documentar formato mensaje SWIFT MT103",
        filename="WRK-TASK-002-doc-swift-mt103.md",
        content=f"""---
id: WRK-TASK-002
type: spec
layer: work-task
scope: ephemeral
status: draft
confidence: medium
version: 1.0.0
created: {TODAY}
updated: {TODAY}
owner: pedro-tech-lead
source_transcript: sample_transcript.txt
tags:
  - swift
  - mt103
  - documentation
---

# WRK-TASK-002 — Documentar formato mensaje SWIFT MT103

## Objective

Documentar el formato del mensaje SWIFT MT103 que se va a utilizar en la plataforma
de pagos internacionales, incluyendo los campos obligatorios y opcionales.

## Implementation Notes

- Definir la estructura de campos del MT103
- Especificar campos obligatorios vs opcionales
- Incluir ejemplos de mensajes válidos
- Documentar las validaciones de formato

## Acceptance Criteria

- [ ] Documento con la estructura completa del MT103
- [ ] Ejemplos de mensajes válidos e inválidos
- [ ] Validaciones de formato especificadas
""",
    ),
]

MOCK_RESULT = ExtractionResult(
    summary="Reunión de diseño técnico sobre la plataforma de Pagos Internacionales. "
            "Se decidió usar Kafka como broker para mensajería SWIFT (ADR-001). "
            "Se definieron reglas anti-fraude: chequeo obligatorio para transferencias >50K EUR "
            "y bloqueo automático de países sancionados (DOM-PAY-001). "
            "Se asignaron tareas: PoC del producer SWIFT (Pedro) y documentación del MT103 (Pedro).",
    artifacts=MOCK_ARTIFACTS,
    source_transcript="sample_transcript.txt",
)


def main():
    print("=" * 60)
    print("  🧪 TEST LOCAL — KDD PMO Copilot")
    print("=" * 60)

    # 1. Guardar artefactos simulados en output/
    print("\n📝 Generando artefactos simulados...")
    saved = save_artifacts(MOCK_RESULT)
    print(f"\n✅ {len(saved)} ficheros guardados en output/\n")

    for path in saved:
        print(f"   📄 {path.name}")

    # 2. Guardar el resultado como JSON para que Streamlit lo recoja
    result_json = {
        "summary": MOCK_RESULT.summary,
        "source_transcript": MOCK_RESULT.source_transcript,
        "artifacts": [
            {
                "id": a.id,
                "type": a.type,
                "title": a.title,
                "filename": a.filename,
            }
            for a in MOCK_RESULT.artifacts
        ],
    }
    json_path = Path(__file__).parent / "output" / "_last_extraction.json"
    json_path.write_text(json.dumps(result_json, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'=' * 60}")
    print(f"  ✅ Artefactos listos para revisión")
    print(f"{'=' * 60}")
    print(f"\n  Ahora lanza Streamlit para validarlos:")
    print(f"  streamlit run app.py")
    print(f"\n  O para probar el email:")
    print(f"  python notifier.py")


if __name__ == "__main__":
    main()

