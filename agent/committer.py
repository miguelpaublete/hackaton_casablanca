"""
committer.py — Commit automático de artefactos validados a GitHub.

Usa la API REST de GitHub directamente (con requests) para soportar
el proxy corporativo. Crea/actualiza ficheros .md en /specs/.

Uso:
    from committer import commit_artifacts
    paths = commit_artifacts(artifacts_list)
"""

import base64
import requests
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


def _get_target_path(artifact: Artifact, project: str = "") -> str:
    """Determina la ruta dentro del repo para un artefacto."""
    folder = FOLDER_MAP.get(artifact.type, "specs")

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

    if project:
        folder = folder.replace("specs/", f"specs/{project}/", 1)

    return f"{folder}/{artifact.filename}"


# ─────────────────────────────────────────────────────────────
# GITHUB REST API (con proxy)
# ─────────────────────────────────────────────────────────────

def _github_session() -> requests.Session:
    """Crea una sesión requests con token y proxy configurados."""
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    if config.HTTP_PROXY:
        session.proxies = {"https": config.HTTP_PROXY, "http": config.HTTP_PROXY}
    return session


def _get_file_sha(session: requests.Session, repo: str, path: str, branch: str) -> str | None:
    """Obtiene el SHA de un fichero existente (None si no existe)."""
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    r = session.get(url, params={"ref": branch}, timeout=30)
    if r.status_code == 200:
        return r.json().get("sha")
    return None


def _create_or_update_file(
    session: requests.Session,
    repo: str,
    path: str,
    content: str,
    message: str,
    branch: str,
    sha: str | None = None,
) -> dict:
    """Crea o actualiza un fichero en el repo vía REST API."""
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha

    r = session.put(url, json=payload, timeout=30)
    if r.status_code not in (200, 201):
        raise RuntimeError(
            f"GitHub API error {r.status_code} para {path}: {r.text[:300]}"
        )
    return r.json()


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
    Crea o actualiza los artefactos en el repositorio GitHub.

    Returns:
        Lista de paths commiteados en el repo.
    """
    if not config.GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN no configurado. Revisa tu .env")
    if not config.GITHUB_REPO:
        raise ValueError("GITHUB_REPO no configurado. Revisa tu .env")

    session = _github_session()
    repo = config.GITHUB_REPO
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    committed_paths = []

    for artifact in artifacts:
        target_path = _get_target_path(artifact, project=project)

        source_line = f"\nSource transcript: {source_transcript}" if source_transcript else ""
        commit_msg = (
            f"[{commit_prefix}] {artifact.id}: {artifact.title}\n\n"
            f"Auto-generated from meeting transcript.{source_line}\n"
            f"Validated by PMO at {timestamp}."
        )

        # Comprobar si el fichero ya existe
        sha = _get_file_sha(session, repo, target_path, branch)
        action = "Actualizado" if sha else "Creado"

        _create_or_update_file(
            session, repo, target_path,
            artifact.content, commit_msg, branch, sha,
        )
        print(f"  {'🔄' if sha else '✅'} {action}: {target_path}")
        committed_paths.append(target_path)

    return committed_paths


# ─────────────────────────────────────────────────────────────
# CLI PARA PRUEBAS
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    import re
    from pathlib import Path

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

