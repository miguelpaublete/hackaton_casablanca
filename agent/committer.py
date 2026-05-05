"""
committer.py — Commit automático de artefactos validados a GitHub.

Usa git local (subprocess) para commitear y pushear, evitando problemas
de proxy y permisos de Fine-grained PATs con la REST API.

Uso:
    from committer import commit_artifacts
    paths = commit_artifacts(artifacts_list)
"""

import subprocess
from datetime import datetime
from pathlib import Path

import config
from extractor import Artifact


# ─────────────────────────────────────────────────────────────
# RUTAS
# ─────────────────────────────────────────────────────────────

REPO_ROOT = config.PROJECT_ROOT.parent  # raíz del repo git
SPECS_DIR = REPO_ROOT / "specs"


# ─────────────────────────────────────────────────────────────
# MAPEO DE TIPO → CARPETA
# ─────────────────────────────────────────────────────────────

FOLDER_MAP = {
    "adr": "adrs",
    "dom": "domain",
    "wrk-task": "work",
    "spec": "domain",
    "loaded": "",
}


def _get_subfolder(artifact: Artifact) -> str:
    """Determina la subcarpeta dentro de specs/ para un artefacto."""
    art_id = artifact.id.upper()
    if art_id.startswith("ADR"):
        return "adrs"
    elif art_id.startswith("DOM"):
        return "domain"
    elif art_id.startswith("WRK-TASK") or art_id.startswith("WRK-PLAN") or art_id.startswith("WRK-SPEC"):
        return "work"
    elif art_id.startswith("ARCH"):
        return "architecture"
    elif art_id.startswith("FEAT"):
        return "feature"
    elif art_id.startswith("PROD"):
        return "product"
    elif art_id.startswith("DOC"):
        return "documentation"
    return FOLDER_MAP.get(artifact.type, "")


def _run_git(*args, cwd=None, use_proxy=False):
    """Ejecuta un comando git y devuelve stdout.

    Si use_proxy=True y config.HTTP_PROXY está definido, inyecta
    -c http.proxy=... -c https.proxy=... para atravesar el proxy corporativo.
    """
    cmd = ["git"]
    if use_proxy and config.HTTP_PROXY:
        cmd += [
            "-c", f"http.proxy={config.HTTP_PROXY}",
            "-c", f"https.proxy={config.HTTP_PROXY}",
        ]
    cmd += list(args)
    result = subprocess.run(
        cmd,
        cwd=cwd or str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        if "user.email" in stderr or "Please tell me who you are" in stderr:
            raise RuntimeError(
                f"git {' '.join(args)} falló: Git no tiene usuario configurado.\n"
                f"Ejecuta:\n  git config user.email 'tu@email.com'\n  git config user.name 'Tu Nombre'\n\n{stderr}"
            )
        raise RuntimeError(f"git {' '.join(args)} falló:\n{stderr or stdout or '(sin salida — comprueba que hay cambios para commitear)'}")
    return result.stdout.strip()


# ─────────────────────────────────────────────────────────────
# COMMIT ARTEFACTOS
# ─────────────────────────────────────────────────────────────

def commit_artifacts(
    artifacts: list[Artifact],
    branch: str = "main",
    commit_prefix: str = "KDD-Copilot",
    source_transcript: str = "",
    project: str = "",
) -> list[str]:
    """
    Escribe los artefactos en specs/, hace git add + commit + push.

    Returns:
        Lista de paths relativos commiteados.
    """
    if not artifacts:
        return []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    committed_paths = []

    for artifact in artifacts:
        subfolder = _get_subfolder(artifact)
        if project:
            target_dir = SPECS_DIR / project / subfolder
        else:
            target_dir = SPECS_DIR / subfolder

        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / artifact.filename
        target_path.write_text(artifact.content, encoding="utf-8")

        rel_path = str(target_path.relative_to(REPO_ROOT)).replace("\\", "/")
        committed_paths.append(rel_path)
        print(f"  ✅ Escrito: {rel_path}")

    # Git add + commit
    for p in committed_paths:
        _run_git("add", p)

    source_line = f"\nSource: {source_transcript}" if source_transcript else ""
    ids = ", ".join(a.id for a in artifacts)
    commit_msg = (
        f"[{commit_prefix}] {ids}\n\n"
        f"Auto-generated from meeting transcript.{source_line}\n"
        f"Validated by PMO at {timestamp}."
    )

    _run_git("commit", "-m", commit_msg)
    print("  📦 Commit creado")

    # Push — inyectar token en la URL para autenticar y proxy corporativo
    try:
        repo_url = f"https://x-access-token:{config.GITHUB_COMMIT_TOKEN}@github.com/{config.GITHUB_REPO}.git"
        _run_git("push", repo_url, branch, use_proxy=True)
        print("  🚀 Push completado")
    except RuntimeError as e:
        print(f"  ⚠️ Push falló (commit guardado localmente): {e}")

    return committed_paths


# ─────────────────────────────────────────────────────────────
# CLI PARA PRUEBAS
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    import re

    parser = argparse.ArgumentParser(description="Commit artefactos .md a GitHub.")
    parser.add_argument("files", nargs="+", help="Ficheros .md a commitear.")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--project", default="")

    args = parser.parse_args()

    artifacts = []
    for fpath in args.files:
        p = Path(fpath)
        content = p.read_text(encoding="utf-8")
        id_match = re.search(r"^id:\s*(.+)$", content, re.MULTILINE)
        art_id = id_match.group(1).strip() if id_match else p.stem
        artifacts.append(Artifact(
            id=art_id, type="loaded", title=p.stem,
            filename=p.name, content=content,
        ))

    paths = commit_artifacts(artifacts, branch=args.branch, project=args.project)
    print(f"\n✅ {len(paths)} artefactos commiteados.")


