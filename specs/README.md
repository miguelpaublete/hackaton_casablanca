# Specs — Artefactos KDD validados

Esta carpeta contiene los artefactos de conocimiento validados por el PMO, generados automáticamente desde transcripciones de reuniones y revisados antes de su commit.

## Estructura

```
specs/
├── adrs/            # Architecture Decision Records (ADR-NNN)
├── architecture/    # Architecture Specs (ARCH-NNN)
├── domain/          # Domain Specs (DOM-AREA-NNN)
├── feature/         # Feature Specs (FEAT-MODULE-NNN)
├── product/         # Product Specs (PROD-JOURNEY-NNN)
├── documentation/   # Documentation Specs (DOC-TYPE-NNN)
└── work/            # Work Artifacts (WRK-SPEC/PLAN/TASK-NNN)
```

## Ciclo de vida

1. **Generación**: `extractor.py` + Vertex AI (Gemini) a partir de una transcripción
2. **Validación**: PMO revisa y edita en Streamlit (`app.py`)
3. **Commit**: `committer.py` commitea aquí con trazabilidad al acta original
4. **Consumo**: GitHub Copilot `@workspace` o `spec-graph` CLI

