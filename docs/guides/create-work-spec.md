# Guide: Create Work Artifacts (WRK-SPEC → WRK-PLAN → WRK-TASK)

Work Artifacts capture **what a team is doing right now**. They are ephemeral — scoped to a delivery and archived when done. The flow is always top-down:

```
WRK-SPEC (what & why)  →  WRK-PLAN (how)  →  WRK-TASK (do)
```

> For the full type definitions, see [spec-types.md](../../knowledge-architecture/spec-types.md). For real examples, see [examples/work/](../../examples/work/).

## The Three Levels

| Artifact | Purpose | Owner | Lifecycle |
|----------|---------|-------|-----------|
| **WRK-SPEC** | Defines scope, constraints, and activated knowledge | Tech lead / architect | Draft → Active → Completed → Archived |
| **WRK-PLAN** | Decomposes into tasks, defines architecture approach | Tech lead | Draft → Active → Completed → Archived |
| **WRK-TASK** | Atomic unit of work, implementable by one person/agent | Developer | Draft → Active → Completed → Archived |

## Step 1: Create a WRK-SPEC

The WRK-SPEC answers: *What are we building and why? What knowledge do we need?*

### Frontmatter

```yaml
---
id: WRK-SPEC-001
type: work
layer: spec
title: VaR Engine Redesign
status: draft
version: "0.1.0"
owner: risk-analytics-team
activates:
  - DOM-RISK-001      # Domain rules we must respect
  - ARCH-002          # Architecture constraints
  - DOM-REG-001       # Regulatory requirements
tags: [var, performance, redesign]
---
```

Key fields:
- `type: work` — marks this as a Work Artifact
- `layer: spec` — this is the scope level
- `activates` — **the most important field**: which Knowledge Artifacts provide context for this work

### Body Structure

```markdown
## Problem Statement
Why are we doing this? What's broken or missing?

## Proposed Solution
High-level approach (not implementation details — that's WRK-PLAN).

## Activated Knowledge
For each activated spec, explain why it's relevant:
- **DOM-RISK-001**: Defines VaR calculation rules we must implement
- **ARCH-002**: Mandates event-driven communication pattern
- **DOM-REG-001**: Regulatory constraints on methodology

## Constraints
Non-negotiable boundaries inherited from activated knowledge.

## Acceptance Criteria
How do we know the work is done?

## Open Questions
Decisions deferred to WRK-PLAN or later.
```

> See [WRK-SPEC-001](../../examples/work/WRK-SPEC-001-var-engine-redesign.md) for a complete example.

### Choosing What to Activate

Activation connects work to organizational knowledge. Choose carefully:

1. **Explicit**: Which specs directly define what you're building?
2. **Transitive**: What do those specs depend on?
3. **Filter**: Remove anything not relevant to this specific work.
4. **Budget**: Keep the activation set manageable (5–10 specs max for a typical WRK-SPEC).

You can use the CLI to discover relevant specs:

```bash
# Find everything connected to a spec
node apps/spec-graph/spec-graph.mjs --specs <dir> context DOM-RISK-001 --depth 2

# See impact of changing a spec
node apps/spec-graph/spec-graph.mjs --specs <dir> impact ARCH-002
```

> Full activation guide: [contextual-activation.md](contextual-activation.md)

## Step 2: Create a WRK-PLAN

The WRK-PLAN answers: *How will we build it? What are the tasks?*

### Frontmatter

```yaml
---
id: WRK-PLAN-001
type: work
layer: plan
title: VaR Engine Implementation Plan
status: draft
version: "0.1.0"
owner: risk-analytics-team
parent: WRK-SPEC-001           # Links to the parent WRK-SPEC
activates:
  - DOM-RISK-001
  - ARCH-002
tags: [var, implementation]
---
```

Key addition: `parent` links this plan to its WRK-SPEC.

### Body Structure

```markdown
## Architecture Approach
Key technical decisions for this implementation.

## Task Decomposition
Break the work into WRK-TASKs:

| Task ID | Title | Estimate | Dependencies |
|---------|-------|----------|--------------|
| WRK-TASK-001 | VaR Calculation Service | 5d | — |
| WRK-TASK-002 | VaR API Endpoint | 3d | WRK-TASK-001 |
| WRK-TASK-003 | Event Consumer | 3d | WRK-TASK-001 |

## Constraints
Inherited from WRK-SPEC + any new ones from architecture decisions.

## Risk Assessment
What could go wrong? Mitigations?

## Dependencies
External dependencies (infrastructure, other teams, etc.)
```

> See [WRK-PLAN-001](../../examples/work/WRK-PLAN-001-var-engine-redesign.md) for a complete example.

## Step 3: Create WRK-TASKs

Each WRK-TASK is an **atomic unit of work** — implementable by one developer or AI agent.

### Frontmatter

```yaml
---
id: WRK-TASK-001
type: work
layer: task
title: VaR Calculation Service
status: draft
version: "0.1.0"
owner: developer-a
parent: WRK-PLAN-001           # Links to the parent WRK-PLAN
scope:
  includes:
    - src/var/calculation/**
  excludes:
    - src/var/api/**
tags: [var, core-engine]
---
```

Key addition: `scope` defines the file boundaries this task operates within.

### Body Structure

```markdown
## Objective
What this task produces (a service, a module, an endpoint).

## Technical Specification
Detailed implementation guidance:
- Interfaces and contracts
- Data models
- Patterns to follow
- Activated knowledge to respect

## Acceptance Criteria
Specific, testable criteria for this task alone.

## Test Strategy
What tests to write: unit, integration, property-based, performance.
```

> See [WRK-TASK-001](../../examples/work/WRK-TASK-001-var-calculation-service.md) and [WRK-TASK-002](../../examples/work/WRK-TASK-002-var-api-endpoint.md) for complete examples.

## Lifecycle

```
Draft ──→ Active ──→ Completed ──→ Archived
  │                      │
  │                      ├─→ Create ADRs for significant decisions
  │                      └─→ Update Knowledge Artifacts with new learnings
  │
  └─→ (abandoned work is archived directly)
```

When work completes:
1. Mark the WRK-TASK as `completed`, then the WRK-PLAN, then the WRK-SPEC
2. Run the [consolidation process](consolidation.md) to feed learnings back into Knowledge Artifacts
3. Archive the work artifacts

## Quick Reference

| Question | Answer |
|----------|--------|
| How many WRK-TASKs per WRK-PLAN? | 3–8 is typical. More suggests the WRK-SPEC scope is too large. |
| Can I skip WRK-PLAN? | For very small work (1–2 tasks), you can go WRK-SPEC → WRK-TASK directly. |
| Who writes each level? | WRK-SPEC: architect/lead. WRK-PLAN: lead. WRK-TASK: developer or lead. |
| Can AI agents write WRK-TASKs? | Yes — this is a key L4/L5 pattern. The agent uses activated knowledge as context. |
