# KDD PMO Copilot — Hackaton Casablanca

Automatización de la metodología **Knowledge-Driven Development (KDD)**: genera, valida y almacena specs de conocimiento a partir de transcripciones de reuniones.

## Arquitectura del repositorio

```
├── framework/          → Metodología KDD (reglas, validación, ejemplos)
├── agent/              → Agente PMO Copilot (extractor, interfaz, commit)
├── actas/              → Transcripciones de reuniones (input)
├── specs/              → Specs validadas por el PMO (output)
└── .github/workflows/  → Pipeline CI/CD
```

## Flujo de trabajo

```
Tu compi (Apps Script)                PMO
   │                                  │
   │  sube acta a /actas/             │  revisa y valida en Streamlit
   ▼                                  ▼
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  /actas/  │───▶│  agent/      │───▶│  Streamlit   │───▶│  /specs/     │
│  *.txt    │    │  extractor   │    │  (app.py)    │    │  validadas   │
└──────────┘    │  + Gemini    │    │  validación  │    │  en GitHub   │
                └──────────────┘    └──────────────┘    └──────────────┘
```

## Quick Start

```bash
cd agent
pip install -r requirements.txt
cp .env.example .env        # Configurar credenciales
streamlit run app.py        # Lanzar interfaz de validación
```

## Estructura detallada

### `framework/` — Metodología KDD
Contiene las reglas de creación y validación de specs, la taxonomía unificada,
la anatomía de specs, ejemplos de referencia y el validador CLI.

### `agent/` — Agente PMO Copilot
Código Python que:
1. Lee transcripciones de `/actas/`
2. Llama a Vertex AI (Gemini) para generar specs
3. Muestra interfaz Streamlit para que el PMO valide
4. Commitea las specs validadas a `/specs/`

### `actas/` — Transcripciones (input)
Carpeta donde el Apps Script deposita las transcripciones de Google Meet.

### `specs/` — Specs validadas (output)
Specs aprobadas por el PMO, organizadas por tipo:
`adrs/`, `domain/`, `architecture/`, `feature/`, `product/`, `documentation/`, `work/`

## Equipo
- **Alejandro** — Arquitectura, agente PMO, framework KDD
- **Miguel** — Apps Script, integración Drive-GitHub

