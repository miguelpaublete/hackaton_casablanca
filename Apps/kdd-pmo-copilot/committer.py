"""
committer.py — Paso 7: Commit automático de artefactos validados a GitHub.

Usa PyGithub para crear/actualizar ficheros .md en la carpeta /specs
del repositorio configurado.

Uso:
    from committer import commit_artifacts
    paths = commit_artifacts(artifacts_list)
"""

from github import Github, GithubException
from datetime import datetime

import config
from extractor import Artifact


# ─────────────────────────────────────────────────────────────
# MAPEO DE TIPO → CARPETA EN EL REPO
# ─────────────────────────────────────────────────────────────

FOLDER_MAP = {
    "adr": "specs/adrs",
    "dom": "specs/domain",
    "wrk-task": "specs/work",
    "spec": "specs/domain",
    "loaded": "specs",
}


def _get_target_path(artifact: Artifact) -> str:
    """Determina la ruta dentro del repo para un artefacto."""
    folder = FOLDER_MAP.get(artifact.type, "specs")

    # Intentar inferir desde el ID
    art_id = artifact.id.upper()
    if art_id.startswith("ADR"):
        folder = "specs/adrs"
    elif art_id.startswith("DOM"):
        folder = "specs/domain"
    elif art_id.startswith("WRK-TASK"):
        folder = "specs/work"
    elif art_id.startswith("WRK-PLAN"):
        folder = "specs/work"
    elif art_id.startswith("WRK-SPEC"):
        folder = "specs/work"
    elif art_id.startswith("ARCH"):
        folder = "specs/architecture"
    elif art_id.startswith("FEAT"):
        folder = "specs/feature"
    elif art_id.startswith("PROD"):
        folder = "specs/product"
    elif art_id.startswith("DOC"):
        folder = "specs/documentation"

    return f"{folder}/{artifact.filename}"


# ─────────────────────────────────────────────────────────────
# COMMIT A GITHUB
# ─────────────────────────────────────────────────────────────

def commit_artifacts(
    artifacts: list[Artifact],
    branch: str = "main",
    commit_prefix: str = "KDD-Copilot",
    source_transcript: str = "",
) -> list[str]:
    """
    Crea o actualiza los artefactos en el repositorio GitHub.

    Args:
        artifacts: Lista de artefactos validados.
        branch: Rama destino.
        commit_prefix: Prefijo del mensaje de commit.
        source_transcript: Nombre del acta origen (trazabilidad).

    Returns:
        Lista de paths commiteados en el repo.
    """
    if not config.GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN no configurado. Revisa tu .env")
    if not config.GITHUB_REPO:
        raise ValueError("GITHUB_REPO no configurado. Revisa tu .env")

    gh = Github(config.GITHUB_TOKEN)
    repo = gh.get_repo(config.GITHUB_REPO)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    committed_paths = []

    for artifact in artifacts:
        target_path = _get_target_path(artifact)

        source_line = f"\nSource transcript: {source_transcript}" if source_transcript else ""
        commit_msg = (
            f"[{commit_prefix}] {artifact.id}: {artifact.title}\n\n"
            f"Auto-generated from meeting transcript.{source_line}\n"
            f"Validated by PMO at {timestamp}."
        )

        try:
            # Intentar obtener fichero existente (para update)
            existing = repo.get_contents(target_path, ref=branch)
            repo.update_file(
                path=target_path,
                message=commit_msg,
                content=artifact.content,
                sha=existing.sha,
                branch=branch,
            )
            print(f"  🔄 Actualizado: {target_path}")
        except GithubException as e:
            if e.status == 404:
                # Fichero no existe → crear
                repo.create_file(
                    path=target_path,
                    message=commit_msg,
                    content=artifact.content,
                    branch=branch,
                )
                print(f"  ✅ Creado: {target_path}")
            else:
                raise

        committed_paths.append(target_path)

    return committed_paths


# ─────────────────────────────────────────────────────────────
# CLI PARA PRUEBAS
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    import re

    parser = argparse.ArgumentParser(
        description="Commit artefactos .md a GitHub."
    )
    parser.add_argument(
        "files", nargs="+",
        help="Ficheros .md a commitear.",
    )
    parser.add_argument(
        "--branch", default="main",
        help="Rama destino (default: main).",
    )

    args = parser.parse_args()

    artifacts = []
    for fpath in args.files:
        p = Path(fpath)
        content = p.read_text(encoding="utf-8")
        # Extraer ID del frontmatter
        id_match = re.search(r"^id:\s*(.+)$", content, re.MULTILINE)
        art_id = id_match.group(1).strip() if id_match else p.stem
        artifacts.append(Artifact(
            id=art_id,
            type="loaded",
            title=p.stem,
            filename=p.name,
            content=content,
        ))

    paths = commit_artifacts(artifacts, branch=args.branch)
    print(f"\n✅ {len(paths)} artefactos commiteados.")


