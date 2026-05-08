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

    VALID_SUFFIXES = (".txt", ".md", ".pdf", ".docx")

    def _filter_actas(files: list[Path]) -> list[Path]:
        """
        Filtra archivos de actas:
        - Excluir .converted.txt (son cache interno)
        - Si hay un .txt/.md para un acta, ocultar el PDF/DOCX correspondiente
        """
        # Recoger stems de los .txt/.md que ya existen
        txt_stems = set()
        for f in files:
            if f.suffix in (".txt", ".md") and not f.name.endswith(".converted.txt"):
                txt_stems.add(f.stem)

        result = []
        for f in files:
            # Saltar caches internos
            if f.name.endswith(".converted.txt"):
                continue
            # Saltar PDF/DOCX si ya hay un .txt con el mismo nombre base
            if f.suffix in (".pdf", ".docx") and f.stem in txt_stems:
                continue
            result.append(f)
        return result

    if not ACTAS_DIR.exists():
        return projects

    for item in sorted(ACTAS_DIR.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            project_name = item.name
            all_files = [f for f in item.iterdir() if f.suffix in VALID_SUFFIXES and f.name != "README.md"]
            actas = sorted(
                _filter_actas(all_files),
                key=lambda f: f.name, reverse=True,
            )
            if actas:
                projects[project_name] = actas

    all_root = [f for f in ACTAS_DIR.iterdir()
                if f.is_file() and f.suffix in VALID_SUFFIXES and f.name != "README.md"]
    root_actas = sorted(
        _filter_actas(all_root),
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

    # ── Monitor / Notificación manual ──────────────────────────
    st.subheader("📡 Monitor de actas")

    pmo_email = config.PMO_EMAIL or "⚠️ PMO_EMAIL no configurado"
    has_email = bool(
        (getattr(config, "MAILJET_API_KEY", "") and getattr(config, "MAILJET_API_SECRET", ""))
        or (config.SMTP_USER and config.SMTP_PASSWORD)
    )

    st.caption(f"Notificando a: **{pmo_email}**")
    if not has_email:
        st.warning("⚠️ Sin credenciales de email. Configura Mailjet o SMTP en `.env`.")

    if st.button("📧 Enviar aviso actas nuevas", use_container_width=True, disabled=not has_email):
        try:
            from watcher import scan_new_actas, send_watcher_email
            app_url = f"http://localhost:{config.STREAMLIT_PORT}"
            new = scan_new_actas()
            if new:
                ok = send_watcher_email(new, app_url)
                if ok:
                    st.success(f"✅ Email enviado con {sum(len(v) for v in new.values())} acta(s) nueva(s)")
                else:
                    st.error("❌ Error al enviar email (revisa consola)")
            else:
                st.info("✅ No hay actas nuevas pendientes de notificar.")
        except Exception as e:
            st.error(f"❌ {e}")

    st.caption("💡 Para monitorización continua, ejecuta en otra terminal:\n`python watcher.py --interval 30`")

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

# ─────────────────────────────────────────────────────────────
# NAVEGACIÓN POR PESTAÑAS
# ─────────────────────────────────────────────────────────────

tab_specs, tab_agenda, tab_setup, tab_onboarding = st.tabs([
    "🧩 Generador de Specs",
    "📅 Smart Agenda",
    "🏗️ Auto-Setup Proyecto",
    "👋 Onboarding Kit",
])

# ══════════════════════════════════════════════════════════════
# TAB: SMART AGENDA
# ══════════════════════════════════════════════════════════════
with tab_agenda:
    st.subheader("📅 Smart Agenda — Preparación de reuniones")
    st.caption("Genera automáticamente una orden del día sugerida basada en el histórico del proyecto.")

    agenda_projects = list(scan_actas().keys())
    if not agenda_projects:
        st.warning("No hay proyectos con actas disponibles.")
    else:
        ag_col1, ag_col2 = st.columns(2)
        with ag_col1:
            agenda_project = st.selectbox("Proyecto:", agenda_projects, key="agenda_project")
        with ag_col2:
            meeting_type = st.text_input("Tipo de reunión:", value="Seguimiento semanal", key="agenda_meeting_type")

        additional_notes = st.text_area(
            "Notas adicionales (opcional):",
            placeholder="Ej: Incluir tema de migración cloud, recordar deadline del viernes...",
            key="agenda_notes",
        )

        if st.button("🚀 Generar Agenda", type="primary", key="btn_agenda"):
            if not config.GITHUB_TOKEN:
                st.error("❌ Configura GITHUB_TOKEN en .env para usar esta funcionalidad.")
            else:
                with st.spinner("Analizando contexto del proyecto y generando agenda..."):
                    try:
                        from smart_tools import generate_smart_agenda
                        agenda_result = generate_smart_agenda(
                            project=agenda_project,
                            meeting_type=meeting_type,
                            additional_context=additional_notes,
                        )
                        st.session_state["agenda_result"] = agenda_result
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

        if "agenda_result" in st.session_state and st.session_state["agenda_result"]:
            ar = st.session_state["agenda_result"]
            st.markdown("---")
            if ar.saved_path:
                st.success(f"✅ Smart Agenda guardada en: `{ar.saved_path}`")
            st.markdown(ar.agenda_md)

            col_kp, col_pd = st.columns(2)
            with col_kp:
                st.markdown("### 🔑 Puntos Clave")
                for p in ar.key_points:
                    st.markdown(f"- {p}")
            with col_pd:
                st.markdown("### ⚠️ Decisiones Pendientes")
                for d in ar.pending_decisions:
                    st.markdown(f"- {d}")

            if ar.risks:
                st.markdown("### 🚨 Riesgos Identificados")
                for r in ar.risks:
                    st.markdown(f"- {r}")

# ══════════════════════════════════════════════════════════════
# TAB: AUTO-SETUP PROYECTO
# ══════════════════════════════════════════════════════════════
with tab_setup:
    st.subheader("🏗️ Auto-Setup de Proyecto")
    st.caption("Genera planificación inicial (WBS, entregables, hitos) desde una descripción sencilla. Consulta specs históricas del equipo.")

    setup_name = st.text_input("Nombre del proyecto:", placeholder="Ej: Migración Core Bancario", key="setup_name")
    setup_desc = st.text_area(
        "Descripción del proyecto:",
        placeholder="Describe en 2-3 frases qué se quiere conseguir, tecnologías involucradas, equipo estimado...",
        height=120,
        key="setup_desc",
    )
    setup_weeks = st.slider("Duración estimada (semanas):", 4, 52, 12, key="setup_weeks")

    if st.button("🚀 Generar Setup", type="primary", key="btn_setup"):
        if not setup_desc:
            st.warning("Escribe una descripción del proyecto.")
        elif not config.GITHUB_TOKEN:
            st.error("❌ Configura GITHUB_TOKEN en .env para usar esta funcionalidad.")
        else:
            with st.spinner("Consultando specs históricas y generando planificación..."):
                try:
                    from smart_tools import generate_project_setup
                    setup_result = generate_project_setup(
                        project_description=setup_desc,
                        project_name=setup_name,
                        duration_weeks=setup_weeks,
                    )
                    st.session_state["setup_result"] = setup_result
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    if "setup_result" in st.session_state and st.session_state["setup_result"]:
        sr = st.session_state["setup_result"]
        st.markdown("---")
        st.markdown(f"### 📋 Proyecto: {sr.project_name}")

        if sr.saved_path:
            st.success(f"✅ Planificación exportada a: `{sr.saved_path}`")
            try:
                with open(sr.saved_path, "rb") as fh:
                    st.download_button(
                        label="⬇️ Descargar Excel de planificación",
                        data=fh.read(),
                        file_name=sr.saved_path.name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_setup_excel",
                    )
            except Exception:
                pass

        tab_wbs, tab_deliv, tab_miles, tab_struct = st.tabs(["WBS", "Entregables", "Hitos", "Estructura"])

        with tab_wbs:
            st.markdown(sr.wbs_md)
        with tab_deliv:
            for d in sr.deliverables:
                st.markdown(f"- ✅ {d}")
        with tab_miles:
            for m in sr.milestones:
                st.markdown(f"**Semana {m.get('week', '?')}** — {m.get('name', '')}")
                st.caption(m.get("description", ""))
        with tab_struct:
            st.markdown(sr.suggested_structure)

# ══════════════════════════════════════════════════════════════
# TAB: ONBOARDING KIT
# ══════════════════════════════════════════════════════════════
with tab_onboarding:
    st.subheader("👋 Generador de Onboarding Kit")
    st.caption("Crea un plan de acogida 100% personalizado para un recurso nuevo al instante.")

    onb_projects = list(scan_actas().keys())
    if not onb_projects:
        st.warning("No hay proyectos disponibles.")
    else:
        onb_col1, onb_col2 = st.columns(2)
        with onb_col1:
            onb_project = st.selectbox("Proyecto:", onb_projects, key="onb_project")
            onb_name = st.text_input("Nombre del nuevo integrante (opcional):", key="onb_name")
        with onb_col2:
            onb_role = st.text_input("Rol:", placeholder="Ej: Analista de Riesgos Junior", key="onb_role")
            onb_start = st.date_input("Fecha de incorporación:", key="onb_start")

        if st.button("🚀 Generar Onboarding Kit", type="primary", key="btn_onboarding"):
            if not onb_role:
                st.warning("Indica el rol del nuevo integrante.")
            elif not config.GITHUB_TOKEN:
                st.error("❌ Configura GITHUB_TOKEN en .env para usar esta funcionalidad.")
            else:
                with st.spinner("Consultando cerebro RAG del proyecto y generando kit..."):
                    try:
                        from smart_tools import generate_onboarding_kit
                        onb_result = generate_onboarding_kit(
                            project=onb_project,
                            person_role=onb_role,
                            person_name=onb_name,
                            start_date=str(onb_start),
                        )
                        st.session_state["onb_result"] = onb_result
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

    if "onb_result" in st.session_state and st.session_state["onb_result"]:
        ob = st.session_state["onb_result"]
        st.markdown("---")

        # Botón de descarga del kit completo en TXT
        try:
            from smart_tools import onboarding_to_txt
            kit_txt = onboarding_to_txt(ob, person_name=st.session_state.get("onb_name", ""))
            safe_role = ob.person_role.lower().replace(" ", "-")[:30]
            st.download_button(
                label="⬇️ Descargar Onboarding Kit (.txt)",
                data=kit_txt.encode("utf-8"),
                file_name=f"onboarding_{ob.project}_{safe_role}.txt",
                mime="text/plain",
                key="dl_onboarding_txt",
            )
        except Exception as e:
            st.warning(f"No se pudo preparar la descarga: {e}")

        tab_welcome, tab_glossary, tab_decisions, tab_tasks = st.tabs([
            "📄 Documento de Bienvenida", "📚 Glosario", "🏗️ Decisiones Recientes", "✅ Tareas 15 días"
        ])

        with tab_welcome:
            st.markdown(ob.welcome_doc_md)
        with tab_glossary:
            for item in ob.glossary:
                st.markdown(f"**{item.get('term', '')}**: {item.get('definition', '')}")
        with tab_decisions:
            for i, dec in enumerate(ob.recent_decisions, 1):
                st.markdown(f"{i}. {dec}")
        with tab_tasks:
            for t in ob.first_tasks:
                st.markdown(f"**Semana {t.get('week', '?')}** — {t.get('task', '')}")
                st.caption(t.get("description", ""))


# ══════════════════════════════════════════════════════════════
# TAB: GENERADOR DE SPECS (contenido original)
# ══════════════════════════════════════════════════════════════
with tab_specs:
    if not st.session_state.current_acta_name:
        st.info(
            "👈 Selecciona un **proyecto** y un **acta** en el panel lateral.\n\n"
            "Las actas con 🆕 son nuevas y necesitan generar specs.\n"
            "Las actas con ✅ ya fueron procesadas."
        )
    else:
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
        else:
            # ── VISTA DE VALIDACIÓN: ACTA | SPECS ──
            result: ExtractionResult = st.session_state.extraction_result

            if result is not None:
                st.markdown(f"**Resumen:** {result.summary}")
                st.markdown("---")

                left_col, right_col = st.columns([1, 1], gap="large")

                with left_col:
                    st.subheader("📄 Acta Original")
                    st.text_area(
                        "Transcripción",
                        value=st.session_state.current_acta_text,
                        height=600,
                        disabled=True,
                        label_visibility="collapsed",
                    )

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

                # ── BARRA DE ACCIONES ──
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




