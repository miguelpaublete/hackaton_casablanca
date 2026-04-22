# Three Pillars of Knowledge-Driven Development

> Spec-Driven · Evolutive · Agentic

Three mutually reinforcing pillars that define what we do. Together they form a system where structured knowledge enables continuous learning, and continuous learning enables intelligent automation.

---

## Pillar 1: Spec-Driven

**Question it answers**: How do we structure, version, and govern knowledge?

The core artifact is the **specification (spec)**: a structured knowledge artifact that links business intent, technical definition, and architectural decision. Specs are not documents — they are **code**: structured, versioned in Git, readable by humans and machines alike.

The framework distinguishes two families of specs along orthogonal axes: **Knowledge Artifacts** (persistent, organizational — ARCH, DOM, PROD, FEAT, DOC) and **Work Artifacts** (ephemeral, scoped to a change — WRK-SPEC, WRK-PLAN, WRK-TASK). Work Artifacts activate Knowledge Artifacts as context, creating a bridge between what the organization knows and what it's building right now.

### What this means in practice

| Aspect | Traditional approach | Spec-Driven approach |
|--------|---------------------|---------------------|
| Knowledge management | Scattered across wikis, slides, emails | Single versioned repository |
| Artifact evolution | Manual, poorly traceable | Full version history with Git |
| Collaboration | Depends on individuals | Pull request review flows |
| Standards compliance | Periodic audits | Automated validation in pipelines |
| Regulatory evidence | Generated ad-hoc on demand | Produced continuously and automatically |

### Specifications as Foundation

Every AI interaction is defined by a formal specification that describes **what** the system must do (functional intent), not **how** it does it. Each spec includes a clear Definition of Done to validate outputs against requirements.

> *Specs are the contract; AI is the executor.*

### Intent-Model Separation

Specifications and code remain independent from any specific AI model. Change models without touching specs or code. This vendor-agnostic approach reduces lock-in and enables continuous adoption of better models as they emerge.

> *Write once, run on any model.*

### Everything as Code

Every artifact, decision, or standard exists as a structured file in a version-controlled repository. This dual nature — human-readable, machine-executable — enables automated validation, generation, and continuous integration.

### Traceability Chain

Specs link the **what**, the **how**, and the **why** of every decision, enabling full traceability:

```
Strategy → Standard → Design → Development → Metric
```

This traceability is not just operational — it is the **evidential support required by any regulatory audit** (DORA, Basel IV, MiFID II, EMIR).

---

## Pillar 2: Evolutive

**Question it answers**: How does knowledge grow with practice?

Architecture is not a static blueprint — it is a **living system** that learns from practice and refines its own standards continuously. Every project doesn't just deliver software: **it delivers knowledge**.

### The Continuous Cycle

```
[Common standards] → [Adapt to context] → [Execute & validate] → [Consolidate learnings]
        ↑________________________________________________________________↓
```

1. Architectural standards are formalized as **base specs**
2. New projects **inherit** the base spec and adapt to their context (not start from zero)
3. During execution, **validation tools detect deviations**
4. At closure, good practices and well-managed exceptions are **incorporated back** into the standard

This is formalized as the **Consolidate** phase: when Work Artifacts complete, learnings flow back into Knowledge Artifacts. New ADRs are recorded, domain specs are updated with clarified rules, and architecture specs are enriched with proven patterns. The Work → Knowledge consolidation loop is what transforms project delivery into organizational learning.

### Controlled Co-evolution

Code and specifications evolve in parallel with absolute traceability throughout the software lifecycle. Every code change links to a spec change; every spec change triggers validation.

> *Nothing changes without a trace.*

### Knowledge Governance

Specifications become reusable organizational assets. Patterns, validations, and learnings scale globally across teams and projects, enabling consistent quality and accelerated delivery.

> *Discover once, apply everywhere.*

### The RFC → SPEC → ADR Governance Cycle

Three artifact types cover the full knowledge lifecycle:

| Artifact | Role | Action |
|----------|------|--------|
| **RFC** (Request for Change) | Propose | Consensus mechanism before formalizing a change |
| **SPEC** | Formalize | Structured definition — the domain's source of truth |
| **ADR** (Architecture Decision Record) | Decide & learn | Record of a concrete decision with context and rationale |

This cycle ensures that knowledge is not just captured but **governed**: proposed transparently, formalized rigorously, and recorded with full context for future reference.

---

## Pillar 3: Agentic

**Question it answers**: How do we amplify team capabilities?

With knowledge structured and machine-readable, organizations can deploy a **layer of intelligent agents** that automates low-value tasks and elevates the team toward strategic work.

### Why agents need specs

Without a structured knowledge base, AI agents have no domain-specific context and reproduce the fundamental problem: dependence on generic models not aligned with organizational standards.

Agents operate across both axes of the unified taxonomy: they **activate** Knowledge Artifacts as context and **execute** Work Artifacts as tasks. A WRK-SPEC triggers contextual activation of relevant domain and architecture specs; a WRK-TASK provides the implementation scope for an agent to generate code, tests, or documentation.

Spec-driven agents guarantee four essential properties:

| Property | What it means in practice |
|----------|--------------------------|
| **Domain alignment** | The agent operates with the organization's real, governed knowledge — not generic knowledge |
| **Model independence** | Logic lives in the spec, not in the model (GPT, Claude, Gemini...). Changing providers requires no recoding |
| **White box** | Agent behavior is auditable, verifiable, and evolvable — essential in regulated environments |
| **Continuous evolution** | A change in a spec automatically translates to a change in agent behavior |

### Effort Redistribution

The agentic layer reorganizes work planes, freeing the team from operational tasks to elevate focus to the strategic plane:

| Plane | Before | After | Enabled by |
|-------|--------|-------|------------|
| Strategic | 10% | 20% | Automation of operational plane |
| Management | 20% | 10% | Governance and knowledge agents |
| Operational | 70% | 70% *(mostly automated)* | Spec validation, coding, and guide agents |

---

## How the Pillars Reinforce Each Other

```
        Spec-Driven
       (structure knowledge)
            │
     ┌──────┴──────┐
     ▼              ▼
 Evolutive      Agentic
(knowledge      (agents operate
 grows with     on structured
 practice)      knowledge)
     │              │
     └──────┬───────┘
            ▼
    Each project delivers
    knowledge that improves
    both standards and agents
```

- **Spec-Driven** creates the structured foundation that both other pillars require
- **Evolutive** ensures the knowledge base improves over time, making agents progressively smarter
- **Agentic** automates validation and governance, making the evolutive cycle faster and more reliable
