"""
notifier.py — Paso 5: Notificación por email al PMO.

Envía un email informando de que hay artefactos KDD pendientes de validar,
con un resumen y un link a la interfaz Streamlit.

Uso:
    from notifier import send_notification
    send_notification(extraction_result)
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

import config
from extractor import ExtractionResult


def build_email_body(result: ExtractionResult, app_url: str) -> str:
    """Construye el cuerpo HTML del email."""
    artifact_rows = ""
    for a in result.artifacts:
        icon = {"adr": "🏗️", "dom": "📖", "wrk-task": "✅"}.get(a.type, "📄")
        artifact_rows += f"""
        <tr>
            <td style="padding:8px; border:1px solid #ddd;">{icon} {a.id}</td>
            <td style="padding:8px; border:1px solid #ddd;">{a.type.upper()}</td>
            <td style="padding:8px; border:1px solid #ddd;">{a.title}</td>
        </tr>"""

    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>📋 KDD PMO Copilot — Nuevos artefactos para validar</h2>
        <p>Se ha procesado una transcripción de reunión y se han generado
        <strong>{len(result.artifacts)} artefactos KDD</strong> pendientes de revisión.</p>

        <h3>Resumen de la reunión</h3>
        <p style="background:#f5f5f5; padding:12px; border-radius:6px;">
            {result.summary}
        </p>

        <h3>Artefactos generados</h3>
        <table style="border-collapse:collapse; width:100%;">
            <thead>
                <tr style="background:#004481; color:white;">
                    <th style="padding:8px; border:1px solid #ddd;">ID</th>
                    <th style="padding:8px; border:1px solid #ddd;">Tipo</th>
                    <th style="padding:8px; border:1px solid #ddd;">Título</th>
                </tr>
            </thead>
            <tbody>
                {artifact_rows}
            </tbody>
        </table>

        <br>
        <a href="{app_url}"
           style="display:inline-block; background:#004481; color:white;
                  padding:12px 24px; text-decoration:none; border-radius:6px;
                  font-weight:bold;">
            🔍 Revisar y Validar en KDD Copilot
        </a>

        <hr style="margin-top:30px;">
        <p style="font-size:12px; color:#999;">
            Generado automáticamente por KDD PMO Copilot —
            {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </p>
    </body>
    </html>
    """


def send_notification(
    result: ExtractionResult,
    recipient: str | None = None,
    app_url: str | None = None,
) -> None:
    """
    Envía email de notificación al PMO.

    Args:
        result: Resultado de la extracción.
        recipient: Email destino (por defecto: PMO_EMAIL del config).
        app_url: URL de la app Streamlit.
    """
    recipient = recipient or config.PMO_EMAIL
    if not recipient:
        raise ValueError("PMO_EMAIL no configurado. Revisa tu .env")

    if app_url is None:
        port = config.STREAMLIT_PORT if hasattr(config, "STREAMLIT_PORT") else 8501
        app_url = f"http://localhost:{port}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📋 KDD Copilot: {len(result.artifacts)} artefactos pendientes de validación"
    msg["From"] = config.SMTP_USER
    msg["To"] = recipient

    html_body = build_email_body(result, app_url)
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.send_message(msg)

    print(f"  📧 Email enviado a {recipient}")


# ─────────────────────────────────────────────────────────────
# CLI PARA PRUEBAS
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Test: generar el HTML sin enviar
    test_result = ExtractionResult(
        summary="Reunión de prueba para verificar el formato del email.",
        artifacts=[],
    )
    html = build_email_body(test_result, "http://localhost:8501")
    output_path = config.OUTPUT_DIR / "_email_preview.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"✅ Preview del email guardado en: {output_path}")

