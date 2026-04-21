# KDD PMO Copilot

Automatización de la metodología Knowledge-Driven Development: extrae artefactos KDD (ADR, DOM, WRK-TASK) desde transcripciones de reuniones usando Vertex AI.

## Arquitectura

```
Apps Script (compi)                    PMO
   │                                    │
   │  sube acta .txt                    │  revisa y valida
   ▼                                    ▼
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  GitHub   │───▶│ GitHub       │───▶│  Streamlit   │───▶│  Commit a    │
│  /actas/  │    │ Actions      │    │  (app.py)    │    │  /specs/     │
│  *.txt    │    │ extractor.py │    │  Validación  │    │  committer   │
└──────────┘    │ + Gemini API │    └──────────────┘    └──────────────┘
                └──────────────┘
```

### Flujo paso a paso

1. **Apps Script** (tu compi): recoge la transcripción de Drive y la sube a `actas/` en el repo GitHub.
2. **GitHub Actions** (`kdd-extract.yml`): detecta el nuevo `.txt`, ejecuta `extractor.py` con Vertex AI (Gemini), genera los artefactos `.md`.
3. **Streamlit** (`app.py`): el PMO abre la UI, ve el acta a la izquierda y los artefactos a la derecha, los edita si hace falta.
4. **Commit** (`committer.py`): al pulsar "Validar", los `.md` se commitean a `/specs/` en el repo.
5. **Consumo**: GitHub Copilot `@workspace` usa los specs como contexto (RAG nativo).

## Estructura

```
repo/
├── .github/workflows/
│   └── kdd-extract.yml            # GitHub Actions pipeline
├── actas/                         # Transcripciones (Apps Script las deja aquí)
├── Apps/kdd-pmo-copilot/
│   ├── config.py                  # Configuración (env vars, sin hardcoding)
│   ├── extractor.py               # Acta → Gemini → artefactos .md
│   ├── notifier.py                # Email HTML al PMO
│   ├── app.py                     # UI Streamlit de validación
│   ├── committer.py               # Commit a GitHub con PyGithub
│   ├── prompts/
│   │   └── extraction_prompt.md   # Prompt KDD para Gemini
│   ├── output/                    # Artefactos generados (gitignored)
│   ├── requirements.txt
│   └── .env.example
├── specs/                         # Artefactos validados (destino final)
└── ...
```

## Quick Start

```bash
# 1. Instalar dependencias
cd Apps/kdd-pmo-copilot
pip install -r requirements.txt

# 2. Configurar credenciales
cp .env.example .env
# Editar .env con tus valores reales

# 3. Autenticarse en GCP
gcloud auth application-default login

# 4. Probar extracción con acta de ejemplo
python extractor.py output/sample_transcript.txt

# 5. Lanzar la UI de validación
streamlit run app.py
```

## GitHub Actions — Secrets necesarios

| Secret | Descripción |
|--------|-------------|
| `GCP_PROJECT_ID` | ID del proyecto en Google Cloud |
| `GCP_LOCATION` | Región de Vertex AI (ej. `europe-west1`) |
| `VERTEX_MODEL` | Modelo Gemini (ej. `gemini-2.0-flash`) |
| `GCP_SA_KEY_JSON` | JSON de la Service Account de GCP |

## Comandos útiles

```bash
# Extracción manual
python extractor.py ../../actas/2026-04-18_reunion.txt --date 2026-04-18

# Commit manual de artefactos
python committer.py output/ADR-001-*.md output/DOM-*.md

# Preview email sin enviar
python notifier.py

# Lanzar Streamlit
streamlit run app.py
```
