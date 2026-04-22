"""
notifier.py — Paso 5: Notificación por email al PMO.

Envía un email informando de que hay artefactos KDD pendientes de validar,
con un resumen y un link a la interfaz Streamlit.

Uso:
    from notifier import send_notification
    send_notification(extraction_result)
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

import config
from extractor import ExtractionResult


def build_email_body(result: ExtractionResult, app_url: str) -> str:
    """Construye el cuerpo HTML del email."""
    # Contar por tipo
    adrs = [a for a in result.artifacts if a.type == "adr"]
    doms = [a for a in result.artifacts if a.type == "dom"]
    tasks = [a for a in result.artifacts if a.type == "wrk-task"]

    artifact_rows = ""
    for a in result.artifacts:
        icon = {"adr": "🏗️", "dom": "📖", "wrk-task": "✅"}.get(a.type, "📄")
        type_label = {"adr": "Decisión Arquitectura", "dom": "Regla de Negocio", "wrk-task": "Tarea"}.get(a.type, a.type.upper())
        artifact_rows += f"""
        <tr>
            <td style="padding:10px 12px; border-bottom:1px solid #eee;">{icon} <strong>{a.id}</strong></td>
            <td style="padding:10px 12px; border-bottom:1px solid #eee;">{type_label}</td>
            <td style="padding:10px 12px; border-bottom:1px solid #eee;">{a.title}</td>
        </tr>"""

    source = ""
    if result.source_transcript:
        source = f"<p style='color:#666; font-size:13px;'>📎 Transcripción origen: <code>{result.source_transcript}</code></p>"

    return f"""
    <html>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; color: #333; max-width: 700px; margin: 0 auto;">

        <!-- Header -->
        <div style="background: linear-gradient(135deg, #004481, #0066cc); padding: 24px 30px; border-radius: 8px 8px 0 0;">
            <h1 style="color: white; margin: 0; font-size: 22px;">📋 KDD PMO Copilot</h1>
            <p style="color: #cce0ff; margin: 8px 0 0 0; font-size: 14px;">Nuevos artefactos pendientes de validación</p>
        </div>

        <!-- Body -->
        <div style="background: #fff; padding: 24px 30px; border: 1px solid #e0e0e0; border-top: none;">

            <!-- Resumen rápido -->
            <div style="display: flex; gap: 12px; margin-bottom: 20px;">
                <div style="background:#e8f4fd; padding:12px 16px; border-radius:6px; text-align:center; flex:1;">
                    <div style="font-size:24px; font-weight:bold; color:#004481;">{len(result.artifacts)}</div>
                    <div style="font-size:12px; color:#666;">Total</div>
                </div>
            </div>

            <table style="width:100%; margin-bottom:8px;">
                <tr>
                    <td style="background:#fff3cd; padding:8px 12px; border-radius:4px; text-align:center; width:33%;">
                        🏗️ <strong>{len(adrs)}</strong> ADR
                    </td>
                    <td style="background:#d4edda; padding:8px 12px; border-radius:4px; text-align:center; width:33%;">
                        📖 <strong>{len(doms)}</strong> DOM
                    </td>
                    <td style="background:#cce5ff; padding:8px 12px; border-radius:4px; text-align:center; width:33%;">
                        ✅ <strong>{len(tasks)}</strong> Tareas
                    </td>
                </tr>
            </table>

            <!-- Resumen reunión -->
            <h3 style="color:#004481; border-bottom:2px solid #004481; padding-bottom:6px;">
                Resumen de la reunión
            </h3>
            <p style="background:#f8f9fa; padding:14px; border-radius:6px; border-left:4px solid #004481; line-height:1.6;">
                {result.summary}
            </p>
            {source}

            <!-- Tabla de artefactos -->
            <h3 style="color:#004481; border-bottom:2px solid #004481; padding-bottom:6px;">
                Artefactos generados
            </h3>
            <table style="border-collapse:collapse; width:100%; margin-bottom:24px;">
                <thead>
                    <tr style="background:#004481; color:white;">
                        <th style="padding:10px 12px; text-align:left; border-radius:4px 0 0 0;">ID</th>
                        <th style="padding:10px 12px; text-align:left;">Tipo</th>
                        <th style="padding:10px 12px; text-align:left; border-radius:0 4px 0 0;">Título</th>
                    </tr>
                </thead>
                <tbody>
                    {artifact_rows}
                </tbody>
            </table>

            <!-- Call to action -->
            <div style="text-align:center; margin: 30px 0;">
                <p style="color:#666; margin-bottom:16px;">
                    Por favor, revisa y valida los artefactos en la interfaz:
                </p>
                <a href="{app_url}"
                   style="display:inline-block; background:#004481; color:white;
                          padding:14px 32px; text-decoration:none; border-radius:6px;
                          font-weight:bold; font-size:16px; letter-spacing:0.5px;">
                    🔍 Abrir KDD Copilot para Validar
                </a>
                <p style="color:#999; font-size:12px; margin-top:12px;">
                    Link: <a href="{app_url}" style="color:#0066cc;">{app_url}</a>
                </p>
            </div>

            <!-- Instrucciones -->
            <div style="background:#f0f7ff; padding:14px; border-radius:6px; margin-top:20px;">
                <strong>📌 ¿Qué hacer?</strong>
                <ol style="margin:8px 0; padding-left:20px; line-height:1.8;">
                    <li>Abre el link de arriba</li>
                    <li>Revisa el acta original (izquierda) y los artefactos (derecha)</li>
                    <li>Edita lo que necesites directamente en la interfaz</li>
                    <li>Pulsa <strong>"✅ Validar y hacer Commit"</strong></li>
                </ol>
            </div>
        </div>

        <!-- Footer -->
        <div style="background:#f5f5f5; padding:16px 30px; border-radius:0 0 8px 8px;
                     border:1px solid #e0e0e0; border-top:none; text-align:center;">
            <p style="font-size:11px; color:#999; margin:0;">
                Generado automáticamente por KDD PMO Copilot —
                {datetime.now().strftime('%Y-%m-%d %H:%M')} —
                Knowledge-Driven Development (Nfq)
            </p>
        </div>

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

    Soporta dos modos:
    - MAILJET: Envío por HTTP API (funciona detrás de proxy corporativo)
    - SMTP: Envío directo por SMTP (necesita acceso de red al servidor)

    Args:
        result: Resultado de la extracción.
        recipient: Email destino (por defecto: PMO_EMAIL del config).
        app_url: URL de la app Streamlit.
    """
    import requests

    recipient = recipient or config.PMO_EMAIL
    if not recipient:
        raise ValueError("PMO_EMAIL no configurado. Revisa tu .env")

    if app_url is None:
        port = getattr(config, "STREAMLIT_PORT", 8501)
        app_url = f"http://localhost:{port}"

    html_body = build_email_body(result, app_url)
    subject = f"📋 KDD Copilot: {len(result.artifacts)} artefactos pendientes de validación"

    # ── Modo 1: Mailjet API (HTTP — funciona detrás de proxy) ──
    mailjet_key = getattr(config, "MAILJET_API_KEY", "") or os.environ.get("MAILJET_API_KEY", "")
    mailjet_secret = getattr(config, "MAILJET_API_SECRET", "") or os.environ.get("MAILJET_API_SECRET", "")
    sender_email = getattr(config, "SENDER_EMAIL", "") or os.environ.get("SENDER_EMAIL", "")

    if mailjet_key and mailjet_secret:
        proxy_url = os.environ.get("HTTP_PROXY", "") or os.environ.get("http_proxy", "")
        proxies = {"https": proxy_url, "http": proxy_url} if proxy_url else None

        payload = {
            "Messages": [{
                "From": {"Email": sender_email or "kdd-copilot@nfq.es", "Name": "KDD PMO Copilot"},
                "To": [{"Email": recipient}],
                "Subject": subject,
                "HTMLPart": html_body,
            }]
        }

        resp = requests.post(
            "https://api.mailjet.com/v3.1/send",
            json=payload,
            auth=(mailjet_key, mailjet_secret),
            proxies=proxies,
            timeout=30,
        )

        if resp.status_code == 200:
            print(f"  📧 Email enviado a {recipient} (via Mailjet)")
        else:
            raise RuntimeError(f"Mailjet error {resp.status_code}: {resp.text}")
        return

    # ── Modo 2: SMTP directo (fallback) ──
    smtp_user = config.SMTP_USER
    smtp_pass = config.SMTP_PASSWORD
    if smtp_user and smtp_pass:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = recipient
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        print(f"  📧 Email enviado a {recipient} (via SMTP)")
        return

    raise ValueError(
        "No hay método de envío configurado.\n"
        "Configura en .env:\n"
        "  Opción A (recomendada): MAILJET_API_KEY + MAILJET_API_SECRET + SENDER_EMAIL\n"
        "  Opción B: SMTP_USER + SMTP_PASSWORD"
    )


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

