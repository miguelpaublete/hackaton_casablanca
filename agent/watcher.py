"""
watcher.py — Monitor automático de actas nuevas.

Vigila la carpeta /actas/ cada X minutos. Cuando detecta actas que no han
sido procesadas aún, envía un email al PMO con el listado y el link a la
interfaz Streamlit para que pueda generar y validar las specs.

Uso:
    python watcher.py                  # intervalo por defecto: 30 min
    python watcher.py --interval 10    # cada 10 minutos
    python watcher.py --once           # ejecutar una sola vez y salir
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import config

# ─────────────────────────────────────────────────────────────
# RUTAS
# ─────────────────────────────────────────────────────────────

ACTAS_DIR = config.PROJECT_ROOT.parent / "actas"
MANIFEST_PATH = config.OUTPUT_DIR / "_processed_actas.json"
VALID_SUFFIXES = (".txt", ".md", ".pdf", ".docx")

# ─────────────────────────────────────────────────────────────
# MANIFEST — qué actas ya se notificaron/procesaron
# ─────────────────────────────────────────────────────────────

def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {"processed": {}, "notified": {}}


def save_manifest(manifest: dict):
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def mark_as_notified(acta_rel: str, manifest: dict):
    manifest.setdefault("notified", {})[acta_rel] = datetime.now().isoformat()
    save_manifest(manifest)


# ─────────────────────────────────────────────────────────────
# ESCANEO DE ACTAS
# ─────────────────────────────────────────────────────────────

def scan_new_actas() -> dict[str, list[Path]]:
    """
    Devuelve un dict {proyecto: [actas_nuevas]} con actas que:
    - son ficheros válidos (.txt, .md, .pdf, .docx)
    - NO son ficheros .converted.txt de cache
    - NO han sido procesadas ni notificadas aún
    """
    manifest = load_manifest()
    already_handled = set(manifest.get("processed", {}).keys()) | set(manifest.get("notified", {}).keys())

    new_actas: dict[str, list[Path]] = {}

    if not ACTAS_DIR.exists():
        return new_actas

    # Detectar proyectos (subcarpetas) y ficheros sueltos
    items = list(ACTAS_DIR.iterdir())
    subdirs = [i for i in items if i.is_dir() and not i.name.startswith(".")]
    loose_files = [i for i in items if i.is_file()]

    def _filter(files: list[Path]) -> list[Path]:
        """Filtra actas válidas y no procesadas."""
        # Ignorar .converted.txt
        files = [f for f in files if not f.name.endswith(".converted.txt")]
        # Solo extensiones válidas
        files = [f for f in files if f.suffix.lower() in VALID_SUFFIXES]
        # Ignorar README
        files = [f for f in files if f.name.lower() != "readme.md"]
        # Filtrar las ya manejadas (por nombre relativo al ACTAS_DIR)
        files = [f for f in files if str(f.relative_to(ACTAS_DIR)) not in already_handled]
        # Si hay .txt/.md para un PDF, ocultar el PDF (ya convertido)
        txt_stems = {f.stem for f in files if f.suffix.lower() in (".txt", ".md")}
        files = [
            f for f in files
            if not (f.suffix.lower() in (".pdf", ".docx") and f.stem in txt_stems)
        ]
        return files

    for subdir in subdirs:
        actas = _filter(list(subdir.rglob("*")))
        if actas:
            new_actas[subdir.name] = actas

    loose = _filter(loose_files)
    if loose:
        new_actas["General"] = loose

    return new_actas


# ─────────────────────────────────────────────────────────────
# EMAIL DE NOTIFICACIÓN
# ─────────────────────────────────────────────────────────────

def build_watcher_email(new_actas: dict[str, list[Path]], app_url: str) -> tuple[str, str]:
    """Construye asunto y cuerpo HTML del email de aviso."""
    total = sum(len(v) for v in new_actas.values())
    subject = f"📋 KDD Copilot: {total} acta(s) nueva(s) pendientes de procesar"

    projects_html = ""
    for project, actas in new_actas.items():
        acta_rows = "".join(
            f"<li style='padding:4px 0;'>📄 {a.name}</li>"
            for a in actas
        )
        projects_html += f"""
        <div style="margin-bottom:16px;">
            <strong style="color:#004481;">📁 {project}</strong>
            <ul style="margin:6px 0; padding-left:20px; color:#333; line-height:1.7;">
                {acta_rows}
            </ul>
        </div>"""

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""
    <html>
    <body style="font-family:'Segoe UI',Arial,sans-serif; color:#333; max-width:700px; margin:0 auto;">

        <div style="background:linear-gradient(135deg,#004481,#0066cc); padding:24px 30px; border-radius:8px 8px 0 0;">
            <h1 style="color:white; margin:0; font-size:22px;">📋 KDD PMO Copilot</h1>
            <p style="color:#cce0ff; margin:8px 0 0 0; font-size:14px;">Nuevas actas detectadas — acción requerida</p>
        </div>

        <div style="background:#fff; padding:24px 30px; border:1px solid #e0e0e0; border-top:none;">

            <p style="font-size:16px;">Hola,</p>
            <p>Se han detectado <strong>{total} acta(s) nueva(s)</strong> en el repositorio que aún no tienen specs generadas:</p>

            <div style="background:#f8f9fa; padding:16px 20px; border-radius:6px; border-left:4px solid #004481; margin:20px 0;">
                {projects_html}
            </div>

            <p style="color:#555;">Por favor, accede a la interfaz KDD Copilot para:</p>
            <ol style="line-height:1.9; color:#333;">
                <li>Seleccionar el proyecto y el acta</li>
                <li>Pulsar <strong>"⚡ Generar Specs"</strong></li>
                <li>Revisar y editar los artefactos generados</li>
                <li>Pulsar <strong>"✅ Validar y Commitear Specs"</strong></li>
            </ol>

            <div style="text-align:center; margin:30px 0;">
                <a href="{app_url}"
                   style="display:inline-block; background:#004481; color:white;
                          padding:14px 32px; text-decoration:none; border-radius:6px;
                          font-weight:bold; font-size:16px;">
                    🚀 Abrir KDD Copilot
                </a>
                <p style="color:#999; font-size:12px; margin-top:10px;">
                    <a href="{app_url}" style="color:#0066cc;">{app_url}</a>
                </p>
            </div>
        </div>

        <div style="background:#f5f5f5; padding:16px 30px; border-radius:0 0 8px 8px;
                    border:1px solid #e0e0e0; border-top:none; text-align:center;">
            <p style="font-size:11px; color:#999; margin:0;">
                KDD PMO Copilot — Monitorización automática — {now}
            </p>
        </div>

    </body>
    </html>
    """
    return subject, html


def send_watcher_email(new_actas: dict[str, list[Path]], app_url: str) -> bool:
    """Envía el email de aviso via Mailjet o SMTP. Retorna True si OK."""
    import requests as req_lib
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import os

    recipient = config.PMO_EMAIL
    if not recipient:
        print("  ⚠️ PMO_EMAIL no configurado. Saltando envío.")
        return False

    subject, html_body = build_watcher_email(new_actas, app_url)

    # ── Mailjet ──
    mailjet_key = getattr(config, "MAILJET_API_KEY", "") or os.environ.get("MAILJET_API_KEY", "")
    mailjet_secret = getattr(config, "MAILJET_API_SECRET", "") or os.environ.get("MAILJET_API_SECRET", "")
    sender_email = getattr(config, "SENDER_EMAIL", "") or os.environ.get("SENDER_EMAIL", "")
    proxy_url = getattr(config, "HTTP_PROXY", "") or os.environ.get("HTTP_PROXY", "")

    if mailjet_key and mailjet_secret:
        proxies = {"https": proxy_url, "http": proxy_url} if proxy_url else None
        payload = {
            "Messages": [{
                "From": {"Email": sender_email or recipient, "Name": "KDD PMO Copilot"},
                "To": [{"Email": recipient}],
                "Subject": subject,
                "HTMLPart": html_body,
            }]
        }
        resp = req_lib.post(
            "https://api.mailjet.com/v3.1/send",
            json=payload,
            auth=(mailjet_key, mailjet_secret),
            proxies=proxies,
            timeout=30,
        )
        print(f"  📡 Mailjet HTTP {resp.status_code}")
        try:
            data = resp.json()
            print(f"  📡 Mailjet response: {json.dumps(data, indent=2, ensure_ascii=False)[:1500]}")
        except Exception:
            print(f"  📡 Mailjet raw: {resp.text[:1500]}")
            data = {}

        if resp.status_code == 200:
            # Verificar que cada mensaje fue aceptado
            messages = data.get("Messages", [])
            all_ok = all(m.get("Status") == "success" for m in messages)
            if all_ok:
                print(f"  📧 Email enviado a {recipient} (Mailjet)")
                return True
            else:
                print(f"  ❌ Mailjet aceptó la petición pero rechazó el envío. Detalle arriba.")
                return False
        else:
            print(f"  ❌ Mailjet error {resp.status_code}: {resp.text}")
            return False

    # ── SMTP fallback ──
    smtp_user = config.SMTP_USER
    smtp_pass = config.SMTP_PASSWORD
    if smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = smtp_user
            msg["To"] = recipient
            msg.attach(MIMEText(html_body, "html"))
            with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            print(f"  📧 Email enviado a {recipient} (SMTP)")
            return True
        except Exception as e:
            print(f"  ❌ SMTP error: {e}")
            return False

    print("  ❌ No hay credenciales de email configuradas (Mailjet o SMTP).")
    return False


# ─────────────────────────────────────────────────────────────
# CICLO PRINCIPAL
# ─────────────────────────────────────────────────────────────

def check_and_notify(app_url: str) -> int:
    """
    Escanea actas nuevas, envía email si hay y marca como notificadas.
    Retorna el número de actas nuevas encontradas.
    """
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🔍 Escaneando {ACTAS_DIR} ...")
    new_actas = scan_new_actas()

    if not new_actas:
        print("  ✅ Sin actas nuevas.")
        return 0

    total = sum(len(v) for v in new_actas.items())
    for project, actas in new_actas.items():
        print(f"  📁 {project}: {len(actas)} acta(s) nueva(s)")
        for a in actas:
            print(f"      - {a.name}")

    print(f"  → Enviando notificación para {sum(len(v) for v in new_actas.values())} actas...")
    ok = send_watcher_email(new_actas, app_url)

    if ok:
        manifest = load_manifest()
        for actas in new_actas.values():
            for acta in actas:
                rel = str(acta.relative_to(ACTAS_DIR))
                mark_as_notified(rel, manifest)
        print("  ✅ Actas marcadas como notificadas.")

    return sum(len(v) for v in new_actas.values())


def run_watcher(interval_minutes: int = 30, run_once: bool = False, app_url: str = "http://localhost:8501"):
    print("=" * 60)
    print("  🤖 KDD PMO Copilot — Watcher de Actas")
    print("=" * 60)
    print(f"  Carpeta vigilada : {ACTAS_DIR}")
    print(f"  Notificando a    : {config.PMO_EMAIL or '⚠️ PMO_EMAIL no configurado'}")
    print(f"  Link Streamlit   : {app_url}")
    if not run_once:
        print(f"  Intervalo        : {interval_minutes} minutos")
    print(f"  Iniciado         : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    while True:
        check_and_notify(app_url)

        if run_once:
            print("\n✅ Ejecución única completada.")
            break

        print(f"\n  💤 Próxima revisión en {interval_minutes} min. (Ctrl+C para parar)")
        time.sleep(interval_minutes * 60)


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KDD PMO Copilot — Monitor de actas nuevas")
    parser.add_argument(
        "--interval", type=int, default=30,
        help="Minutos entre comprobaciones (default: 30)"
    )
    parser.add_argument(
        "--once", action="store_true",
        help="Ejecutar una sola vez y salir"
    )
    parser.add_argument(
        "--app-url", default=f"http://localhost:{getattr(config, 'STREAMLIT_PORT', 8501)}",
        help="URL de la interfaz Streamlit"
    )
    args = parser.parse_args()

    run_watcher(
        interval_minutes=args.interval,
        run_once=args.once,
        app_url=args.app_url,
    )


