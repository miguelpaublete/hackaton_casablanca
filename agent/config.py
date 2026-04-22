"""
config.py — Configuración centralizada del proyecto KDD PMO Copilot.

Lee variables de entorno (desde .env en local o GitHub Secrets en CI).
Nunca contiene credenciales hardcodeadas.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env solo si existe (en CI usamos GitHub Secrets)
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    load_dotenv(_env_path)

# ── Google Cloud / Vertex AI ──────────────────────────────
GCP_PROJECT_ID: str = os.environ.get("GCP_PROJECT_ID", "")
GCP_LOCATION: str = os.environ.get("GCP_LOCATION", "europe-west1")
VERTEX_MODEL: str = os.environ.get("VERTEX_MODEL", "gemini-2.0-flash")

# ── Google Drive ──────────────────────────────────────────
DRIVE_FOLDER_ID: str = os.environ.get("DRIVE_FOLDER_ID", "")

# ── GitHub ────────────────────────────────────────────────
GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO: str = os.environ.get("GITHUB_REPO", "")

# ── SMTP ──────────────────────────────────────────────────
SMTP_HOST: str = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT: int = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER: str = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD: str = os.environ.get("SMTP_PASSWORD", "")
PMO_EMAIL: str = os.environ.get("PMO_EMAIL", "")

# ── Mailjet (HTTP API — funciona detrás de proxy) ────────
MAILJET_API_KEY: str = os.environ.get("MAILJET_API_KEY", "")
MAILJET_API_SECRET: str = os.environ.get("MAILJET_API_SECRET", "")
SENDER_EMAIL: str = os.environ.get("SENDER_EMAIL", "")

# ── Proxy corporativo ────────────────────────────────────
HTTP_PROXY: str = os.environ.get("HTTP_PROXY", "")

# ── Streamlit ─────────────────────────────────────────────
STREAMLIT_PORT: int = int(os.environ.get("STREAMLIT_PORT", "8501"))

# ── Paths ─────────────────────────────────────────────────
PROJECT_ROOT: Path = Path(__file__).parent
PROMPTS_DIR: Path = PROJECT_ROOT / "prompts"
OUTPUT_DIR: Path = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
