"""
app.py — Paso 6: Interfaz Streamlit para validación de artefactos KDD.

Layout:
  - Izquierda: Acta original (transcripción)
  - Derecha: Artefactos extraídos como tarjetas editables
  - Botón "Validar" → dispara commit a GitHub (Paso 7)

Uso:
    streamlit run app.py
"""

import json
import streamlit as st
from pathlib import Path
from datetime import date

import config
from extractor import extract_artifacts, ExtractionResult, Artifact, save_artifacts

# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="KDD PMO Copilot",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# ESTADO DE SESIÓN
# ─────────────────────────────────────────────────────────────

if "extraction_result" not in st.session_state:
    st.session_state.extraction_result = None
if "transcript_text" not in st.session_state:
    st.session_state.transcript_text = ""
if "edited_artifacts" not in st.session_state:
    st.session_state.edited_artifacts = {}
if "validated" not in st.session_state:
    st.session_state.validated = False


# ─────────────────────────────────────────────────────────────
# SIDEBAR: CARGA Y EXTRACCIÓN
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.title("KDD PMO Copilot")
    st.markdown("---")

    st.subheader("1️⃣ Cargar transcripción")

    upload_mode = st.radio(
        "Origen del acta:",
        ["📁 Subir fichero", "📂 Desde carpeta output"],
        horizontal=True,
    )

    transcript_loaded = False

    if upload_mode == "📁 Subir fichero":
        uploaded = st.file_uploader(
            "Sube el .txt de la transcripción",
            type=["txt", "md"],
        )
        if uploaded:
            st.session_state.transcript_text = uploaded.read().decode("utf-8")
            transcript_loaded = True
            st.success(f"✅ {uploaded.name} ({len(st.session_state.transcript_text)} chars)")

    else:
        # Listar ficheros .txt en output/
        output_files = sorted(config.OUTPUT_DIR.glob("*.txt"))
        if output_files:
            selected = st.selectbox(
                "Selecciona un acta:",
                output_files,
                format_func=lambda p: p.name,
            )
            if selected:
                st.session_state.transcript_text = selected.read_text(encoding="utf-8")
                transcript_loaded = True
                st.success(f"✅ {selected.name}")
        else:
            st.warning("No hay ficheros .txt en output/")

    st.markdown("---")
    st.subheader("2️⃣ Extraer artefactos")

    col_date, col_model = st.columns(2)
    with col_date:
        meeting_date = st.date_input("Fecha reunión", value=date.today())
    with col_model:
        st.text_input("Modelo", value=config.VERTEX_MODEL, disabled=True)

    col_a, col_d, col_t = st.columns(3)
    with col_a:
        adr_off = st.number_input("ADR offset", min_value=1, value=1, step=1)
    with col_d:
        dom_off = st.number_input("DOM offset", min_value=1, value=1, step=1)
    with col_t:
        task_off = st.number_input("TASK offset", min_value=1, value=1, step=1)

    extract_btn = st.button(
        "🚀 Extraer con Gemini",
        disabled=not st.session_state.transcript_text,
        use_container_width=True,
        type="primary",
    )

    if extract_btn and st.session_state.transcript_text:
        with st.spinner("Llamando a Vertex AI..."):
            try:
                result = extract_artifacts(
                    transcript=st.session_state.transcript_text,
                    today=meeting_date.isoformat(),
                    adr_offset=adr_off,
                    dom_offset=dom_off,
                    task_offset=task_off,
                    save=True,
                )
                st.session_state.extraction_result = result
                st.session_state.edited_artifacts = {
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
    st.balloons()


