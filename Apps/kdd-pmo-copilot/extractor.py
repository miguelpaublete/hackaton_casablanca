"""
extractor.py — Paso 4: Extracción de artefactos KDD desde un acta de reunión.

Lee una transcripción, la envía a Vertex AI (Gemini) con el prompt de
extracción, y devuelve los artefactos KDD (ADR, DOM, WRK-TASK) parseados.

Uso:
    from extractor import extract_artifacts
    result = extract_artifacts("texto del acta...")
    # result.summary  -> resumen de la reunión
    # result.artifacts -> lista de Artifact(id, type, title, filename, content)
"""

import json
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import config


# ─────────────────────────────────────────────────────────────
# 1. MODELOS DE DATOS
# ─────────────────────────────────────────────────────────────

@dataclass
class Artifact:
    """Un artefacto KDD extraído del acta."""
    id: str
    type: str           # "adr", "dom", "wrk-task"
    title: str
    filename: str
    content: str        # Markdown completo (frontmatter + body)


@dataclass
class ExtractionResult:
    """Resultado completo de la extracción."""
    summary: str
    artifacts: list[Artifact] = field(default_factory=list)
    raw_response: str = ""
    source_transcript: str = ""     # Nombre del fichero de acta origen


# ─────────────────────────────────────────────────────────────
# 2. PREPARAR PROMPT
# ─────────────────────────────────────────────────────────────

def load_prompt_template() -> str:
    """Carga la plantilla de prompt desde el fichero .md."""
    prompt_path = config.PROMPTS_DIR / "extraction_prompt.md"
    return prompt_path.read_text(encoding="utf-8")


def build_prompt(
    transcript: str,
    today: str | None = None,
    adr_offset: int = 1,
    dom_offset: int = 1,
    task_offset: int = 1,
) -> str:
    """
    Construye el prompt final sustituyendo el transcript y metadatos.

    Args:
        transcript: Texto del acta de reunión.
        today: Fecha en formato YYYY-MM-DD (por defecto hoy).
        adr_offset: Número inicial para ADRs (para no pisar IDs existentes).
        dom_offset: Número inicial para DOMs.
        task_offset: Número inicial para WRK-TASKs.
    """
    if today is None:
        today = date.today().isoformat()

    template = load_prompt_template()
    prompt = template.replace("{TRANSCRIPT}", transcript)

    # Añadir contexto de offsets y fecha al final del system prompt
    context_block = (
        f"\n\n## Context Variables\n"
        f"- Today's date: {today}\n"
        f"- ADR numbering starts at: {adr_offset:03d}\n"
        f"- DOM numbering starts at: {dom_offset:03d}\n"
        f"- WRK-TASK numbering starts at: {task_offset:03d}\n"
    )
    prompt += context_block
    return prompt


# ─────────────────────────────────────────────────────────────
# 3. LLAMADA A VERTEX AI
# ─────────────────────────────────────────────────────────────

def call_vertex_ai(prompt: str) -> str:
    """
    Envía el prompt a Vertex AI (Gemini) y devuelve la respuesta como texto.

    Requiere autenticación con Google Cloud:
    - En local: `gcloud auth application-default login`
    - En CI: service account key vía GOOGLE_APPLICATION_CREDENTIALS
    """
    from google.cloud import aiplatform
    from vertexai.generative_models import GenerativeModel, GenerationConfig

    # Inicializar Vertex AI
    aiplatform.init(
        project=config.GCP_PROJECT_ID,
        location=config.GCP_LOCATION,
    )

    model = GenerativeModel(config.VERTEX_MODEL)

    generation_config = GenerationConfig(
        temperature=0.2,          # Baja temperatura = más determinista
        max_output_tokens=8192,
        response_mime_type="application/json",
    )

    response = model.generate_content(
        prompt,
        generation_config=generation_config,
    )

    return response.text


# ─────────────────────────────────────────────────────────────
# 4. PARSEAR RESPUESTA
# ─────────────────────────────────────────────────────────────

def parse_response(raw_json: str) -> ExtractionResult:
    """
    Parsea la respuesta JSON de Gemini y devuelve un ExtractionResult.

    Es tolerante a respuestas envueltas en ```json ... ```.
    """
    # Limpiar posibles bloques de código
    cleaned = raw_json.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```\s*$", "", cleaned)

    data = json.loads(cleaned)

    artifacts = []
    for item in data.get("artifacts", []):
        artifacts.append(Artifact(
            id=item["id"],
            type=item.get("type", "unknown"),
            title=item.get("title", ""),
            filename=item.get("filename", f"{item['id']}.md"),
            content=item.get("content", ""),
        ))

    return ExtractionResult(
        summary=data.get("summary", ""),
        artifacts=artifacts,
        raw_response=raw_json,
    )


# ─────────────────────────────────────────────────────────────
# 5. GUARDAR ARTEFACTOS EN DISCO
# ─────────────────────────────────────────────────────────────

def save_artifacts(result: ExtractionResult, output_dir: Path | None = None) -> list[Path]:
    """
    Guarda cada artefacto como un fichero .md individual.

    Returns:
        Lista de Paths de los ficheros generados.
    """
    if output_dir is None:
        output_dir = config.OUTPUT_DIR

    output_dir.mkdir(parents=True, exist_ok=True)
    saved_paths = []

    for artifact in result.artifacts:
        filepath = output_dir / artifact.filename
        filepath.write_text(artifact.content, encoding="utf-8")
        saved_paths.append(filepath)
        print(f"  ✅ {artifact.id} → {filepath.name}")

    # Guardar también el resumen
    summary_path = output_dir / "_summary.md"
    summary_path.write_text(
        f"# Resumen de la reunión\n\n{result.summary}\n\n"
        f"## Artefactos generados\n\n"
        + "\n".join(f"- `{a.id}` — {a.title}" for a in result.artifacts),
        encoding="utf-8",
    )
    saved_paths.append(summary_path)

    return saved_paths


# ─────────��───────────────────────────────────────────────────
# 6. FUNCIÓN PRINCIPAL DE EXTRACCIÓN
# ─────────────────────────────────────────────────────────────

def extract_artifacts(
    transcript: str,
    today: str | None = None,
    adr_offset: int = 1,
    dom_offset: int = 1,
    task_offset: int = 1,
    save: bool = True,
    output_dir: Path | None = None,
    source_transcript: str = "",
) -> ExtractionResult:
    """
    Pipeline completo: prompt → Vertex AI → parse → (opcionalmente) guardar.

    Args:
        transcript: Texto del acta de reunión.
        today: Fecha (YYYY-MM-DD). Por defecto, hoy.
        adr_offset / dom_offset / task_offset: Offsets de numeración.
        save: Si True, guarda los .md en disco.
        output_dir: Carpeta de salida (por defecto: config.OUTPUT_DIR).
        source_transcript: Nombre del fichero de acta (para trazabilidad).

    Returns:
        ExtractionResult con el resumen y los artefactos.
    """
    print("📝 Construyendo prompt de extracción...")
    prompt = build_prompt(transcript, today, adr_offset, dom_offset, task_offset)

    print(f"🤖 Llamando a Vertex AI ({config.VERTEX_MODEL})...")
    raw_response = call_vertex_ai(prompt)

    print("🔍 Parseando respuesta...")
    result = parse_response(raw_response)
    result.source_transcript = source_transcript

    # Inyectar trazabilidad al acta en el frontmatter de cada artefacto
    if source_transcript:
        for artifact in result.artifacts:
            # Añadir source_transcript justo antes del cierre del frontmatter (---)
            if "\n---\n" in artifact.content:
                parts = artifact.content.split("\n---\n", 1)
                # parts[0] = "---\nyaml...", parts[1] = body
                artifact.content = (
                    f"{parts[0]}\n"
                    f"source_transcript: {source_transcript}\n"
                    f"---\n{parts[1]}"
                )

    print(f"   Resumen: {result.summary[:100]}...")
    print(f"   Artefactos encontrados: {len(result.artifacts)}")

    if save:
        print("💾 Guardando artefactos en disco...")
        save_artifacts(result, output_dir)

    return result


# ─────────────────────────────────────────────────────────────
# 7. CLI PARA PRUEBAS LOCALES
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extrae artefactos KDD desde un acta de reunión."
    )
    parser.add_argument(
        "transcript_file",
        help="Ruta al fichero de texto con la transcripción.",
    )
    parser.add_argument(
        "--date", default=None,
        help="Fecha de la reunión (YYYY-MM-DD). Por defecto: hoy.",
    )
    parser.add_argument(
        "--output-dir", default=None,
        help="Carpeta de salida para los artefactos.",
    )
    parser.add_argument(
        "--adr-offset", type=int, default=1,
        help="Offset de numeración para ADRs.",
    )
    parser.add_argument(
        "--dom-offset", type=int, default=1,
        help="Offset de numeración para DOMs.",
    )
    parser.add_argument(
        "--task-offset", type=int, default=1,
        help="Offset de numeración para WRK-TASKs.",
    )

    args = parser.parse_args()

    transcript_path = Path(args.transcript_file)
    if not transcript_path.exists():
        print(f"❌ No se encuentra el fichero: {transcript_path}")
        exit(1)

    transcript_text = transcript_path.read_text(encoding="utf-8")
    print(f"📄 Acta cargada: {transcript_path.name} ({len(transcript_text)} chars)")

    out_dir = Path(args.output_dir) if args.output_dir else None

    result = extract_artifacts(
        transcript=transcript_text,
        today=args.date,
        adr_offset=args.adr_offset,
        dom_offset=args.dom_offset,
        task_offset=args.task_offset,
        save=True,
        output_dir=out_dir,
        source_transcript=transcript_path.name,
    )

    print(f"\n✅ Extracción completada: {len(result.artifacts)} artefactos generados.")




