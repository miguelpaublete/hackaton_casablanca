# Actas de Reuniones

Carpeta de entrada del agente PMO Copilot. Aquí se depositan las transcripciones de reuniones para su procesamiento.

## Estructura

Cada proyecto tiene su propia subcarpeta:

```
actas/
├── carbon-markets/          → Proyecto Carbon Markets
│   └── *.txt / *.pdf / *.docx
├── pagos-internacionales/   → Proyecto Pagos Internacionales (SWIFT)
│   └── *.txt / *.pdf / *.docx
└── <nuevo-proyecto>/        → Añadir una carpeta por cada nuevo proyecto
    └── *.txt / *.pdf / *.docx
```

## Convención de nombres de archivos

```
YYYY-MM-DD_descripcion-breve.txt
```

Ejemplo: `2026-04-18_kick-off-swift-mt103.txt`

## Cómo añadir un nuevo proyecto

1. Crear una carpeta con el slug del proyecto (minúsculas, separado por guiones)
2. Depositar las transcripciones dentro de esa carpeta
3. El agente PMO las detectará automáticamente al procesar

## Formatos soportados

- `.txt` — Transcripciones en texto plano (recomendado)
- `.pdf` — PDFs exportados desde Google Meet / Docs
- `.docx` — Documentos Word
