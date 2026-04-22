# Guide: The Governance Cycle (RFC → SPEC → ADR)

The governance cycle is how knowledge **evolves**. It ensures that changes to organizational knowledge are proposed, discussed, decided, and recorded — not applied ad hoc.

```
RFC (proposal)  ──→  Discussion  ──→  Decision  ──→  SPEC (new/updated)
                                          │                    +
                                          └───────────→  ADR (record)
```

> For governance artifact type definitions, see [spec-types.md](../../knowledge-architecture/spec-types.md). For the Evolutive pillar rationale, see [pillars.md](../../foundation/pillars.md).

## When to Use What

| Situation | Artifact |
|-----------|----------|
| Proposing a new approach or significant change | **RFC** |
| The decision is straightforward and uncontested | Go directly to **SPEC** |
| Recording why a decision was made | **ADR** |
| Defining a standing constraint or policy | **RULE** |

**Rule of thumb**: If the change affects multiple teams or reverses a previous decision, write an RFC first. If it's a local improvement within your domain, update the SPEC directly.

## Writing an RFC

An RFC (Request for Comments) proposes a change and invites discussion.

### Frontmatter

```yaml
---
id: RFC-001
type: governance
layer: rfc
title: Migrate from REST to gRPC for Internal Services
status: proposed           # proposed → accepted → superseded | rejected
version: "0.1.0"
owner: platform-team
tags: [api, grpc, migration]
dependencies:
  - id: ARCH-001
    type: supersedes        # This RFC proposes replacing ARCH-001
---
```

### Body

```markdown
## Context

What is the current situation? Why is a change being considered?

## Proposal

What specifically are you proposing?

## Rationale

Why this approach over alternatives?

## Alternatives Considered

What else was evaluated? Why were they rejected?

## Impact

- Which specs will change?
- Which teams are affected?
- What is the migration path?

## Open Questions

What needs discussion before deciding?
```

### RFC Lifecycle

1. **Proposed**: Author creates the RFC and shares with stakeholders
2. **Discussion**: Team reviews, comments, suggests modifications
3. **Decision**: Accept, reject, or defer
4. **Accepted** → Creates or updates SPECs + records an ADR
5. **Rejected** → Record the ADR explaining why (knowledge is preserved)

## Writing an ADR

An ADR (Architecture Decision Record) captures **why** a decision was made. It is written *after* the decision, not before.

### Frontmatter

```yaml
---
id: ADR-001
type: governance
layer: adr
title: Use Event-Driven Architecture for Trade Lifecycle
status: accepted           # accepted → superseded
version: "1.0.0"
owner: platform-team
tags: [architecture, events, kafka]
dependencies:
  - id: ARCH-002
    type: depends-on        # The SPEC that resulted from this decision
---
```

### Body

```markdown
## Status

Accepted — 2025-03-15

## Context

What was the situation that required a decision?

## Decision

What was decided? State it clearly in one sentence.

> We will use Apache Kafka as the event backbone for all trade lifecycle events.

## Rationale

Why this decision? What factors were weighted?

## Consequences

### Positive
- Decoupled services, independent scaling
- Built-in audit trail

### Negative
- Eventual consistency (not immediate)
- Event schema governance overhead

### Risks
- Kafka operational complexity
- Consumer lag under peak load

## Alternatives Considered

| Alternative | Why rejected |
|-------------|-------------|
| Synchronous REST | Tight coupling, cascading failures |
| RabbitMQ | Less suited for event sourcing at scale |
```

## Writing a RULE

A RULE is a **standing constraint** that applies across multiple specs. Rules are more durable than ADRs — they define ongoing policy rather than recording a point-in-time decision.

### Frontmatter

```yaml
---
id: RULE-001
type: governance
layer: rule
title: All Services Must Publish Domain Events
status: active
version: "1.0.0"
owner: architecture-guild
tags: [events, mandatory]
---
```

### Body

```markdown
## Rule

All services that modify domain state must publish a domain event
to the event backbone within the same transaction boundary.

## Rationale

Ensures auditability, enables downstream consumers, and maintains
the event-driven architecture integrity defined in ARCH-002.

## Enforcement

- CI check: verify event publication in service tests
- PR review: architecture guild reviews new services

## Exceptions

Document exceptions as ADRs with justification.
```

## The Full Cycle in Practice

Here's how the cycle works for a real scenario:

1. **Problem**: The VaR engine is too slow (current state documented in `DOM-RISK-001`)
2. **RFC**: Team proposes redesigning with event-driven partitioned workers
3. **Discussion**: Architecture guild reviews, risk team validates methodology constraints
4. **Decision**: Accepted with modifications (partition by asset class, not by portfolio)
5. **ADR**: Records the decision and rationale
6. **SPEC updates**: `ARCH-002` updated with new patterns, new `DOM-RISK-002` extends calculation rules
7. **Work begins**: `WRK-SPEC-001` is created, activating the updated knowledge

## Tips

- **Keep RFCs focused**: One proposal per RFC. Don't bundle unrelated changes.
- **Write ADRs even for rejected proposals**: The reasoning is valuable — it prevents re-litigating the same decision.
- **Link everything**: RFCs reference the specs they affect. ADRs reference the specs they produced. Use `dependencies` in frontmatter.
- **Review cadence**: Set a regular review (monthly or quarterly) to check if active RULEs and ADRs are still current.
