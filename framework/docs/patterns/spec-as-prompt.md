# Pattern: Spec as Prompt

How to use KDD specs as structured context for AI agents, enabling domain-aligned code generation with minimal hallucination.

> This pattern implements the [Agentic pillar](../../foundation/pillars.md). For activation mechanics, see [contextual-activation.md](../guides/contextual-activation.md).

## The Problem

When AI agents generate code without domain context:
- They hallucinate business rules (plausible but wrong)
- They violate architecture constraints they don't know about
- They produce generic patterns instead of domain-specific ones
- Each regeneration may produce different (inconsistent) results

## The Pattern

Feed activated specs into the agent's context window as structured input. The spec becomes the prompt — or more precisely, the **system-level context** that constrains the agent's output.

```
┌─────────────────────────────────────────────┐
│  Agent Context Window                       │
│                                             │
│  System: You are implementing WRK-TASK-001  │
│                                             │
│  Activated Knowledge:                       │
│  ├── DOM-RISK-001 (VaR calculation rules)   │
│  ├── ARCH-002 (event-driven patterns)       │
│  └── DOM-REG-001 (regulatory constraints)   │
│                                             │
│  Task: [WRK-TASK-001 body]                  │
│                                             │
│  → Agent generates domain-aligned code      │
└─────────────────────────────────────────────┘
```

## Implementation Patterns

### Pattern 1: Activation Bundle as System Prompt

Concatenate activated specs into a single context block:

```markdown
# Activated Knowledge

## DOM-RISK-001: Market Risk Calculation (VaR)
[full spec body]

## ARCH-002: Event-Driven Architecture
[full spec body]

---

# Your Task

## WRK-TASK-001: VaR Calculation Service
[full task body]

Implement this task respecting the activated knowledge above.
Acceptance criteria from the task AND from activated specs must be met.
```

**When to use**: Simple workflows, single-agent tasks, L4 adoption.

### Pattern 2: Layered Context Injection

Structure context by priority — the agent reads domain rules first, then architecture constraints, then the task:

```markdown
# Domain Rules (MUST follow)
[DOM specs — business rules, calculations, invariants]

# Architecture Constraints (MUST respect)
[ARCH specs — patterns, technology decisions, NFRs]

# Product Context (SHOULD align with)
[PROD/FEAT specs — user outcomes, success metrics]

# Task
[WRK-TASK with acceptance criteria]
```

**When to use**: Complex tasks where priority ordering matters.

### Pattern 3: Spec Reference with Retrieval

For large knowledge bases, don't inject all specs — inject summaries and let the agent request full specs on demand:

```markdown
# Available Knowledge (summaries)
- DOM-RISK-001: VaR must use 250-day historical simulation, 99% regulatory / 95% internal
- ARCH-002: All services communicate via Kafka events, Schema Registry required
- DOM-REG-001: MiFID II reporting, T+1 deadline

# Full specs available via tool: read_spec(id)

# Task
[WRK-TASK body]
```

**When to use**: L5 adoption, large knowledge graphs, agent frameworks with tool use.

## Context Window Optimization

Specs are designed to be context-efficient:

| Spec section | Include? | Why |
|-------------|----------|-----|
| Frontmatter | Yes (summary only) | ID, type, status, confidence — helps the agent understand the spec's role |
| Intent | Yes | Essential for understanding purpose |
| Definition | Yes | The core content the agent needs |
| Acceptance Criteria | Yes | Defines the contract the agent must meet |
| Evidence | Optional | Include if the agent needs to understand validation approach |
| Traceability | No | Not useful for generation |

**Budget guideline**: A typical WRK-TASK activation (2–5 specs) should fit in 3,000–8,000 tokens of context.

## Validation Loop

After the agent generates code, validate against spec acceptance criteria:

```
1. Agent generates code using activated specs
2. Run acceptance criteria from WRK-TASK
3. Run acceptance criteria from activated DOM/ARCH specs
4. If failing → feed the failure + relevant spec section back to agent
5. Iterate until all criteria pass
```

This creates a **spec-driven feedback loop** — the spec defines both the input context and the output validation.

## Example: VaR Calculation Service

**Input to agent**:

```markdown
# Domain Rules

## DOM-RISK-001: Market Risk Calculation
- Historical simulation: 250-business-day rolling window
- Regulatory VaR: 10-day holding, 99th percentile
- Internal VaR: 1-day holding, 95th percentile
- Position-level attribution required
- Asset classes: Equities, FX, Rates, Credit, Commodities

# Architecture Constraints

## ARCH-002: Event-Driven Architecture
- Services communicate via Apache Kafka
- Events use Schema Registry (Avro)
- Consumers must be idempotent
- Dead letter queues for failed processing

# Task: WRK-TASK-001 — VaR Calculation Service

## Objective
Implement the core VaR calculation engine as a stateless service.

## Acceptance Criteria
- Computes 1-day and 10-day VaR at 95% and 99% confidence
- Covers all 5 asset classes
- Position-level risk attribution
- Processes 20,000 positions in under 12 minutes
- >95% test coverage
```

**Result**: The agent produces a calculation service that:
- Uses the exact methodology from DOM-RISK-001 (no hallucinated formulas)
- Follows event-driven patterns from ARCH-002
- Meets all acceptance criteria from the task

## Tips

- **Frontmatter matters.** Include `confidence: high` vs `low` — it signals to the agent how much to trust the spec.
- **Don't over-activate.** More context ≠ better output. 5 focused specs > 20 loosely related ones.
- **Include acceptance criteria from specs, not just the task.** The agent should know the domain constraints it must meet.
- **Version pin.** When referencing specs, note the version. This makes the generation reproducible.
- **Iterate on activation, not on prompts.** If the agent gets domain rules wrong, the fix is usually activating a missing spec — not rewriting the prompt.
