            st.error("❌ committer.py aún no implementado. Se guardaron en disco.")
app.py — Interfaz Streamlit para el PMO.
        # Actualizar contenido
Flujo simplificado:
1. La app detecta automáticamente las actas nuevas en /actas/
2. Las agrupa por proyecto
3. El PMO selecciona un proyecto y pulsa "Generar Specs"
4. Revisa las specs generadas (acta a la izquierda, specs a la derecha)
5. Edita lo que necesite y pulsa "Validar"
6. Las specs se commitean a /specs/ en el repo
        "✅ Validar y hacer Commit a GitHub",
with action_col2:
        st.success("✅ Artefactos guardados en output/")
with action_col1:
    if st.button("💾 Guardar cambios en disco", use_container_width=True):
        # Actualizar contenido editado en los artefactos
import re
        for artifact in result.artifacts:
            artifact.content = st.session_state.edited_artifacts.get(
from datetime import date, datetime
            )
action_col1, action_col2, action_col3 = st.columns([1, 1, 1])
# BARRA INFERIOR: ACCIONES
            st.session_state.edited_artifacts[artifact.id] = edited
# ────────────��────────────────────────────────────────────────
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

    Convención:
      actas/
        proyecto-alpha/
          2026-04-18_reunion-diseno.txt
        proyecto-beta/
          2026-04-19_kickoff.txt

    Ficheros sueltos van a "General".
    """
    projects = {}

    if not ACTAS_DIR.exists():
        return projects

    for item in sorted(ACTAS_DIR.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            project_name = item.name
            actas = sorted(
                [f for f in item.iterdir() if f.suffix in (".txt", ".md")],
                key=lambda f: f.name, reverse=True,
            )
            if actas:
                projects[project_name] = actas

    root_actas = sorted(
        [f for f in ACTAS_DIR.iterdir()
         if f.is_file() and f.suffix in (".txt", ".md") and f.name != "README.md"],
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


                key=f"editor_{artifact.id}",
                f"Contenido de {artifact.id}",
                value=st.session_state.edited_artifacts.get(artifact.id, artifact.content),
    for i, artifact in enumerate(result.artifacts):
        icon = type_icons.get(artifact.type, "📄")
        with st.expander(f"{icon} {artifact.id} — {artifact.title}", expanded=(i == 0)):
    # Tabs por tipo
    st.subheader(f"🧩 Artefactos Extraídos ({len(result.artifacts)})")
# ── COLUMNA DERECHA: Artefactos editables ──
        value=st.session_state.transcript_text,
# ── COLUMNA IZQUIERDA: Acta original ──
# Dos columnas: Acta | Artefactos
# Resumen
    st.info("👈 Usa el panel lateral para cargar una transcripción y extraer artefactos.")
st.markdown("# 📋 KDD PMO Copilot — Validación de Artefactos")
# LAYOUT PRINCIPAL: ACTA | ARTEFACTOS
    # Cargar desde disco (si ya se ejecutó antes)
if "current_acta_text" not in st.session_state:
    st.session_state.current_acta_text = ""
if "current_acta_name" not in st.session_state:
    st.session_state.current_acta_name = ""
if "current_project" not in st.session_state:
    st.session_state.current_project = ""
if "edited_specs" not in st.session_state:
    st.session_state.edited_specs = {}
        if md_files:
            artifacts = []
            for f in md_files:
                content = f.read_text(encoding="utf-8")
                art_id = f.stem.split("-")[0] + "-" + "-".join(f.stem.split("-")[1:3]) if "-" in f.stem else f.stem
# SIDEBAR
                import re
                id_match = re.search(r"^id:\s*(.+)$", content, re.MULTILINE)
                if id_match:
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

                    id=art_id,
                    type="loaded",
    if not all_projects:
        st.warning("📂 No hay actas en la carpeta `actas/`")
        st.info(f"Ruta: `{ACTAS_DIR}`")
        st.stop()
                    filename=f.name,
    # Selector de proyecto
    st.subheader("1️⃣ Selecciona proyecto")
                summary=summary, artifacts=artifacts
    project_options = []
    for proj, actas in all_projects.items():
        new_count = len([a for a in actas if not is_processed(a.name)])
        badge = f" 🆕 {new_count} nuevas" if new_count > 0 else " ✅"
        project_options.append(f"{proj}{badge}")
            st.session_state.edited_artifacts = {
    selected_idx = st.selectbox(
        "Proyecto:",
        range(len(project_options)),
        format_func=lambda i: project_options[i],
        label_visibility="collapsed",
    )
    selected_project = list(all_projects.keys())[selected_idx]
    project_actas = all_projects[selected_project]
                    transcript=st.session_state.transcript_text,
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
            st.session_state.current_acta_text = acta.read_text(encoding="utf-8")
            st.session_state.current_acta_name = acta.name
            st.session_state.current_project = selected_project
            st.session_state.extraction_result = None
            st.session_state.edited_specs = {}
            st.session_state.validated = False
    with col_a:
        adr_off = st.number_input("ADR offset", min_value=1, value=1, step=1)
        dom_off = st.number_input("DOM offset", min_value=1, value=1, step=1)
    # Botón de generar specs
    st.subheader("3️⃣ Generar specs")
        disabled=not st.session_state.transcript_text,
    if st.session_state.current_acta_name and not is_processed(st.session_state.current_acta_name):
        generate_btn = st.button(
            f"🚀 Generar specs de:\n{st.session_state.current_acta_name}",
            use_container_width=True,
            type="primary",
        )
                "Selecciona un acta:",
        if generate_btn:
            with st.spinner("Generando specs..."):
                try:
                    if config.GITHUB_TOKEN:
                        result = extract_artifacts(
                            transcript=st.session_state.current_acta_text,
                            today=date.today().isoformat(),
                            save=True,
                            source_transcript=st.session_state.current_acta_name,
                        )
                    else:
                        # Modo demo: sin token configurado
                        from test_local import MOCK_RESULT
                        from copy import deepcopy
                        result = deepcopy(MOCK_RESULT)
                        result.source_transcript = st.session_state.current_acta_name
                        save_artifacts(result)

                    st.session_state.extraction_result = result
                    st.session_state.edited_specs = {
                        a.id: a.content for a in result.artifacts
                    }
                    st.session_state.validated = False
                    mode = "GitHub Copilot" if config.GITHUB_TOKEN else "Demo"
                    st.success(f"✅ {len(result.artifacts)} specs generadas ({mode})")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    upload_mode = st.radio(
    elif not st.session_state.current_acta_name:
        st.info("👆 Selecciona un acta primero")
    else:
        st.success("✅ Esta acta ya fue procesada")

import config
from extractor import extract_artifacts, ExtractionResult, Artifact, save_artifacts
# LAYOUT PRINCIPAL
# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
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

st.set_page_config(
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
    page_icon="📋",
    layout="wide",
# ─────────────────────────────────────────────────────────────
# VISTA DE VALIDACIÓN: ACTA | SPECS
# ─────────────────────────────────────────────────────────────

    initial_sidebar_state="expanded",
)
# ─────────────────────────────────────────────────────────────
# ESTADO DE SESIÓN
# ─────────────────────────────────────────────────────────────
if "extraction_result" not in st.session_state:
    st.session_state.extraction_result = None
    st.session_state.transcript_text = ""
if "edited_artifacts" not in st.session_state:
    st.session_state.edited_artifacts = {}
if "validated" not in st.session_state:
        value=st.session_state.current_acta_text,


# ─────────────────────────────────────────────────────────────
# SIDEBAR: CARGA Y EXTRACCIÓN
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.subheader(f"🧩 Specs Generadas ({len(result.artifacts)})")
    st.title("KDD PMO Copilot")

    st.subheader("1️⃣ Cargar transcripción")
    for i, spec in enumerate(result.artifacts):
        icon = type_icons.get(spec.type, "📄")
        with st.expander(f"{icon} {spec.id} — {spec.title}", expanded=(i == 0)):
        ["📁 Subir fichero", "📂 Desde carpeta output"],
                f"Contenido de {spec.id}",
                value=st.session_state.edited_specs.get(spec.id, spec.content),

                key=f"editor_{spec.id}",

    if upload_mode == "📁 Subir fichero":
            st.session_state.edited_specs[spec.id] = edited
            "Sube el .txt de la transcripción",
            type=["txt", "md"],
        )
# BARRA DE ACCIONES
            st.session_state.transcript_text = uploaded.read().decode("utf-8")
            transcript_loaded = True
            st.success(f"✅ {uploaded.name} ({len(st.session_state.transcript_text)} chars)")

col_save, col_validate, col_status = st.columns([1, 1, 1])
        # Listar ficheros .txt en output/
with col_save:
    if st.button("💾 Guardar borrador", use_container_width=True):
        for spec in result.artifacts:
            spec.content = st.session_state.edited_specs.get(spec.id, spec.content)
            if selected:
        st.success("✅ Borrador guardado en disco")
                transcript_loaded = True
with col_validate:
        else:
        "✅ Validar y Commitear Specs",

    st.markdown("---")
    st.subheader("2️⃣ Extraer artefactos")

        for spec in result.artifacts:
            spec.content = st.session_state.edited_specs.get(spec.id, spec.content)


    col_a, col_d, col_t = st.columns(3)
    with col_a:
        adr_off = st.number_input("ADR offset", min_value=1, value=1, step=1)
    with col_d:
        dom_off = st.number_input("DOM offset", min_value=1, value=1, step=1)
            mark_as_processed(
                st.session_state.current_acta_name,
                [s.id for s in result.artifacts],
            )
    with col_t:
            st.success(f"✅ {len(committed)} specs commiteadas a /specs/")

    extract_btn = st.button(
        "🚀 Extraer con Gemini",
        use_container_width=True,
            mark_as_processed(
                st.session_state.current_acta_name,
                [s.id for s in result.artifacts],
            )
            st.warning("⚠️ GITHUB_TOKEN no configurado. Specs guardadas en disco.")
        type="primary",
    )

with col_status:
    if st.session_state.validated:
        st.success("🎉 Specs validadas")
        st.balloons()
                    a.id: a.content for a in result.artifacts
                }
                st.session_state.validated = False
                st.success(f"✅ {len(result.artifacts)} artefactos extraídos")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    # Cargar desde disco (si ya se ejecutó antes)
    st.markdown("---")
    if st.button("📥 Cargar artefactos previos", use_container_width=True):
        md_files = sorted(config.OUTPUT_DIR.glob("*.md"))
        md_files = [f for f in md_files if f.name != "_summary.md"]
        if md_files:
            artifacts = []
            for f in md_files:
                content = f.read_text(encoding="utf-8")
                art_id = f.stem.split("-")[0] + "-" + "-".join(f.stem.split("-")[1:3]) if "-" in f.stem else f.stem
                # Intentar extraer ID del frontmatter
                import re
                id_match = re.search(r"^id:\s*(.+)$", content, re.MULTILINE)
                if id_match:
                    art_id = id_match.group(1).strip()
                artifacts.append(Artifact(
                    id=art_id,
                    type="loaded",
                    title=f.stem,
                    filename=f.name,
                    content=content,
                ))
            summary_path = config.OUTPUT_DIR / "_summary.md"
            summary = summary_path.read_text(encoding="utf-8") if summary_path.exists() else ""
            st.session_state.extraction_result = ExtractionResult(
                summary=summary, artifacts=artifacts
            )
            st.session_state.edited_artifacts = {
                a.id: a.content for a in artifacts
            }
            st.success(f"✅ {len(artifacts)} artefactos cargados")
        else:
            st.warning("No hay artefactos en output/")


# ─────────────────────────────────────────────────────────────
# LAYOUT PRINCIPAL: ACTA | ARTEFACTOS
# ─────────────────────────────────────────────────────────────

st.markdown("# 📋 KDD PMO Copilot — Validación de Artefactos")

if not st.session_state.extraction_result:
    st.info("👈 Usa el panel lateral para cargar una transcripción y extraer artefactos.")
    st.stop()

result: ExtractionResult = st.session_state.extraction_result

# Resumen
st.markdown(f"**Resumen:** {result.summary}")
st.markdown("---")

# Dos columnas: Acta | Artefactos
left_col, right_col = st.columns([1, 1], gap="large")

# ── COLUMNA IZQUIERDA: Acta original ──
with left_col:
    st.subheader("📄 Acta Original")
    st.text_area(
        "Transcripción",
        value=st.session_state.transcript_text,
        height=600,
        disabled=True,
        label_visibility="collapsed",
    )

# ── COLUMNA DERECHA: Artefactos editables ──
with right_col:
    st.subheader(f"🧩 Artefactos Extraídos ({len(result.artifacts)})")

    # Tabs por tipo
    type_icons = {"adr": "🏗️", "dom": "📖", "wrk-task": "✅", "loaded": "📂"}

    for i, artifact in enumerate(result.artifacts):
        icon = type_icons.get(artifact.type, "📄")
        with st.expander(f"{icon} {artifact.id} — {artifact.title}", expanded=(i == 0)):
            edited = st.text_area(
                f"Contenido de {artifact.id}",
                value=st.session_state.edited_artifacts.get(artifact.id, artifact.content),
                height=350,
                key=f"editor_{artifact.id}",
                label_visibility="collapsed",
            )
            st.session_state.edited_artifacts[artifact.id] = edited


# ─────────────────────────────────────────────────────────────
# BARRA INFERIOR: ACCIONES
# ─────────────────────────────────────────────────────────────

st.markdown("---")

action_col1, action_col2, action_col3 = st.columns([1, 1, 1])

with action_col1:
    if st.button("💾 Guardar cambios en disco", use_container_width=True):
        # Actualizar contenido editado en los artefactos
        for artifact in result.artifacts:
            artifact.content = st.session_state.edited_artifacts.get(
                artifact.id, artifact.content
            )
        save_artifacts(result)
        st.success("✅ Artefactos guardados en output/")

with action_col2:
    validate_btn = st.button(
        "✅ Validar y hacer Commit a GitHub",
        use_container_width=True,
        type="primary",
    )
    if validate_btn:
        # Actualizar contenido
        for artifact in result.artifacts:
            artifact.content = st.session_state.edited_artifacts.get(
                artifact.id, artifact.content
            )
        try:
            from committer import commit_artifacts
            committed = commit_artifacts(
                result.artifacts,
                source_transcript=result.source_transcript,
            )
            st.session_state.validated = True
            st.success(f"✅ {len(committed)} artefactos commiteados a GitHub")
            for path in committed:
                st.code(path, language=None)
        except ImportError:
            st.error("❌ committer.py aún no implementado. Se guardaron en disco.")
            save_artifacts(result)
        except Exception as e:
            st.error(f"❌ Error en commit: {e}")

with action_col3:
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
with action_col3:
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


