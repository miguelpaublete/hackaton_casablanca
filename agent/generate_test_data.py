"""
generate_test_data.py — Genera datos de prueba:
- 5 proyectos de ejemplo (prueba_1..prueba_5) con 5 actas cada uno en /actas/
- 2 planificaciones históricas de referencia en /Set-up proyecto/_historical/
"""

from pathlib import Path
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parent.parent
ACTAS_DIR = ROOT / "actas"
HIST_DIR = ROOT / "Set-up proyecto" / "_historical"


# ─────────────────────────────────────────────────────────────
# 5 PROYECTOS DE PRUEBA
# ─────────────────────────────────────────────────────────────

PROJECTS = {
    "prueba_1": {
        "title": "Migración de plataforma de pagos a Cloud GCP",
        "team": "Carlos (Arquitecto), Marta (PM), Luis (Dev Lead), Ana (DevOps)",
        "actas": [
            ("2026-02-02_kickoff", "Kickoff del proyecto", [
                "Carlos: Presento el alcance: migrar la plataforma de pagos del datacenter on-prem a GCP en 6 meses.",
                "Marta: El presupuesto aprobado es de 850k EUR. Tenemos sponsor del CIO.",
                "Luis: Primero hay que inventariar los 47 microservicios actuales y clasificarlos.",
                "Ana: Propongo usar GKE para los stateless y Cloud SQL para los datos transaccionales.",
                "Decisión: Se aprueba arquitectura objetivo basada en GKE + Cloud SQL + Pub/Sub.",
                "Tarea: Carlos preparará el ADR de selección cloud antes del próximo viernes.",
                "Tarea: Luis hará el inventario de servicios con tags de criticidad.",
                "Riesgo identificado: Compliance PCI-DSS en cloud requiere validación con seguridad.",
            ]),
            ("2026-02-09_arquitectura", "Definición de arquitectura objetivo", [
                "Carlos: He preparado el ADR-001 sobre la elección de GCP frente a AWS y Azure.",
                "Luis: El inventario muestra 47 servicios: 32 stateless, 12 con estado, 3 batch.",
                "Marta: ¿Qué servicios entran en la primera ola de migración?",
                "Carlos: Propongo empezar por los 5 menos críticos para validar el patrón de despliegue.",
                "Decisión: Se aprueba el plan de olas. Ola 1 en marzo, ola 2 en mayo, ola 3 en junio.",
                "Ana: Necesito que seguridad apruebe la VPC compartida antes de marzo.",
                "Acción: Marta agendará reunión con CISO para semana del 16/02.",
                "Regla de negocio: Toda transacción debe seguir cifrada en tránsito y en reposo (PCI-DSS).",
            ]),
            ("2026-02-16_seguridad", "Revisión de seguridad y compliance", [
                "Marta: Tenemos hoy a David del equipo de seguridad y a la oficina de cumplimiento.",
                "David: La VPC compartida está aprobada con condiciones. Necesitamos VPC Service Controls.",
                "Carlos: Implementaremos VPC-SC alrededor de los buckets que contengan datos PCI.",
                "Compliance: Recordamos que el log de auditoría debe retenerse 7 años en Cloud Storage clase Archive.",
                "Decisión: Se adopta CMEK (Customer Managed Encryption Keys) para todos los datos sensibles.",
                "Riesgo: Si no llega aprobación de la AEPD antes de abril, se retrasa la ola 1.",
                "Tarea: Ana documentará el ADR-002 sobre CMEK y Cloud KMS.",
            ]),
            ("2026-02-23_devops", "Setup de pipelines CI/CD", [
                "Ana: He montado el pipeline base en Cloud Build con stages: build, test, scan, deploy.",
                "Luis: Hay que añadir Snyk en la fase de scan, ya está aprobado por seguridad.",
                "Decisión: Se usa Artifact Registry como repositorio único de imágenes Docker.",
                "Decisión: Despliegues a producción siempre con aprobación manual de PM y arquitecto.",
                "Tarea: Luis migrará los 5 servicios de la ola 1 al nuevo pipeline antes de finales de febrero.",
                "Bloqueante: Falta token de Snyk en GCP Secret Manager. Ana lo gestionará.",
            ]),
            ("2026-03-02_avance-ola1", "Avance de la ola 1 de migración", [
                "Luis: Llevamos 3 de 5 servicios desplegados en pre-producción. Funcionan correctamente.",
                "Carlos: Las pruebas de carga muestran latencia 18% menor en GCP que on-prem.",
                "Marta: ¿Cuándo podemos hacer el go-live de la ola 1?",
                "Luis: Si seguridad aprueba el pen-test del viernes, podemos pasar a producción el 10/03.",
                "Riesgo: El servicio de conciliación nocturna tiene problemas con el connector a Oracle on-prem.",
                "Tarea: Ana investigará si Cloud Interconnect resuelve la latencia con Oracle.",
                "Decisión: Posible rollback automático si se supera el 1% de tasa de error tras go-live.",
            ]),
        ],
    },
    "prueba_2": {
        "title": "Implantación de sistema antifraude con Machine Learning",
        "team": "Sara (Data Scientist), Pablo (PM), Inés (ML Eng), Roberto (Negocio Riesgos)",
        "actas": [
            ("2026-01-12_kickoff-antifraude", "Kickoff antifraude ML", [
                "Pablo: Objetivo: reducir el fraude en pagos con tarjeta un 30% en 12 meses con un modelo ML.",
                "Sara: Tenemos 18 meses de histórico de transacciones, 2.3M de etiquetas confirmadas.",
                "Roberto: El umbral de falsos positivos no puede superar el 0.5%, es crítico para la experiencia de cliente.",
                "Inés: Propongo un ensemble de XGBoost + red neuronal con features de comportamiento.",
                "Decisión: Modelo objetivo en producción para Q3 2026.",
                "Riesgo: La normativa PSD2 exige explicabilidad de decisiones ML, hay que considerar SHAP.",
                "Tarea: Sara preparará el dataset de entrenamiento limpio antes del 26/01.",
            ]),
            ("2026-01-19_features", "Ingeniería de features", [
                "Sara: He identificado 142 features candidatas, voy a hacer feature selection con mutual info.",
                "Inés: Las features de velocidad (txns/hora) son las más predictivas según mi análisis previo.",
                "Roberto: Negocio insiste en incluir el merchant category code y la geolocalización.",
                "Decisión: Se priorizan 35 features finales: 12 transaccionales, 15 de comportamiento, 8 contextuales.",
                "Tarea: Inés montará el feature store en Vertex AI para reutilización.",
                "Bloqueante: Falta acuerdo con DPO sobre uso de geolocalización fina.",
            ]),
            ("2026-01-26_modelo-baseline", "Modelo baseline", [
                "Sara: Baseline XGBoost da 0.87 AUC, recall 78% al 0.4% FPR. Buen punto de partida.",
                "Inés: La red neuronal por sí sola da 0.85, peor. Pero el ensemble llega a 0.91 AUC.",
                "Pablo: ¿Cuándo podemos hacer un piloto con datos reales?",
                "Decisión: Piloto en modo shadow desde 15/02 durante 4 semanas, sin bloquear transacciones reales.",
                "Riesgo: El modelo es sensible a drift, necesitamos monitorización continua.",
                "Tarea: Inés implementará el módulo de detección de drift con Evidently AI.",
            ]),
            ("2026-02-02_explicabilidad", "Cumplimiento y explicabilidad", [
                "Roberto: Compliance ha pedido que cualquier rechazo de pago se pueda justificar al cliente.",
                "Sara: Implementaremos SHAP values en cada decisión, con top-3 features que más influyen.",
                "Decisión: Se aprueba framework de explicabilidad basado en SHAP.",
                "Decisión: Logs de decisiones se guardan 5 años para auditoría regulatoria.",
                "Riesgo: Latencia del modelo + SHAP puede superar SLA de 80ms en pico de Black Friday.",
                "Tarea: Inés benchmarkeará el coste de SHAP en latencia de inferencia.",
            ]),
            ("2026-02-09_resultados-shadow", "Resultados primer mes de shadow mode", [
                "Sara: En shadow el modelo habría detectado 142 fraudes adicionales con 0.3% FPR.",
                "Roberto: Equivale a 380k EUR ahorrados en un mes. Negocio muy contento.",
                "Pablo: Podemos pasar a active mode el 1 de marzo si seguridad aprueba.",
                "Decisión: Go-live progresivo: 10% del tráfico el 1/03, 50% el 8/03, 100% el 15/03.",
                "Bloqueante: El equipo de operaciones necesita formación antes del go-live.",
                "Tarea: Pablo organizará 2 sesiones de formación para el equipo de fraude.",
            ]),
        ],
    },
    "prueba_3": {
        "title": "Cumplimiento normativo MiFID II — reportes de transacciones",
        "team": "Elena (PMO Regulatorio), Diego (Dev), Mireia (Compliance), Javier (QA)",
        "actas": [
            ("2026-03-01_kickoff-mifid", "Kickoff MiFID II", [
                "Elena: ESMA ha publicado actualización del RTS 22, hay que adaptar el reporting de transacciones antes del 30/06.",
                "Mireia: Los principales cambios afectan a 8 campos del esquema XML actual.",
                "Diego: El sistema actual reporta diariamente a CNMV, hay que mantener la ventana temporal.",
                "Decisión: Se aborda el cambio en 3 sprints de 4 semanas cada uno.",
                "Riesgo: Sanción potencial de hasta 5M EUR si no se cumple el plazo.",
                "Tarea: Mireia traducirá los cambios regulatorios a requisitos funcionales.",
            ]),
            ("2026-03-08_analisis-gap", "Análisis gap regulatorio", [
                "Mireia: He identificado 12 gaps entre la implementación actual y la nueva norma.",
                "Diego: 8 son cambios de mapeo, 3 son nuevos campos calculados, 1 implica refactor del motor.",
                "Decisión: El gap más complejo (clasificación de instrumentos OTC) se aborda primero.",
                "Decisión: Mantenemos compatibilidad con esquema antiguo durante 3 meses tras go-live.",
                "Tarea: Diego preparará ADR sobre estrategia de versionado dual del esquema.",
                "Bloqueante: Pendiente de recibir el XSD actualizado por parte de ESMA.",
            ]),
            ("2026-03-15_diseno", "Diseño técnico solución", [
                "Diego: Propongo un módulo nuevo de transformación XML que aísle el cambio.",
                "Javier: QA necesita acceso a un set de transacciones de test que cubra los 12 gaps.",
                "Decisión: Se adopta arquitectura de strategy pattern para soportar versiones múltiples del reporte.",
                "Tarea: Diego implementará prototipo del módulo antes del 22/03.",
                "Tarea: Javier definirá el plan de pruebas con casos para cada gap.",
                "Riesgo: Si ESMA cambia el XSD a última hora, hay que rehacer mappings.",
            ]),
            ("2026-03-22_pruebas", "Sesión de pruebas con set regulatorio", [
                "Javier: He ejecutado 1247 casos, 89% pasan. Los fallos son del nuevo campo 'execution venue'.",
                "Diego: El problema viene del lookup en la tabla de venues. Mireia, ¿quién la mantiene?",
                "Mireia: Esa tabla la actualiza el equipo de Reference Data semanalmente.",
                "Decisión: Se incluye validación previa al envío que rechace transacciones con venue desconocido.",
                "Tarea: Diego coordinará con Reference Data para sincronización diaria.",
                "Riesgo: Si la tabla está desfasada, hay riesgo de reportes erróneos a CNMV.",
            ]),
            ("2026-03-29_revision-compliance", "Revisión final con Compliance", [
                "Mireia: He revisado los reportes de muestra y todos cumplen con RTS 22 actualizado.",
                "Elena: ¿Estamos listos para UAT con Compliance al completo la próxima semana?",
                "Javier: Sí, tengo el entorno de UAT con datos enmascarados de producción.",
                "Decisión: UAT comienza 5/04, duración 2 semanas, con sign-off formal del CRO.",
                "Decisión: Go-live planificado para el 1/06, 30 días antes del deadline regulatorio.",
                "Tarea: Elena preparará comunicación al regulador para informar del nuevo flujo.",
            ]),
        ],
    },
    "prueba_4": {
        "title": "Modernización de la app de banca digital móvil",
        "team": "Lucía (Product Owner), Raúl (Tech Lead), Carmen (UX), Tomás (iOS), Nora (Android)",
        "actas": [
            ("2026-02-05_kickoff-mobile", "Kickoff modernización app", [
                "Lucía: La app actual tiene un NPS de 28, queremos llegar a 50 en 9 meses.",
                "Carmen: He hecho 12 entrevistas con clientes, los principales pain points son: login lento, navegación confusa y falta de personalización.",
                "Raúl: Técnicamente arrastramos 4 años de deuda. Propongo migrar a arquitectura modular.",
                "Decisión: Se aprueba reescritura progresiva siguiendo el patrón Strangler Fig.",
                "Riesgo: La app tiene 2.4M usuarios activos, no podemos permitir downtime.",
                "Tarea: Carmen entregará wireframes de los 5 flujos principales en 2 semanas.",
            ]),
            ("2026-02-12_arquitectura-mobile", "Arquitectura técnica modular", [
                "Raúl: Propongo dividir la app en 8 módulos: Auth, Cuentas, Tarjetas, Transferencias, Inversión, Préstamos, Soporte, Marketing.",
                "Tomás: En iOS usaremos Swift Package Manager para los módulos.",
                "Nora: En Android iremos con Gradle + Kotlin Multiplatform donde tenga sentido.",
                "Decisión: Lógica de negocio compartida en KMM (Kotlin Multiplatform Mobile).",
                "Decisión: UI nativa en cada plataforma, no usamos cross-platform UI.",
                "Tarea: Raúl preparará ADR comparando KMM vs Flutter vs nativo puro.",
            ]),
            ("2026-02-19_login-biometria", "Nuevo flujo de login con biometría", [
                "Carmen: El nuevo flujo tiene 3 pasos vs los 7 actuales. Tests de usabilidad muy positivos.",
                "Tomás: FaceID/TouchID integrado con el secure enclave del dispositivo.",
                "Nora: Android usará BiometricPrompt API, soporte desde Android 6.",
                "Decisión: Login biométrico opcional, siempre con fallback a PIN de 6 dígitos.",
                "Regla de negocio: Tras 3 fallos biométricos, se fuerza re-autenticación con usuario y contraseña.",
                "Tarea: Tomás y Nora implementarán login biométrico en sprint 3.",
            ]),
            ("2026-02-26_personalizacion", "Personalización con ML", [
                "Lucía: Queremos un home personalizado con widgets relevantes para cada usuario.",
                "Carmen: He diseñado 8 widgets: saldo, próximos cobros, ofertas, gasto categorizado, etc.",
                "Raúl: La personalización vendrá de un servicio backend que ya está en roadmap del equipo de data.",
                "Decisión: Se priorizan 4 widgets para MVP: saldo, próximos cobros, gasto del mes y promociones.",
                "Riesgo: El consentimiento GDPR para personalización requiere texto legal aprobado.",
                "Tarea: Lucía coordinará con legal el texto de consentimiento.",
            ]),
            ("2026-03-05_avance-mvp", "Avance del MVP", [
                "Tomás: iOS MVP al 65%. Login y home funcionando. Falta el módulo de transferencias.",
                "Nora: Android al 60%. Mismos hitos pendientes.",
                "Carmen: Test con 8 usuarios early adopters fue muy positivo, NPS interno 52.",
                "Lucía: ¿Vamos a llegar al beta cerrado del 1/04?",
                "Raúl: Apretado pero factible. Necesitamos paralelizar el módulo de transferencias.",
                "Decisión: Se contrata 1 dev contractor adicional para acelerar transferencias.",
                "Riesgo: Posible retraso del beta de 1 a 2 semanas si seguridad pide cambios.",
            ]),
        ],
    },
    "prueba_5": {
        "title": "Plataforma de Open Banking — APIs PSD2",
        "team": "Andrés (API Architect), Beatriz (PM), Hugo (Backend), Clara (Security)",
        "actas": [
            ("2026-01-08_kickoff-openbanking", "Kickoff Open Banking", [
                "Beatriz: Vamos a publicar las APIs PSD2 en versión 3.0 según estándar Berlin Group.",
                "Andrés: La plataforma actual soporta v2.5. Hay que actualizar 14 endpoints.",
                "Clara: PSD2 exige SCA (Strong Customer Authentication) con dynamic linking.",
                "Decisión: Adoptamos OpenAPI 3.1 como contrato fuente de verdad.",
                "Decisión: API Gateway: Apigee X. Sandbox público para TPPs en sandbox.bbva.com.",
                "Tarea: Andrés actualizará specs OpenAPI según Berlin Group v1.3.6.",
            ]),
            ("2026-01-15_sca-flow", "Flujo de SCA", [
                "Clara: SCA requiere dos factores de tres categorías: knowledge, possession, inherence.",
                "Hugo: Actualmente usamos OTP por SMS (possession) + PIN (knowledge). Cumple.",
                "Andrés: El reto es el dynamic linking: el OTP debe estar ligado al importe y al beneficiario exactos.",
                "Decisión: Migrar de SMS a push notifications firmadas para reducir fraude SIM-swap.",
                "Riesgo: Hay un 12% de clientes sin app móvil instalada, necesitan fallback SMS.",
                "Tarea: Hugo implementará servicio de notificación dual (push + SMS).",
            ]),
            ("2026-01-22_consentimientos", "Gestión de consentimientos", [
                "Andrés: Endpoint /consents con TTL máximo de 90 días según norma.",
                "Beatriz: ¿Cómo gestionamos la renovación de consentimientos?",
                "Clara: La renovación requiere SCA completo. No se puede automatizar.",
                "Decisión: Se construye dashboard para que el cliente vea y revoque consentimientos activos.",
                "Decisión: Notificación automática 7 días antes de vencer cada consentimiento.",
                "Tarea: Hugo implementará el módulo de consentimientos antes del 5/02.",
                "Bloqueante: Pendiente de recibir lista de TPPs autorizados por Banco de España.",
            ]),
            ("2026-01-29_sandbox", "Lanzamiento de sandbox para TPPs", [
                "Andrés: El sandbox está al 80%. Faltan los endpoints de Funds Confirmation.",
                "Hugo: He generado 100 cuentas sintéticas con datos realistas para testing.",
                "Beatriz: ¿Cuándo invitamos a los primeros TPPs a probar?",
                "Decisión: Beta cerrada con 5 TPPs partner desde 15/02. Lanzamiento público 1/04.",
                "Riesgo: Si los TPPs encuentran bugs críticos, se retrasa el lanzamiento público.",
                "Tarea: Beatriz preparará comunicación a TPPs partner.",
            ]),
            ("2026-02-05_metricas-tpp", "Métricas y monitorización", [
                "Andrés: Necesitamos dashboards de uso por TPP, latencia, errores y SCA exitosos.",
                "Hugo: He montado Grafana con métricas de Apigee + logs en BigQuery.",
                "Clara: Compliance pide alerta automática si un TPP supera 100 errores 4xx en 1h.",
                "Decisión: Se adoptan SLAs publicados: 99.9% disponibilidad, p95 <500ms.",
                "Decisión: Throttling por TPP: 100 req/s por defecto, configurable por contrato.",
                "Tarea: Hugo implementará alertas y rate limiting antes del go-live.",
            ]),
        ],
    },
}


def render_acta(project_meta, acta_meta) -> str:
    title = acta_meta[1]
    bullets = acta_meta[2]
    fecha_iso = acta_meta[0][:10]
    lines = [
        f"# {project_meta['title']} — {title}",
        f"**Fecha:** {fecha_iso}",
        f"**Asistentes:** {project_meta['team']}",
        "",
        "## Notas de la reunión",
        "",
    ]
    for b in bullets:
        lines.append(f"- {b}")
    lines.append("")
    return "\n".join(lines)


def generate_actas():
    for project, meta in PROJECTS.items():
        proj_dir = ACTAS_DIR / project
        proj_dir.mkdir(parents=True, exist_ok=True)
        for acta in meta["actas"]:
            fname = f"{acta[0]}.txt"
            (proj_dir / fname).write_text(render_acta(meta, acta), encoding="utf-8")
        print(f"  ✓ {project}: {len(meta['actas'])} actas creadas en {proj_dir}")


# ─────────────────────────────────────────────────────────────
# 2 PLANIFICACIONES HISTÓRICAS DE REFERENCIA
# ─────────────────────────────────────────────────────────────

HISTORICAL_PLANS = {
    "PLAN-migracion-core-bancario.md": """# Planificación histórica — Migración de Core Bancario a microservicios

**Duración real:** 18 semanas
**Equipo:** 12 personas (1 PM, 2 arquitectos, 6 desarrolladores, 2 QA, 1 DevOps)
**Presupuesto:** 1.2M EUR

## Fases y entregables

### Fase 1 — Análisis y diseño (semanas 1-3)
- Inventario de funcionalidades del core legacy
- Mapping a bounded contexts (DDD)
- ADR de arquitectura objetivo
- Plan de migración por dominios
- **Entregable:** Documento de arquitectura objetivo (HLD)

### Fase 2 — Plataforma base (semanas 4-6)
- Setup de Kubernetes (GKE)
- API Gateway (Kong)
- Service Mesh (Istio)
- Observabilidad (Prometheus + Grafana + Loki)
- CI/CD con GitHub Actions
- **Entregable:** Plataforma base operativa con servicio "Hello World"

### Fase 3 — Migración de dominios (semanas 7-14)
- Strangler Fig pattern para cada dominio
- Migración por orden: Cuentas → Tarjetas → Préstamos → Inversiones
- Pruebas de carga y caos por dominio
- Rollout progresivo con feature flags
- **Entregables:** 4 dominios migrados, cada uno con su ADR y DOM specs

### Fase 4 — Cutover y estabilización (semanas 15-18)
- Migración del 100% del tráfico
- Decomisado del core legacy
- Monitorización intensiva 24x7 durante 4 semanas
- Documentación post-mortem y lecciones aprendidas
- **Entregable:** Core legacy apagado, doc de operaciones

## Hitos críticos
- Semana 3: Aprobación de arquitectura por CTO
- Semana 6: Plataforma base validada por seguridad
- Semana 10: 50% de dominios migrados (checkpoint go/no-go)
- Semana 14: 100% migrado en pre-producción
- Semana 16: Cutover completo a producción
- Semana 18: Cierre del proyecto y entrega a operaciones

## Estructura documental usada

```
core-migration/
├── specs/
│   ├── architecture/   (ADRs)
│   ├── domains/        (DOMs por bounded context)
│   └── tasks/          (WRK-TASK)
├── docs/
│   ├── HLD.md
│   ├── runbook.md
│   └── post-mortem.md
└── infra/              (Terraform + Helm)
```

## Lecciones aprendidas
- El strangler pattern funcionó muy bien, evitó big-bang
- Subestimamos el tiempo de pruebas de regresión (factor 1.4x)
- Los feature flags fueron clave para el rollback rápido
- Faltó formación temprana al equipo de operaciones (2 semanas tarde)
""",
    "PLAN-implantacion-plataforma-datos.md": """# Planificación histórica — Implantación de Plataforma de Datos

**Duración real:** 14 semanas
**Equipo:** 9 personas (1 PM, 1 arquitecto, 4 data engineers, 2 analistas, 1 DPO)
**Presupuesto:** 720k EUR

## Fases y entregables

### Fase 1 — Discovery y arquitectura (semanas 1-2)
- Entrevistas con áreas consumidoras (Riesgos, Marketing, Finanzas)
- Catálogo inicial de fuentes de datos (47 sistemas origen)
- ADR de elección de stack (BigQuery + dbt + Looker)
- Modelo de gobierno de datos
- **Entregable:** Documento de visión y arquitectura

### Fase 2 — Plataforma base (semanas 3-5)
- Setup de BigQuery con datasets por capas (raw / staging / marts)
- Pipelines de ingesta con Cloud Composer (Airflow)
- Catálogo de datos en Data Catalog
- IAM por capas y por rol
- **Entregable:** Plataforma operativa con 3 fuentes piloto

### Fase 3 — Modelado y casos de uso (semanas 6-11)
- 4 dominios modelados en dbt: Clientes, Productos, Riesgos, Marketing
- Tests de calidad automatizados (dbt tests + Soda)
- Linaje de datos automático
- 6 dashboards Looker para áreas consumidoras
- **Entregables:** Modelos productivos por dominio, dashboards aprobados

### Fase 4 — Self-service y formación (semanas 12-14)
- Habilitación self-service para 25 analistas
- 4 sesiones de formación (BigQuery, dbt, Looker, gobierno)
- Documentación de procesos
- Handover al equipo de operaciones de datos
- **Entregable:** Comunidad self-service operativa

## Hitos críticos
- Semana 2: Aprobación de arquitectura por DPO y CISO
- Semana 5: Primera fuente productiva en BigQuery
- Semana 8: Primer dashboard usado por negocio
- Semana 11: 4 dominios modelados y validados
- Semana 13: 25 analistas formados
- Semana 14: Cierre y entrega a operaciones

## Estructura documental usada

```
data-platform/
├── specs/
│   ├── architecture/
│   ├── domains/
│   └── governance/
├── dbt/
│   ├── models/raw/
│   ├── models/staging/
│   └── models/marts/
├── airflow/dags/
└── docs/
    ├── catalog.md
    ├── lineage.md
    └── data-contracts.md
```

## Lecciones aprendidas
- Empezar con un caso de uso real desde sprint 1 fue clave para mantener engagement
- La adopción del catálogo costó más de lo previsto (formación insuficiente)
- Los data contracts evitaron muchas roturas en producción
- Hubo que añadir una fase no prevista de masking de datos personales (2 semanas extra)
"""
}


def generate_historical_plans():
    HIST_DIR.mkdir(parents=True, exist_ok=True)
    for fname, content in HISTORICAL_PLANS.items():
        (HIST_DIR / fname).write_text(content, encoding="utf-8")
        print(f"  ✓ Plan histórico creado: {HIST_DIR / fname}")


if __name__ == "__main__":
    print("=" * 70)
    print("Generando datos de prueba KDD PMO Copilot")
    print("=" * 70)
    print("\n[1/2] Generando actas de prueba (5 proyectos × 5 actas)...")
    generate_actas()
    print("\n[2/2] Generando planificaciones históricas de referencia...")
    generate_historical_plans()
    print("\n✅ Datos de prueba generados correctamente.")

