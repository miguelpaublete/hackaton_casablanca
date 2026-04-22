"""
send_test_email.py — Envía un email real de prueba al PMO.

Usa los artefactos generados por test_local.py y envía la notificación
al email configurado en .env (PMO_EMAIL).

Uso:
    python send_test_email.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import config
from test_local import MOCK_RESULT
from notifier import send_notification


def main():
    print("=" * 60)
    print("  📧 ENVÍO DE EMAIL DE PRUEBA — KDD PMO Copilot")
    print("=" * 60)

    # Validar configuración
    missing = []
    has_mailjet = config.MAILJET_API_KEY and config.MAILJET_API_SECRET
    has_smtp = config.SMTP_USER and config.SMTP_PASSWORD

    if not has_mailjet and not has_smtp:
        missing.append("MAILJET_API_KEY + MAILJET_API_SECRET (o SMTP_USER + SMTP_PASSWORD)")
    if not config.PMO_EMAIL:
        missing.append("PMO_EMAIL")

    if missing:
        print(f"\n❌ Faltan variables en .env: {', '.join(missing)}")
        return

    method = "Mailjet (HTTP)" if has_mailjet else "SMTP"
    sender = config.SENDER_EMAIL if has_mailjet else config.SMTP_USER

    print(f"\n  Método:  {method}")
    print(f"  De:      {sender}")
    print(f"  Para:    {config.PMO_EMAIL}")
    print(f"  Artefactos: {len(MOCK_RESULT.artifacts)}")

    app_url = f"http://localhost:{config.STREAMLIT_PORT}"
    print(f"  Link Streamlit: {app_url}")

    print(f"\n  Enviando...")

    try:
        send_notification(
            result=MOCK_RESULT,
            recipient=config.PMO_EMAIL,
            app_url=app_url,
        )
        print(f"\n✅ Email enviado correctamente a {config.PMO_EMAIL}")
        print(f"   Revisa tu bandeja de entrada (o spam).")
    except Exception as e:
        print(f"\n❌ Error al enviar: {e}")
        print(f"\n  Posibles causas:")
        print(f"    - App Password incorrecta")
        print(f"    - Proxy corporativo bloqueando SMTP")
        print(f"    - 2FA no activada en Gmail (necesaria para App Passwords)")


if __name__ == "__main__":
    main()



