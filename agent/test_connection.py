"""Test rápido de conexión a GitHub Models."""
from extractor import call_github_models

prompt = 'Reply ONLY with this exact JSON: {"ok": true, "message": "hola"}'
try:
    response = call_github_models(prompt)
    print("✅ CONEXIÓN OK")
    print("RESPONSE:", response[:300])
except Exception as e:
    print("❌ ERROR:", e)

