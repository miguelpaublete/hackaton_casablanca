# Guide: Contextual Activation

Contextual activation is the process of **injecting the right organizational knowledge into a work stream**. It ensures that when a team (or AI agent) works on a task, they have the relevant domain rules, architecture constraints, and product context — not everything, just what matters.

> For the theoretical foundation, see the Activation section in [unified-taxonomy.md](../../knowledge-architecture/unified-taxonomy.md). For the Agentic pillar rationale, see [pillars.md](../../foundation/pillars.md).

## Why It Matters

Without activation:
- Developers re-discover constraints by trial and error
- AI agents hallucinate domain rules instead of using documented ones
- Architecture decisions are violated because teams didn't know they existed
- Knowledge exists but isn't used at the point of work

With activation:
- The right knowledge is available *before* implementation begins
- Constraints are respected by design, not caught in review
- AI agents produce domain-aligned output on the first pass

## The Activation Pipeline

Activation follows four steps:

```
1. Explicit  →  2. Transitive  →  3. Filtered  →  4. Budgeted
```

### 1. Explicit Activation

Start with the specs that **directly define** what you're building.

Ask: *"Which specs describe the domain rules, architecture patterns, or product requirements I need?"*

```yaml
# In your WRK-SPEC frontmatter:
activates:
  - DOM-RISK-001      # VaR calculation rules
  - ARCH-002          # Event-driven architecture
```

### 2. Transitive Activation

Follow the dependency graph from your explicitly activated specs.

```bash
# See what DOM-RISK-001 depends on
node apps/spec-graph/spec-graph.mjs --specs <dir> context DOM-RISK-001 --depth 2
```

This might reveal:
- `DOM-REG-001` (regulatory constraints that DOM-RISK-001 implements)
- `ARCH-001` (API standards that ARCH-002 extends)

Add relevant transitive specs to your activation set.

### 3. Filtered Activation

Not everything in the transitive closure is relevant. Remove specs that:
- Describe a different aspect of the domain than what you're working on
- Are at a layer too abstract or too detailed for your current scope
- Are deprecated or superseded

**Filter heuristic**: If removing a spec from the activation set wouldn't change how you implement the work, it doesn't belong.

### 4. Budgeted Activation

Keep the activation set manageable:

| Work level | Typical budget |
|------------|---------------|
| WRK-SPEC | 5–10 specs |
| WRK-PLAN | 3–7 specs (subset of WRK-SPEC's activation) |
| WRK-TASK | 2–5 specs (only what this task touches) |

Larger budgets dilute focus. If you need more than 10 specs, your WRK-SPEC scope is probably too broad.

## Activation Matrix

Different phases of work activate different knowledge layers:

| Phase | Primary layers | Secondary layers |
|-------|---------------|-----------------|
| Requirements | PROD, DOM | ARCH |
| Design | ARCH, DOM | PROD, FEAT |
| Build | FEAT, DOM | ARCH |
| Test | DOM, FEAT | ARCH |
| Deploy | ARCH | DOM |

## Manual vs. Automatic Activation

### Manual (L1–L3)

At lower adoption levels, the tech lead manually selects which specs to activate:

1. Review the domain you're working in
2. Use `spec-graph context` to explore the knowledge graph
3. Read candidate specs and decide relevance
4. List them in the `activates` field of your WRK-SPEC

### Automatic (L4–L5)

At higher adoption levels, AI agents can run the activation pipeline:

1. Parse the WRK-SPEC to understand the task
2. Query the knowledge graph for relevant specs
3. Apply the filter/budget heuristics
4. Inject activated specs into the agent's context window

This is the core of the [spec-as-prompt pattern](../patterns/spec-as-prompt.md).

## Using the CLI for Activation

```bash
# Discover specs connected to your domain
node apps/spec-graph/spec-graph.mjs --specs <dir> filter --layer domain --tag risk

# See the full context around a spec (depth 2 = direct + transitive)
node apps/spec-graph/spec-graph.mjs --specs <dir> context DOM-RISK-001 --depth 2

# Check impact: what depends on a spec you're changing?
node apps/spec-graph/spec-graph.mjs --specs <dir> impact ARCH-002

# Find shortest path between two specs (useful for understanding relationships)
node apps/spec-graph/spec-graph.mjs --specs <dir> path DOM-RISK-001 FEAT-ANALYTICS-001
```

## Example

For the VaR Engine Redesign (`WRK-SPEC-001`):

| Step | Action | Result |
|------|--------|--------|
| Explicit | "We're redesigning the VaR engine" | DOM-RISK-001, ARCH-002 |
| Transitive | `context DOM-RISK-001 --depth 2` | + DOM-REG-001, ARCH-001, DOM-DATA-001 |
| Filtered | ARCH-001 is too abstract, DOM-DATA-001 is about different data | Remove both |
| Budgeted | 3 specs is within budget | Final: DOM-RISK-001, ARCH-002, DOM-REG-001 |

These three specs provide the calculation rules, architecture pattern, and regulatory constraints needed to build the engine correctly.
