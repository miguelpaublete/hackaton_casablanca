"""
extractor.py - Extraccion de artefactos KDD desde un acta de reunion.
Lee una transcripcion, la envia a GitHub Models (GPT-4o) con el prompt de
extraccion, y devuelve los artefactos KDD (ADR, DOM, WRK-TASK) parseados.
Uso:
    from extractor import extract_artifacts
    result = extract_artifacts("texto del acta...")
    # result.summary  -> resumen de la reunion
    # result.artifacts -> lista de Artifact(id, type, title, filename, content)
"""
import json
import os
import re
import requests
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
import config
# -----------------------------------------------------------------
# 1. MODELOS DE DATOS
# -----------------------------------------------------------------
@dataclass
class Artifact:
    """Un artefacto KDD extraido del acta."""
    id: str
    type: str           # "adr", "dom", "wrk-task"
    title: str
    filename: str
    content: str        # Markdown completo (frontmatter + body)
@dataclass
class ExtractionResult:
    """Resultado completo de la extraccion."""
    summary: str
    artifacts: list[Artifact] = field(default_factory=list)
    raw_response: str = ""
    source_transcript: str = ""
# -----------------------------------------------------------------
# 2. PREPARAR PROMPT
# -----------------------------------------------------------------

# Archivos del framework KDD que se inyectan como contexto autoritativo.
# El orden importa: de más general (taxonomía) a más específico (anatomía).
_FRAMEWORK_FILES = [
    "framework/knowledge-architecture/unified-taxonomy.md",
    "framework/knowledge-architecture/spec-types.md",
    "framework/knowledge-architecture/spec-anatomy.md",
]

# Presupuesto máximo para el contexto del framework (en chars).
# 8000 tokens ≈ 6000 palabras ≈ 24000 chars.
# Reservamos ~12000 chars para el framework, dejando el resto
# para el prompt template (~6000) + el transcript (~6000).
_FRAMEWORK_BUDGET_CHARS = 10_000


def _extract_framework_essentials(content: str, filename: str) -> str:
    """
    Extrae solo las secciones esenciales de un documento del framework,
    descartando ejemplos extensos, diagramas ASCII grandes y secciones
    comparativas que no aportan a la generación de specs.
    """
    lines = content.splitlines()
    result_lines = []
    skip_sections = {
        "## Differential Advantages",
        "## Extending to Other Verticals",
        "## The Knowledge-Work Duality",
        "## Derived Knowledge Graph",
        "## Current Tooling vs. Full Activation",
        "## How Activation Works",
        "## Activation Matrix",
        "### vs. GitHub Spec Kit",
        "### vs. Vibe Coding",
        "### vs. Waterfall",
        "## Complete Example: DOM-RISK-001",
        "## Validation Checklist",
    }
    in_skip = False
    in_code_block = False
    code_block_lines = 0

    for line in lines:
        # Detectar bloques de código largos y truncarlos
        if line.strip().startswith("```"):
            if in_code_block:
                in_code_block = False
                code_block_lines = 0
                result_lines.append(line)
                continue
            else:
                in_code_block = True
                code_block_lines = 0
                result_lines.append(line)
                continue

        if in_code_block:
            code_block_lines += 1
            if code_block_lines <= 8:  # Solo primeras 8 líneas de cada bloque
                result_lines.append(line)
            elif code_block_lines == 9:
                result_lines.append("  ...")
            continue

        # Detectar secciones a saltar
        for skip in skip_sections:
            if line.startswith(skip):
                in_skip = True
                break

        if in_skip:
            # Terminar skip al encontrar un heading del mismo o menor nivel
            if line.startswith("## ") and not any(line.startswith(s) for s in skip_sections):
                in_skip = False
            elif line.startswith("# ") and not line.startswith("## "):
                in_skip = False
            else:
                continue

        result_lines.append(line)

    return "\n".join(result_lines)


def load_framework_context() -> str:
    """
    Carga los documentos del framework KDD desde /framework y los
    concatena como contexto compacto para el modelo.
    Aplica extracción de esenciales + presupuesto de chars.
    """
    repo_root = Path(__file__).parent.parent
    sections = []
    total_chars = 0

    for rel_path in _FRAMEWORK_FILES:
        full_path = repo_root / rel_path
        if full_path.exists():
            raw = full_path.read_text(encoding="utf-8")
            compact = _extract_framework_essentials(raw, full_path.name)

            # Respetar presupuesto
            remaining = _FRAMEWORK_BUDGET_CHARS - total_chars
            if remaining <= 0:
                print(f"  [framework] PRESUPUESTO AGOTADO, saltando: {rel_path}")
                continue
            if len(compact) > remaining:
                compact = compact[:remaining] + "\n\n(... truncado por presupuesto de contexto)"
                print(f"  [framework] truncado: {rel_path} ({remaining} chars de {len(compact)})")
            else:
                print(f"  [framework] cargado: {rel_path} ({len(compact)} chars, original {len(raw)})")

            sections.append(f"### {full_path.name}\n\n{compact}")
            total_chars += len(compact)
        else:
            print(f"  [framework] AVISO: no encontrado: {full_path}")

    if not sections:
        print("  [framework] ADVERTENCIA: ningún fichero del framework encontrado.")
        return "(Framework documentation not available — using built-in rules only.)"

    header = (
        "Follow these framework documents strictly for artifact types, "
        "frontmatter fields, and body section structure.\n\n---\n\n"
    )
    result = header + "\n\n---\n\n".join(sections)
    print(f"  [framework] TOTAL: {len(result):,} chars ({len(result)//4} tokens aprox)")
    return result


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
    project: str = "tbd",
) -> str:
    """
    Construye el prompt final inyectando el framework KDD real y los metadatos.
    Trunca el transcript si el prompt total supera el presupuesto de tokens.
    """
    if today is None:
        today = date.today().isoformat()

    template = load_prompt_template()
    framework_context = load_framework_context()

    # Calcular cuánto espacio queda para el transcript
    # Presupuesto total: ~28000 chars ≈ 7000 tokens (dejando margen para los 8000)
    TOTAL_BUDGET_CHARS = 28_000
    base_prompt = (
        template
        .replace("{FRAMEWORK_CONTEXT}", framework_context)
        .replace("{TRANSCRIPT}", "")
        .replace("{TODAY}", today)
        .replace("{PROJECT}", project)
        .replace("{ADR_OFFSET}", str(adr_offset))
        .replace("{DOM_OFFSET}", str(dom_offset))
        .replace("{TASK_OFFSET}", str(task_offset))
    )
    remaining = TOTAL_BUDGET_CHARS - len(base_prompt)
    if remaining < 1000:
        remaining = 1000  # mínimo para que tenga sentido

    if len(transcript) > remaining:
        print(f"  [prompt] Transcript truncado: {len(transcript)} -> {remaining} chars")
        transcript = transcript[:remaining] + "\n\n(... transcript truncado por límite de tokens)"

    prompt = (
        template
        .replace("{FRAMEWORK_CONTEXT}", framework_context)
        .replace("{TRANSCRIPT}", transcript)
        .replace("{TODAY}", today)
        .replace("{PROJECT}", project)
        .replace("{ADR_OFFSET}", str(adr_offset))
        .replace("{DOM_OFFSET}", str(dom_offset))
        .replace("{TASK_OFFSET}", str(task_offset))
    )
    print(f"  [prompt] Total: {len(prompt):,} chars (~{len(prompt)//4} tokens)")
    return prompt
# -----------------------------------------------------------------
# 3. LLAMADA A GITHUB MODELS
# -----------------------------------------------------------------
def call_github_models(prompt: str) -> str:
    """
    Envia el prompt a GitHub Models API y devuelve la respuesta.
    Usa el GITHUB_TOKEN configurado en .env.
    """
    token = config.GITHUB_TOKEN
    if not token:
        raise ValueError(
            "GITHUB_TOKEN no configurado. Ponlo en .env\n"
            "Es el mismo token que usas para GitHub Copilot."
        )
    model = os.environ.get("GITHUB_MODEL", "openai/gpt-4.1")
    proxy_url = config.HTTP_PROXY
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert Knowledge Architect. Always respond with valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 8192,
    }
    proxies = {"https": proxy_url, "http": proxy_url} if proxy_url else None
    endpoint = os.environ.get(
        "GITHUB_MODELS_ENDPOINT",
        "https://models.github.ai/inference/chat/completions",
    )
    response = requests.post(
        endpoint,
        headers=headers,
        json=payload,
        proxies=proxies,
        timeout=120,
    )
    if response.status_code != 200:
        if response.status_code == 403 and "no_access" in response.text:
            raise RuntimeError(
                "❌ Tu GITHUB_TOKEN no tiene permiso 'Models: Read'.\n\n"
                "SOLUCIÓN: Crea un nuevo Fine-grained PAT en:\n"
                "https://github.com/settings/personal-access-tokens/new\n"
                "→ Account permissions → Models → Read\n"
                "→ Repository permissions → Contents → Read and write\n\n"
                f"Modelo solicitado: {model}\n"
                f"Respuesta API: {response.text[:200]}"
            )
        raise RuntimeError(
            f"GitHub Models API error {response.status_code}: {response.text}"
        )
    data = response.json()
    return data["choices"][0]["message"]["content"]
# -----------------------------------------------------------------
# 4. PARSEAR RESPUESTA
# -----------------------------------------------------------------
def parse_response(raw_json: str) -> ExtractionResult:
    """
    Parsea la respuesta JSON y devuelve un ExtractionResult.
    Es tolerante a respuestas envueltas en ```json ... ```.
    """
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
# -----------------------------------------------------------------
# 5. GUARDAR ARTEFACTOS EN DISCO
# -----------------------------------------------------------------
def save_artifacts(result: ExtractionResult, output_dir: Path | None = None) -> list[Path]:
    """Guarda cada artefacto como un fichero .md individual."""
    if output_dir is None:
        output_dir = config.OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    saved_paths = []
    for artifact in result.artifacts:
        filepath = output_dir / artifact.filename
        filepath.write_text(artifact.content, encoding="utf-8")
        saved_paths.append(filepath)
        print(f"  OK {artifact.id} -> {filepath.name}")
    # Guardar tambien el resumen
    summary_path = output_dir / "_summary.md"
    summary_path.write_text(
        f"# Resumen de la reunion\n\n{result.summary}\n\n"
        f"## Artefactos generados\n\n"
        + "\n".join(f"- `{a.id}` - {a.title}" for a in result.artifacts),
        encoding="utf-8",
    )
    saved_paths.append(summary_path)
    return saved_paths
# -----------------------------------------------------------------
# 6. FUNCION PRINCIPAL DE EXTRACCION
# -----------------------------------------------------------------
def extract_artifacts(
    transcript: str,
    today: str | None = None,
    adr_offset: int = 1,
    dom_offset: int = 1,
    task_offset: int = 1,
    save: bool = True,
    output_dir: Path | None = None,
    source_transcript: str = "",
    project: str = "tbd",
) -> ExtractionResult:
    """Pipeline completo: prompt -> GitHub Models -> parse -> (opcionalmente) guardar."""
    print(f"Construyendo prompt de extraccion (project={project})...")
    prompt = build_prompt(transcript, today, adr_offset, dom_offset, task_offset, project)
    print("Llamando a GitHub Models...")
    raw_response = call_github_models(prompt)
    print("Parseando respuesta...")
    result = parse_response(raw_response)
    result.source_transcript = source_transcript
    # Inyectar trazabilidad al acta en el frontmatter
    if source_transcript:
        for artifact in result.artifacts:
            if "\n---\n" in artifact.content:
                parts = artifact.content.split("\n---\n", 1)
                artifact.content = (
                    f"{parts[0]}\n"
                    f"source_transcript: {source_transcript}\n"
                    f"---\n{parts[1]}"
                )
    print(f"   Resumen: {result.summary[:100]}...")
    print(f"   Artefactos encontrados: {len(result.artifacts)}")
    if save:
        print("Guardando artefactos en disco...")
        save_artifacts(result, output_dir)
    return result
# -----------------------------------------------------------------
# 7. CLI PARA PRUEBAS LOCALES
# -----------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Extrae artefactos KDD desde un acta de reunion."
    )
    parser.add_argument("transcript_file", help="Ruta al .txt con la transcripcion.")
    parser.add_argument("--date", default=None, help="Fecha (YYYY-MM-DD).")
    parser.add_argument("--output-dir", default=None, help="Carpeta de salida.")
    parser.add_argument("--adr-offset", type=int, default=1)
    parser.add_argument("--dom-offset", type=int, default=1)
    parser.add_argument("--task-offset", type=int, default=1)
    args = parser.parse_args()
    transcript_path = Path(args.transcript_file)
    if not transcript_path.exists():
        print(f"No se encuentra el fichero: {transcript_path}")
        exit(1)
    transcript_text = transcript_path.read_text(encoding="utf-8")
    print(f"Acta cargada: {transcript_path.name} ({len(transcript_text)} chars)")
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
    print(f"\nExtraccion completada: {len(result.artifacts)} artefactos generados.")
