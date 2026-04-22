# Artifact Quick Reference

All artifact types in one page. For full definitions, see [spec-types.md](../../knowledge-architecture/spec-types.md) and [unified-taxonomy.md](../../knowledge-architecture/unified-taxonomy.md).

## Knowledge Artifacts (Persistent)

| Type | Layer | ID Pattern | Purpose | Key Relations |
|------|-------|------------|---------|---------------|
| **ARCH** | Architecture | `ARCH-AREA-NNN` | Cross-cutting technical decisions and patterns | Constrains DOM, PROD, FEAT |
| **DOM** | Domain | `DOM-AREA-NNN` | Business rules, domain logic, invariants | Implements regulations, constrained-by ARCH |
| **PROD** | Product | `PROD-AREA-NNN` | Product-level capabilities and vision | Implements strategy, constrains FEAT |
| **FEAT** | Feature | `FEAT-AREA-NNN` | User-facing feature specifications | Implements PROD, uses-data-from DOM |
| **DOC** | Documentation | `DOC-AREA-NNN` | Conventions, guides, standards | Supports all layers |

**Lifecycle**: `draft` → `active` → `deprecated`

**Confidence**: `low` (inferred) · `medium` (validated OR reviewed) · `high` (validated AND reviewed)

## Work Artifacts (Ephemeral)

| Type | Layer | ID Pattern | Purpose | Parent |
|------|-------|------------|---------|--------|
| **WRK-SPEC** | Spec | `WRK-SPEC-NNN` | Scope, constraints, activated knowledge | — |
| **WRK-PLAN** | Plan | `WRK-PLAN-NNN` | Architecture approach, task decomposition | WRK-SPEC |
| **WRK-TASK** | Task | `WRK-TASK-NNN` | Atomic implementable unit | WRK-PLAN |

**Lifecycle**: `draft` → `active` → `completed` → `archived`

**Key field**: `activates` — lists Knowledge Artifacts that provide context for this work.

## Governance Artifacts (Bridge)

| Type | Layer | ID Pattern | Purpose | Lifecycle |
|------|-------|------------|---------|-----------|
| **RFC** | RFC | `RFC-NNN` | Proposal for change | `proposed` → `accepted` / `rejected` → `superseded` |
| **ADR** | ADR | `ADR-NNN` | Record of a decision and rationale | `accepted` → `superseded` |
| **RULE** | Rule | `RULE-NNN` | Standing constraint or policy | `active` → `deprecated` |

## Dependency Relations

| Relation | Meaning | Typical usage |
|----------|---------|---------------|
| `implements` | Realizes a higher-level spec | FEAT → PROD, DOM → Regulation |
| `constrained-by` | Must respect constraints from | DOM → ARCH, FEAT → DOM |
| `extends` | Adds detail to a same-layer spec | DOM-002 → DOM-001 |
| `uses-data-from` | Consumes data defined elsewhere | FEAT → DOM |
| `activates` | Knowledge injected into work | WRK-SPEC → DOM, ARCH |
| `depends-on` | Generic dependency | Any |
| `supersedes` | Replaces another spec | New version → deprecated version |

## Required Frontmatter Fields

| Field | All types | Notes |
|-------|-----------|-------|
| `id` | Yes | Unique identifier |
| `type` | Yes | `knowledge`, `work`, or `governance` |
| `layer` | Yes | Depends on type (see tables above) |
| `title` | Yes | Human-readable |
| `status` | Yes | Lifecycle stage |
| `confidence` | Knowledge only | `low` / `medium` / `high` |
| `version` | Yes | Semver |
| `owner` | Yes | Team or person |

## Optional Frontmatter Fields

| Field | Applies to | Purpose |
|-------|-----------|---------|
| `domain` | Knowledge | Functional domain |
| `subdomain` | Knowledge | Subdomain within domain |
| `dependencies` | All | `[{id, type}]` |
| `activates` | Work | Knowledge specs to inject |
| `parent` | WRK-PLAN, WRK-TASK | Link to parent work artifact |
| `scope` | WRK-TASK | File boundaries `{includes, excludes}` |
| `reviewers` | All | List of reviewers |
| `tags` | All | Free-form tags |
| `supersedes` | All | ID of replaced spec |

> Full frontmatter reference: [spec-anatomy.md](../../knowledge-architecture/spec-anatomy.md)
