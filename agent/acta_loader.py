"""
acta_loader.py — Lee actas en cualquier formato (TXT, MD, PDF, DOCX) y devuelve texto plano.

Cachea conversiones de PDF/DOCX a .txt en la misma carpeta para acelerar
re-lecturas y permitir inspección manual.
"""

import re
from pathlib import Path


def _clean_extracted_text(raw: str) -> str:
    """
    Limpia texto extraído de PDF que viene con una palabra por línea
    (a veces separadas por líneas vacías).
    Une todo en párrafos coherentes.
    """
    lines = raw.splitlines()
    paragraphs = []
    current = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            # Línea vacía: solo es fin de párrafo si lo acumulado
            # ya tiene suficiente contenido (>80 chars = párrafo real).
            # Si es poco texto, es solo un salto entre palabras sueltas.
            if current and len(" ".join(current)) > 80:
                paragraphs.append(" ".join(current))
                current = []
            # Si hay poco, seguimos acumulando
        else:
            current.append(stripped)

    if current:
        paragraphs.append(" ".join(current))

    # Limpiar espacios múltiples
    result = "\n\n".join(paragraphs)
    result = re.sub(r"  +", " ", result)
    return result


def _read_pdf(path: Path) -> str:
    """Extrae texto de un PDF usando pypdf y limpia el formato."""
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            return f"[ERROR: instala pypdf -> pip install pypdf]\nArchivo: {path.name}"

    try:
        reader = PdfReader(str(path))
        chunks = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if text.strip():
                chunks.append(text.strip())
        raw = "\n\n".join(chunks)
        return _clean_extracted_text(raw)
    except Exception as e:
        return f"[ERROR leyendo PDF: {e}]\nArchivo: {path.name}"


def _read_docx(path: Path) -> str:
    """Extrae texto de un .docx usando python-docx."""
    try:
        from docx import Document
    except ImportError:
        return f"[ERROR: instala python-docx -> pip install python-docx]\nArchivo: {path.name}"

    try:
        doc = Document(str(path))
        return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        return f"[ERROR leyendo DOCX: {e}]\nArchivo: {path.name}"


def read_acta(path: Path, use_cache: bool = True) -> str:
    """
    Lee el contenido de un acta como texto plano.

    Para PDFs y DOCX, cachea el resultado en `<nombre>.converted.txt`
    en la misma carpeta. Si ya existe, se reutiliza.
    """
    suffix = path.suffix.lower()

    # Texto directo
    if suffix in (".txt", ".md"):
        return path.read_text(encoding="utf-8", errors="ignore")

    # PDF / DOCX → cachear conversión a .txt
    if suffix in (".pdf", ".docx"):
        cache_path = path.with_suffix(path.suffix + ".converted.txt")
        if use_cache and cache_path.exists():
            return cache_path.read_text(encoding="utf-8", errors="ignore")

        text = _read_pdf(path) if suffix == ".pdf" else _read_docx(path)

        # Guardar cache si la conversión fue exitosa
        if text and not text.startswith("[ERROR"):
            try:
                cache_path.write_text(text, encoding="utf-8")
            except Exception:
                pass  # cache es opcional
        return text

    return f"[Formato no soportado: {suffix}]"


def convert_all_actas(actas_dir: Path) -> dict:
    """
    Recorre todos los PDF/DOCX en actas_dir (recursivo) y los convierte a .txt cacheado.
    Útil para precalentar el cache antes de lanzar la app.

    Returns:
        Dict con stats: {converted: int, skipped: int, errors: list[str]}
    """
    stats = {"converted": 0, "skipped": 0, "errors": []}

    if not actas_dir.exists():
        return stats

    for path in actas_dir.rglob("*"):
        if path.suffix.lower() not in (".pdf", ".docx"):
            continue
        if path.name.endswith(".converted.txt"):
            continue

        cache_path = path.with_suffix(path.suffix + ".converted.txt")
        if cache_path.exists():
            stats["skipped"] += 1
            continue

        text = read_acta(path, use_cache=False)
        if text.startswith("[ERROR"):
            stats["errors"].append(f"{path.name}: {text}")
        else:
            stats["converted"] += 1
            print(f"  ✅ Convertido: {path.relative_to(actas_dir)}")

    return stats


if __name__ == "__main__":
    import sys
    actas_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "actas"
    print(f"📂 Convirtiendo actas en: {actas_dir}")
    stats = convert_all_actas(actas_dir)
    print(f"\n✅ {stats['converted']} convertidas, {stats['skipped']} ya en cache")
    if stats["errors"]:
        print(f"\n❌ Errores ({len(stats['errors'])}):")
        for e in stats["errors"]:
            print(f"   - {e}")

