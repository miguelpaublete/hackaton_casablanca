# Getting Started with Knowledge-Driven Development

## What is KDD?

Knowledge-Driven Development (KDD) is a methodology where **structured specifications are the primary artifact** that drives software delivery. Instead of ad-hoc documents or tribal knowledge, every significant decision, domain rule, and architectural constraint lives as a versioned, machine-readable spec.

Three axes organize all artifacts:

```
Knowledge (persistent)    Work (ephemeral)       Governance (bridge)
────────────────────     ─────────────────      ──────────────────
ARCH  Architecture       WRK-SPEC  Scope        RFC   Proposals
DOM   Domain rules       WRK-PLAN  How          ADR   Decisions
PROD  Product vision     WRK-TASK  Do           RULE  Constraints
FEAT  Feature specs
DOC   Documentation
```

- **Knowledge Artifacts** capture what the organization *knows* — they persist across projects.
- **Work Artifacts** capture what a team *does* — they are ephemeral and scoped to a delivery.
- **Governance Artifacts** bridge both — they record how knowledge evolves through decisions.

> For the full rationale, see [manifesto.md](../foundation/manifesto.md). For the three pillars (Spec-Driven, Evolutive, Agentic), see [pillars.md](../foundation/pillars.md).

---

## Your First Spec in 10 Minutes

Let's create a simple Domain spec for a business rule.

### Step 1: Create the file

```bash
mkdir -p specs/domain
touch specs/domain/DOM-PAYMENTS-001-transfer-limits.md
```

### Step 2: Write the frontmatter

```yaml
---
id: DOM-PAYMENTS-001
type: knowledge
layer: domain
title: Domestic Transfer Limits
status: draft
confidence: medium
version: "0.1.0"
owner: payments-team
domain: payments
subdomain: transfers
tags: [limits, compliance]
dependencies: []
---
```

### Step 3: Write the body

```markdown
## Intent

Define the maximum transfer amounts for domestic payments,
ensuring compliance with AML thresholds.

## Definition

### Transfer Limits

| Customer Tier | Single Transfer | Daily Aggregate |
|---------------|---------------:|----------------:|
| Standard      |        €10,000 |         €25,000 |
| Premium       |        €50,000 |        €100,000 |
| Corporate     |       €500,000 |      €1,000,000 |

### Rules

- Transfers exceeding the single limit require dual approval.
- Daily aggregate is calculated on a rolling 24-hour window.
- Corporate limits may be overridden per-client via RULE artifacts.

## Acceptance Criteria

- [ ] Payment service enforces single-transfer limits by tier
- [ ] Daily aggregate check runs before authorization
- [ ] Dual approval flow triggers above threshold

## Evidence

- AML regulation reference: EU Directive 2015/849
- Business validation: Product owner sign-off pending
```

### Step 4: Validate

```bash
node apps/spec-graph/spec-graph.mjs --specs specs validate
```

That's it. You have a versioned, structured domain spec that any team member or AI agent can consume.

---

## Progressive Adoption

You don't need to adopt everything at once. KDD defines five adoption levels:

| Level | Name | What you do | What you get |
|-------|------|-------------|--------------|
| **L1** | Document | Write specs in Markdown with YAML frontmatter | Single source of truth, version control |
| **L2** | Validate | Run `spec-graph validate`, enforce in CI | Broken links caught early, dependency integrity |
| **L3** | Automate | Generate boilerplate from specs (API stubs, schemas) | Consistency between spec and code |
| **L4** | Generate | AI agents consume specs as context to produce code | Domain-aligned generation, less hallucination |
| **L5** | Orchestrate | Agents activate knowledge automatically per task | Full agentic workflow with knowledge loop |

**Start at L1.** Most teams get value within the first sprint. See [adoption-levels.md](reference/adoption-levels.md) for detailed criteria and examples.

---

## What's Next?

| I want to... | Go to |
|--------------|-------|
| Create a Knowledge spec (ARCH, DOM, PROD, FEAT, DOC) | [guides/create-knowledge-spec.md](guides/create-knowledge-spec.md) |
| Plan and execute work (WRK-SPEC → WRK-PLAN → WRK-TASK) | [guides/create-work-spec.md](guides/create-work-spec.md) |
| Understand the governance cycle (RFC → SPEC → ADR) | [guides/governance-cycle.md](guides/governance-cycle.md) |
| Use specs as context for AI agents | [patterns/spec-as-prompt.md](patterns/spec-as-prompt.md) |
| Adopt KDD in an existing project | [patterns/brownfield-adoption.md](patterns/brownfield-adoption.md) |
| Look up artifact types quickly | [reference/artifact-quick-ref.md](reference/artifact-quick-ref.md) |
| Check a spec before submitting a PR | [reference/spec-checklist.md](reference/spec-checklist.md) |

> For the full framework specification, see [foundation/](../foundation/) and [knowledge-architecture/](../knowledge-architecture/).
