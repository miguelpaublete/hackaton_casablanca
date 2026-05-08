"""
smart_tools.py — Herramientas inteligentes del KDD PMO Copilot.

1. Smart Agenda: Genera orden del día sugerida antes de reuniones.
2. Auto-Setup: Genera planificación inicial de proyecto desde un prompt.
3. Onboarding Kit: Genera kit de bienvenida para nuevos integrantes.
"""

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import config
from acta_loader import read_acta
from extractor import call_github_models


# ─────────────────────────────────────────────────────────────
# UTILIDADES COMUNES
# ─────────────────────────────────────────────────────────────

ACTAS_DIR = config.PROJECT_ROOT.parent / "actas"
SPECS_DIR = config.PROJECT_ROOT.parent / "specs"
SMART_AGENDA_DIR = config.PROJECT_ROOT.parent / "Smart agenda"
SETUP_DIR = config.PROJECT_ROOT.parent / "Set-up proyecto"
HISTORICAL_PLANS_DIR = SETUP_DIR / "_historical"


def _slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip().lower()
    return re.sub(r"[-\s]+", "-", text)[:60] or "sin-nombre"


def _gather_historical_plans() -> str:
    """Recopila planificaciones históricas de referencia (Set-up proyecto/_historical)."""
    chunks = []
    if HISTORICAL_PLANS_DIR.exists():
        for f in sorted(HISTORICAL_PLANS_DIR.glob("*.md")):
            content = f.read_text(encoding="utf-8", errors="ignore")
            chunks.append(f"### Plan histórico: {f.name}\n{content[:3000]}\n")
    return "\n---\n".join(chunks) if chunks else "(Sin planes históricos cargados)"


def _gather_project_context(project: str, max_actas: int = 3) -> str:
    """
    Recopila contexto de un proyecto: últimas actas + specs existentes.
    """
    chunks = []

    # Últimas actas del proyecto
    actas_path = ACTAS_DIR / project
    if actas_path.exists():
        acta_files = sorted(
            [f for f in actas_path.iterdir()
             if f.suffix in (".txt", ".md", ".pdf", ".docx")
             and not f.name.endswith(".converted.txt")
             and f.name != "README.md"],
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )[:max_actas]
        for af in acta_files:
            text = read_acta(af)
            # Limitar a 3000 chars por acta para no reventar el contexto
            chunks.append(f"### Acta: {af.name}\n{text[:3000]}\n")

    # Specs existentes del proyecto
    specs_path = SPECS_DIR / project
    if specs_path.exists():
        spec_files = sorted(specs_path.glob("*.md"))[:10]
        for sf in spec_files:
            content = sf.read_text(encoding="utf-8", errors="ignore")
            chunks.append(f"### Spec: {sf.name}\n{content[:2000]}\n")

    return "\n---\n".join(chunks) if chunks else "(Sin contexto previo disponible)"


def _gather_all_specs() -> str:
    """Recopila todas las specs de todos los proyectos (para Auto-Setup y Onboarding)."""
    chunks = []
    if SPECS_DIR.exists():
        for project_dir in sorted(SPECS_DIR.iterdir()):
            if project_dir.is_dir():
                spec_files = sorted(project_dir.glob("*.md"))[:5]
                for sf in spec_files:
                    content = sf.read_text(encoding="utf-8", errors="ignore")
                    chunks.append(f"### [{project_dir.name}] {sf.name}\n{content[:1500]}\n")
    return "\n---\n".join(chunks[:20]) if chunks else "(Sin specs históricas)"


# ─────────────────────────────────────────────────────────────
# 1. SMART AGENDA
# ─────────────────────────────────────────────────────────────

@dataclass
class AgendaResult:
    project: str
    agenda_md: str
    key_points: list[str]
    pending_decisions: list[str]
    risks: list[str]
    saved_path: Path | None = None


def generate_smart_agenda(
    project: str,
    meeting_type: str = "seguimiento semanal",
    additional_context: str = "",
) -> AgendaResult:
    """
    Genera una orden del día inteligente basada en el contexto del proyecto.
    """
    project_context = _gather_project_context(project, max_actas=3)

    prompt = f"""You are an expert PMO assistant. Generate a smart meeting agenda in Spanish.

## CONTEXT
- Project: {project}
- Meeting type: {meeting_type}
- Today: {date.today().isoformat()}
- Additional notes from PMO: {additional_context or 'None'}

## PROJECT HISTORY (last meetings and specs):
{project_context}

## TASK
Analyze the project history and generate:
1. A suggested agenda (ordered list of discussion points with time estimates)
2. Key points that MUST be discussed (blockers, pending decisions, deadlines)
3. Pending decisions that need resolution
4. Identified risks

## OUTPUT FORMAT (JSON only, no markdown fences):
{{
  "agenda_md": "# Orden del Día - {{project}}\\n\\n## 1. Punto...\\n...(full markdown agenda)",
  "key_points": ["point1", "point2"],
  "pending_decisions": ["decision1", "decision2"],
  "risks": ["risk1", "risk2"]
}}
"""
    raw = call_github_models(prompt)
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```\s*$", "", cleaned)

    data = json.loads(cleaned)
    result = AgendaResult(
        project=project,
        agenda_md=data.get("agenda_md", ""),
        key_points=data.get("key_points", []),
        pending_decisions=data.get("pending_decisions", []),
        risks=data.get("risks", []),
    )

    # Guardar como .txt en Smart agenda/{project}/
    project_dir = SMART_AGENDA_DIR / project
    project_dir.mkdir(parents=True, exist_ok=True)
    today_str = date.today().isoformat()
    out_path = project_dir / f"smart_agenda_reunion_{today_str}.txt"

    body = []
    body.append(f"SMART AGENDA — Reunión del día {today_str}")
    body.append(f"Proyecto: {project}")
    body.append(f"Tipo de reunión: {meeting_type}")
    body.append("=" * 70)
    body.append("")
    body.append(result.agenda_md)
    body.append("")
    body.append("-" * 70)
    body.append("PUNTOS CLAVE:")
    for p in result.key_points:
        body.append(f"  • {p}")
    body.append("")
    body.append("DECISIONES PENDIENTES:")
    for d in result.pending_decisions:
        body.append(f"  • {d}")
    body.append("")
    body.append("RIESGOS IDENTIFICADOS:")
    for r in result.risks:
        body.append(f"  • {r}")

    out_path.write_text("\n".join(body), encoding="utf-8")
    result.saved_path = out_path
    return result


# ─────────────────────────────────────────────────────────────
# 2. AUTO-SETUP DE PROYECTO
# ─────────────────────────────────────────────────────────────

@dataclass
class ProjectSetupResult:
    project_name: str
    wbs_md: str
    deliverables: list[str]
    milestones: list[dict]
    suggested_structure: str
    wbs_tasks: list[dict]  # [{phase, task, owner, week_start, week_end, duration}]
    saved_path: Path | None = None


def generate_project_setup(
    project_description: str,
    project_name: str = "",
    duration_weeks: int = 12,
) -> ProjectSetupResult:
    """
    Genera la planificación inicial y estructura documental de un proyecto.
    Consulta specs históricas + planificaciones históricas como referencia.
    Exporta a Excel en `Set-up proyecto/`.
    """
    historical_specs = _gather_all_specs()
    historical_plans = _gather_historical_plans()

    prompt = f"""You are a senior PMO in a banking consultancy (BBVA). Generate a complete project setup in Spanish.

## INPUT
- Project name: {project_name or 'To be defined from description'}
- Description: {project_description}
- Estimated duration: {duration_weeks} weeks
- Today: {date.today().isoformat()}

## HISTORICAL PROJECT PLANS (use as primary reference for structure):
{historical_plans}

## HISTORICAL SPECS (additional context):
{historical_specs}

## TASK
Generate:
1. A Work Breakdown Structure (WBS) in Markdown with phases, tasks, and subtasks
2. List of required deliverables
3. Critical milestones with estimated dates
4. Suggested folder/document structure for the project
5. A FLAT list of WBS tasks with owner, week_start, week_end and duration_weeks (for Excel export)

Use patterns from the historical plans when applicable.

## OUTPUT FORMAT (JSON only):
{{
  "project_name": "Final project name",
  "wbs_md": "# WBS\\n\\n## Fase 1...\\n...(complete WBS in markdown)",
  "deliverables": ["deliverable1", "deliverable2"],
  "milestones": [
    {{"name": "Kickoff", "week": 1, "description": "..."}},
    {{"name": "MVP", "week": 6, "description": "..."}}
  ],
  "suggested_structure": "```\\nproject/\\n  specs/\\n  docs/\\n  ...\\n```",
  "wbs_tasks": [
    {{"phase": "Fase 1 - Análisis", "task": "Recogida de requisitos", "owner": "PM", "week_start": 1, "week_end": 2, "duration_weeks": 2}},
    {{"phase": "Fase 1 - Análisis", "task": "Aprobación stakeholders", "owner": "PMO", "week_start": 2, "week_end": 3, "duration_weeks": 1}}
  ]
}}
"""
    raw = call_github_models(prompt)
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```\s*$", "", cleaned)

    data = json.loads(cleaned)
    result = ProjectSetupResult(
        project_name=data.get("project_name", project_name),
        wbs_md=data.get("wbs_md", ""),
        deliverables=data.get("deliverables", []),
        milestones=data.get("milestones", []),
        suggested_structure=data.get("suggested_structure", ""),
        wbs_tasks=data.get("wbs_tasks", []),
    )

    # Generar Excel en Set-up proyecto/
    result.saved_path = _export_setup_to_excel(result, duration_weeks)
    return result


def _export_setup_to_excel(result: ProjectSetupResult, duration_weeks: int) -> Path:
    """Genera un Excel con la planificación: hojas WBS, Entregables, Hitos, Estructura."""
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
    except ImportError:
        # Fallback: guardar como markdown si no hay openpyxl
        SETUP_DIR.mkdir(parents=True, exist_ok=True)
        slug = _slugify(result.project_name)
        out = SETUP_DIR / f"setup_{slug}_{date.today().isoformat()}.md"
        out.write_text(
            f"# {result.project_name}\n\n## WBS\n{result.wbs_md}\n\n"
            f"## Entregables\n" + "\n".join(f"- {d}" for d in result.deliverables) +
            f"\n\n## Hitos\n" + "\n".join(f"- Semana {m.get('week')}: {m.get('name')} — {m.get('description','')}" for m in result.milestones) +
            f"\n\n## Estructura\n{result.suggested_structure}",
            encoding="utf-8",
        )
        return out

    SETUP_DIR.mkdir(parents=True, exist_ok=True)
    slug = _slugify(result.project_name)
    out_path = SETUP_DIR / f"setup_{slug}_{date.today().isoformat()}.xlsx"

    wb = Workbook()
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="1F4E78")

    # Hoja 1: Resumen
    ws = wb.active
    ws.title = "Resumen"
    ws["A1"] = "Proyecto"
    ws["B1"] = result.project_name
    ws["A2"] = "Duración (semanas)"
    ws["B2"] = duration_weeks
    ws["A3"] = "Fecha generación"
    ws["B3"] = date.today().isoformat()
    for cell in ("A1", "A2", "A3"):
        ws[cell].font = Font(bold=True)
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 60

    # Hoja 2: WBS
    ws_wbs = wb.create_sheet("WBS")
    headers = ["Fase", "Tarea", "Responsable", "Semana inicio", "Semana fin", "Duración (sem)"]
    for col, h in enumerate(headers, 1):
        c = ws_wbs.cell(row=1, column=col, value=h)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center")
    for i, t in enumerate(result.wbs_tasks, 2):
        ws_wbs.cell(row=i, column=1, value=t.get("phase", ""))
        ws_wbs.cell(row=i, column=2, value=t.get("task", ""))
        ws_wbs.cell(row=i, column=3, value=t.get("owner", ""))
        ws_wbs.cell(row=i, column=4, value=t.get("week_start", ""))
        ws_wbs.cell(row=i, column=5, value=t.get("week_end", ""))
        ws_wbs.cell(row=i, column=6, value=t.get("duration_weeks", ""))
    for col_letter, w in zip("ABCDEF", (28, 50, 18, 14, 14, 16)):
        ws_wbs.column_dimensions[col_letter].width = w

    # Hoja 3: Entregables
    ws_d = wb.create_sheet("Entregables")
    ws_d.cell(row=1, column=1, value="Entregable").font = header_font
    ws_d.cell(row=1, column=1).fill = header_fill
    for i, d in enumerate(result.deliverables, 2):
        ws_d.cell(row=i, column=1, value=d)
    ws_d.column_dimensions["A"].width = 80

    # Hoja 4: Hitos
    ws_m = wb.create_sheet("Hitos")
    for col, h in enumerate(["Semana", "Hito", "Descripción"], 1):
        c = ws_m.cell(row=1, column=col, value=h)
        c.font = header_font
        c.fill = header_fill
    for i, m in enumerate(result.milestones, 2):
        ws_m.cell(row=i, column=1, value=m.get("week", ""))
        ws_m.cell(row=i, column=2, value=m.get("name", ""))
        ws_m.cell(row=i, column=3, value=m.get("description", ""))
    for col_letter, w in zip("ABC", (12, 30, 70)):
        ws_m.column_dimensions[col_letter].width = w

    # Hoja 5: Estructura sugerida
    ws_s = wb.create_sheet("Estructura")
    ws_s["A1"] = "Estructura documental sugerida"
    ws_s["A1"].font = header_font
    ws_s["A1"].fill = header_fill
    ws_s["A2"] = result.suggested_structure
    ws_s["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws_s.column_dimensions["A"].width = 100
    ws_s.row_dimensions[2].height = 400

    wb.save(out_path)
    return out_path


# ─────────────────────────────────────────────────────────────
# 3. ONBOARDING KIT
# ─────────────────────────────────────────────────────────────

@dataclass
class OnboardingResult:
    person_role: str
    project: str
    welcome_doc_md: str
    glossary: list[dict]  # [{term, definition}]
    recent_decisions: list[str]
    first_tasks: list[dict]  # [{task, week, description}]


def generate_onboarding_kit(
    project: str,
    person_role: str,
    person_name: str = "",
    start_date: str = "",
) -> OnboardingResult:
    """
    Genera un kit de onboarding personalizado para un nuevo integrante.
    """
    project_context = _gather_project_context(project, max_actas=5)
    all_specs = _gather_all_specs()

    prompt = f"""You are a senior PMO creating an onboarding kit for a new team member. Write everything in Spanish.

## NEW TEAM MEMBER
- Name: {person_name or 'Nuevo integrante'}
- Role: {person_role}
- Start date: {start_date or 'Next week'}
- Project: {project}

## PROJECT CONTEXT (recent meetings and specs):
{project_context}

## ALL TEAM SPECS (for glossary and cross-project context):
{all_specs}

## TASK
Generate a comprehensive onboarding kit including:
1. A welcome document (markdown) with project overview, team structure hints, and key contacts
2. A glossary of technical terms and acronyms used in this project
3. Summary of the last 3 key decisions that affect this person's role
4. Assigned tasks for the first 15 days (progressive difficulty)

## OUTPUT FORMAT (JSON only):
{{
  "welcome_doc_md": "# Bienvenida al proyecto {{project}}\\n\\n...(full markdown document)",
  "glossary": [
    {{"term": "KDD", "definition": "Knowledge-Driven Development..."}},
    {{"term": "ADR", "definition": "Architecture Decision Record..."}}
  ],
  "recent_decisions": [
    "Se decidió usar Vertex AI para...",
    "Se aprobó la arquitectura de..."
  ],
  "first_tasks": [
    {{"task": "Leer specs del proyecto", "week": 1, "description": "..."}},
    {{"task": "Configurar entorno", "week": 1, "description": "..."}}
  ]
}}
"""
    raw = call_github_models(prompt)
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```\s*$", "", cleaned)

    data = json.loads(cleaned)
    return OnboardingResult(
        person_role=person_role,
        project=project,
        welcome_doc_md=data.get("welcome_doc_md", ""),
        glossary=data.get("glossary", []),
        recent_decisions=data.get("recent_decisions", []),
        first_tasks=data.get("first_tasks", []),
    )


def onboarding_to_txt(result: OnboardingResult, person_name: str = "") -> str:
    """Serializa un OnboardingResult a texto plano para descarga."""
    lines = []
    lines.append(f"ONBOARDING KIT — Proyecto {result.project}")
    lines.append(f"Generado: {date.today().isoformat()}")
    if person_name:
        lines.append(f"Para: {person_name}")
    lines.append(f"Rol: {result.person_role}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("DOCUMENTO DE BIENVENIDA")
    lines.append("-" * 70)
    lines.append(result.welcome_doc_md)
    lines.append("")
    lines.append("=" * 70)
    lines.append("GLOSARIO DE TÉRMINOS")
    lines.append("-" * 70)
    for item in result.glossary:
        lines.append(f"  • {item.get('term', '')}: {item.get('definition', '')}")
    lines.append("")
    lines.append("=" * 70)
    lines.append("DECISIONES CLAVE RECIENTES")
    lines.append("-" * 70)
    for i, d in enumerate(result.recent_decisions, 1):
        lines.append(f"  {i}. {d}")
    lines.append("")
    lines.append("=" * 70)
    lines.append("TAREAS PARA LOS PRIMEROS 15 DÍAS")
    lines.append("-" * 70)
    for t in result.first_tasks:
        lines.append(f"  [Semana {t.get('week', '?')}] {t.get('task', '')}")
        if t.get("description"):
            lines.append(f"      → {t.get('description')}")
    return "\n".join(lines)







