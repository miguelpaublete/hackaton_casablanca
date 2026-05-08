# Planificación histórica — Migración de Core Bancario a microservicios

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
