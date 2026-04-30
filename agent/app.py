"""
app.py — Interfaz Streamlit para el PMO.

Flujo simplificado:
1. La app detecta automáticamente las actas nuevas en /actas/
2. Las agrupa por proyecto
3. El PMO selecciona un proyecto y pulsa "Generar Specs"
4. Revisa las specs generadas (acta a la izquierda, specs a la derecha)
5. Edita lo que necesite y pulsa "Validar"
6. Las specs se commitean a /specs/ en el repo
"""

import json
import re
import streamlit as st
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path

import config
from extractor import extract_artifacts, ExtractionResult, Artifact, save_artifacts


# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────────────────────
# RUTAS
# ─────────────────────────────────────────────────────────────

ACTAS_DIR = config.PROJECT_ROOT.parent / "actas"
SPECS_DIR = config.PROJECT_ROOT.parent / "specs"
MANIFEST_PATH = config.OUTPUT_DIR / "_processed_actas.json"


# ─────────────────────────────────────────────────────────────
# GESTIÓN DE ACTAS PROCESADAS
# ─────────────────────────────────────────────────────────────

def load_manifest() -> dict:
    """Carga el registro de actas ya procesadas."""
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {"processed": {}}


def save_manifest(manifest: dict):
    """Guarda el registro de actas procesadas."""
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def mark_as_processed(acta_name: str, specs_generated: list[str]):
    """Marca un acta como procesada con los IDs de specs generadas."""
    manifest = load_manifest()
    manifest["processed"][acta_name] = {
        "date": datetime.now().isoformat(),
        "specs": specs_generated,
    }
    save_manifest(manifest)


def is_processed(acta_name: str) -> bool:
    """Comprueba si un acta ya fue procesada."""
    manifest = load_manifest()
    return acta_name in manifest.get("processed", {})


# ─────────────────────────────────────────────────────────────
# DETECCIÓN DE ACTAS Y PROYECTOS
# ─────────────────────────────────────────────────────────────

def scan_actas() -> dict[str, list[Path]]:
    """
    Escanea la carpeta /actas/ y agrupa los ficheros por proyecto.
    Ficheros sueltos van a "General".
    """
    projects = {}

    if not ACTAS_DIR.exists():
        return projects

    for item in sorted(ACTAS_DIR.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            project_name = item.name
            actas = sorted(
                [f for f in item.iterdir() if f.suffix in (".txt", ".md", ".pdf", ".docx")],
                key=lambda f: f.name, reverse=True,
            )
            if actas:
                projects[project_name] = actas

    root_actas = sorted(
        [f for f in ACTAS_DIR.iterdir()
         if f.is_file() and f.suffix in (".txt", ".md", ".pdf", ".docx") and f.name != "README.md"],
        key=lambda f: f.name, reverse=True,
    )
    if root_actas:
        projects["General"] = root_actas

    return projects


def get_new_actas(projects: dict[str, list[Path]]) -> dict[str, list[Path]]:
    """Filtra solo las actas que NO han sido procesadas aún."""
    new = {}
    for project, actas in projects.items():
        new_actas = [a for a in actas if not is_processed(a.name)]
        if new_actas:
            new[project] = new_actas
    return new


# ─────────────────────────────────────────────────────────────
# ESTADO DE SESIÓN
# ─────────────────────────────────────────────────────────────

if "extraction_result" not in st.session_state:
    st.session_state.extraction_result = None
if "current_acta_text" not in st.session_state:
    st.session_state.current_acta_text = ""
if "current_acta_name" not in st.session_state:
    st.session_state.current_acta_name = ""
if "current_project" not in st.session_state:
    st.session_state.current_project = ""
if "edited_specs" not in st.session_state:
    st.session_state.edited_specs = {}
if "validated" not in st.session_state:
    st.session_state.validated = False


# ─────────────────────────────────────────────────────────────
# LECTURA DE ACTAS (TXT, MD, PDF, DOCX)
# ─────────────────────────────────────────────────────────────

from acta_loader import read_acta as _read_acta


# ─────────────────────────────────────────────────────────────
# OFFSETS POR PROYECTO
# ─────────────────────────────────────────────────────────────

def compute_offsets(project_output_dir: Path) -> dict:
    """
    Calcula los próximos offsets de ADR/DOM/TASK escaneando los .md ya
    generados en la carpeta output del proyecto, para evitar colisiones
    de IDs entre actas del mismo proyecto.
    """
    offsets = {"adr": 1, "dom": 1, "task": 1}
    if not project_output_dir.exists():
        return offsets

    pat_adr = re.compile(r"ADR-(\d+)", re.IGNORECASE)
    pat_dom = re.compile(r"DOM-[A-Z]+-(\d+)", re.IGNORECASE)
    pat_task = re.compile(r"WRK-TASK-(\d+)", re.IGNORECASE)

    max_adr = max_dom = max_task = 0
    for f in project_output_dir.glob("*.md"):
        name = f.stem
        if (m := pat_adr.search(name)):
            max_adr = max(max_adr, int(m.group(1)))
        if (m := pat_dom.search(name)):
            max_dom = max(max_dom, int(m.group(1)))
        if (m := pat_task.search(name)):
            max_task = max(max_task, int(m.group(1)))

    offsets["adr"] = max_adr + 1
    offsets["dom"] = max_dom + 1
    offsets["task"] = max_task + 1
    return offsets


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("📋 KDD PMO Copilot")
    st.caption("Knowledge-Driven Development")
    st.markdown("---")

    all_projects = scan_actas()
    new_projects = get_new_actas(all_projects)

    total_actas = sum(len(a) for a in all_projects.values())
    total_new = sum(len(a) for a in new_projects.values())
    total_processed = total_actas - total_new

    col1, col2, col3 = st.columns(3)
    col1.metric("Proyectos", len(all_projects))
    col2.metric("Actas nuevas", total_new)
    col3.metric("Procesadas", total_processed)

    if not all_projects:
        st.warning("📂 No hay actas en la carpeta `actas/`")
        st.info(f"Ruta: `{ACTAS_DIR}`")
        st.stop()

    # Selector de proyecto
    st.subheader("1️⃣ Selecciona proyecto")

    project_options = []
    for proj, actas in all_projects.items():
        new_count = len([a for a in actas if not is_processed(a.name)])
        badge = f" 🆕 {new_count} nuevas" if new_count > 0 else " ✅"
        project_options.append(f"{proj}{badge}")

    selected_idx = st.selectbox(
        "Proyecto:",
        range(len(project_options)),
        format_func=lambda i: project_options[i],
        label_visibility="collapsed",
    )
    selected_project = list(all_projects.keys())[selected_idx]
    project_actas = all_projects[selected_project]

    st.markdown("---")

    # Lista de actas del proyecto
    st.subheader("2️⃣ Actas del proyecto")

    for acta in project_actas:
        processed = is_processed(acta.name)
        icon = "✅" if processed else "🆕"
        if st.button(
            f"{icon} {acta.name}",
            key=f"acta_{acta.name}",
            use_container_width=True,
        ):
            st.session_state.current_acta_text = _read_acta(acta)
            st.session_state.current_acta_name = acta.name
            st.session_state.current_project = selected_project
            st.session_state.extraction_result = None
            st.session_state.edited_specs = {}
            st.session_state.validated = False

    st.markdown("---")

    # Botón de generar specs
    st.subheader("3️⃣ Generar specs")

    if st.session_state.current_acta_name and not is_processed(st.session_state.current_acta_name):
        generate_btn = st.button(
            f"🚀 Generar specs de:\n{st.session_state.current_acta_name}",
            use_container_width=True,
            type="primary",
        )
        if generate_btn:
            with st.spinner("Generando specs..."):
                try:
                    project_slug = st.session_state.current_project
                    project_output = config.OUTPUT_DIR / project_slug
                    project_output.mkdir(parents=True, exist_ok=True)
                    offsets = compute_offsets(project_output)

                    if config.GITHUB_TOKEN:
                        result = extract_artifacts(
                            transcript=st.session_state.current_acta_text,
                            today=date.today().isoformat(),
                            save=True,
                            output_dir=project_output,
                            source_transcript=st.session_state.current_acta_name,
                            project=project_slug,
                            adr_offset=offsets["adr"],
                            dom_offset=offsets["dom"],
                            task_offset=offsets["task"],
                        )
                    else:
                        from test_local import MOCK_RESULT
                        result = deepcopy(MOCK_RESULT)
                        result.source_transcript = st.session_state.current_acta_name
                        save_artifacts(result, output_dir=project_output)

                    st.session_state.extraction_result = result
                    st.session_state.edited_specs = {
                        a.id: a.content for a in result.artifacts
                    }
                    st.session_state.validated = False
                    mode = "GitHub Models" if config.GITHUB_TOKEN else "Demo"
                    st.success(f"✅ {len(result.artifacts)} specs generadas ({mode}) en `output/{project_slug}/`")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    import traceback
                    st.code(traceback.format_exc())
    elif not st.session_state.current_acta_name:
        st.info("👆 Selecciona un acta primero")
    else:
        st.success("✅ Esta acta ya fue procesada")


# ─────────────────────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ─────────────────────────────────────────────────────────────

st.markdown("# 📋 KDD PMO Copilot")

if not st.session_state.current_acta_name:
    st.info(
        "👈 Selecciona un **proyecto** y un **acta** en el panel lateral.\n\n"
        "Las actas con 🆕 son nuevas y necesitan generar specs.\n"
        "Las actas con ✅ ya fueron procesadas."
    )
    st.stop()

st.markdown(
    f"**Proyecto:** `{st.session_state.current_project}` · "
    f"**Acta:** `{st.session_state.current_acta_name}` · "
    f"**Estado:** {'✅ Procesada' if is_processed(st.session_state.current_acta_name) else '🆕 Pendiente'}"
)

# Si no hay resultado de extracción, mostrar solo el acta
if not st.session_state.extraction_result:
    st.markdown("---")
    st.subheader("📄 Transcripción del acta")
    st.text_area(
        "Contenido",
        value=st.session_state.current_acta_text,
        height=500,
        disabled=True,
        label_visibility="collapsed",
    )
    st.info("👈 Pulsa **'🚀 Generar specs'** en el panel lateral para extraer las specs de esta acta.")
    st.stop()


# ─────────────────────────────────────────────────────────────
# VISTA DE VALIDACIÓN: ACTA | SPECS
# ─────────────────────────────────────────────────────────────

result: ExtractionResult = st.session_state.extraction_result

# Resumen
st.markdown(f"**Resumen:** {result.summary}")
st.markdown("---")

# Dos columnas: Acta | Specs
left_col, right_col = st.columns([1, 1], gap="large")

# ── COLUMNA IZQUIERDA: Acta original ──
with left_col:
    st.subheader("📄 Acta Original")
    st.text_area(
        "Transcripción",
        value=st.session_state.current_acta_text,
        height=600,
        disabled=True,
        label_visibility="collapsed",
    )

# ── COLUMNA DERECHA: Specs editables ──
with right_col:
    st.subheader(f"🧩 Specs Generadas ({len(result.artifacts)})")

    type_icons = {"adr": "🏗️", "dom": "📖", "wrk-task": "✅", "loaded": "📂"}

    for i, spec in enumerate(result.artifacts):
        icon = type_icons.get(spec.type, "📄")
        with st.expander(f"{icon} {spec.id} — {spec.title}", expanded=(i == 0)):
            edited = st.text_area(
                f"Contenido de {spec.id}",
                value=st.session_state.edited_specs.get(spec.id, spec.content),
                height=350,
                key=f"editor_{spec.id}",
                label_visibility="collapsed",
            )
            st.session_state.edited_specs[spec.id] = edited


# ─────────────────────────────────────────────────────────────
# BARRA DE ACCIONES
# ─────────────────────────────────────────────────────────────

st.markdown("---")

col_save, col_validate, col_notify = st.columns([1, 1, 1])

with col_save:
    if st.button("💾 Guardar borrador", use_container_width=True):
        for spec in result.artifacts:
            spec.content = st.session_state.edited_specs.get(spec.id, spec.content)
        save_artifacts(result)
        st.success("✅ Borrador guardado en disco")

with col_validate:
    if st.button(
        "✅ Validar y Commitear Specs",
        use_container_width=True,
        type="primary",
    ):
        for spec in result.artifacts:
            spec.content = st.session_state.edited_specs.get(spec.id, spec.content)

        if config.GITHUB_TOKEN and config.GITHUB_REPO:
            try:
                from committer import commit_artifacts
                committed = commit_artifacts(
                    result.artifacts,
                    source_transcript=result.source_transcript,
                    project=st.session_state.current_project,
                )
                mark_as_processed(
                    st.session_state.current_acta_name,
                    [s.id for s in result.artifacts],
                )
                st.session_state.validated = True
                st.success(f"✅ {len(committed)} specs commiteadas a /specs/")
                for path in committed:
                    st.code(path, language=None)
            except Exception as e:
                st.error(f"❌ Error en commit: {e}")
        else:
            save_artifacts(result)
            mark_as_processed(
                st.session_state.current_acta_name,
                [s.id for s in result.artifacts],
            )
            st.warning("⚠️ GITHUB_TOKEN/GITHUB_REPO no configurados. Specs guardadas en disco.")

with col_notify:
    if st.button("📧 Notificar al PMO", use_container_width=True):
        try:
            from notifier import send_notification
            send_notification(result)
            st.success("✅ Email enviado al PMO")
        except ImportError:
            st.warning("⚠️ notifier.py aún no implementado.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

if st.session_state.validated:
    st.balloons()








