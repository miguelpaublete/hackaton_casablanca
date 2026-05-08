# Planificación histórica — Implantación de Plataforma de Datos

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
