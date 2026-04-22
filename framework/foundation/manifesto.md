# Manifesto — Why Knowledge-Driven Development

> The key is not just "specs before code" but **what knowledge to structure and how to activate it contextually**.

---

## The Double Problem

Organizations face two converging crises that amplify each other:

### 1. Organizational Knowledge is Fragmented

Critical knowledge — architectural decisions, business rules, domain expertise, regulatory requirements — is **distributed, duplicated, or siloed** across tools, formats, and teams. This fragmentation creates structural problems that worsen as organizations scale:

- **Knowledge depends on individuals**, not systems — continuity and scalability suffer
- **No coherence across domains** — each area defines its own standards, complicating integration
- **Minimal reuse** — teams reinvent solutions that already exist elsewhere
- **Impossible to govern** — no global view of maturity, compliance, or architectural evolution

### 2. AI Acceleration Without Methodology

AI-assisted development is accelerating at unprecedented speed, but without a structured approach it amplifies the knowledge problem rather than solving it. Four specific challenges emerge:

#### Ephemeral Stacks

The AI ecosystem evolves relentlessly: models, frameworks, agents, toolkits. Any investment in a specific tool has an expiration date. **Knowledge tied to a stack is lost when that stack changes.**

> *Specifications are the asset that survives technology changes.*

#### Black-Box by Design

"Vibe coding" enables prototyping in hours what used to take weeks. But the result is **easy to create, impossible to maintain**:

- No traceability: which requirement does this code fulfill?
- No interpretability: why does it work this way?
- No baseline: what do we compare against to validate?
- No best practices: the code "works" but nobody knows how

> *Specifications create the verifiable contract that vibe coding ignores.*

#### Fast Start, Forced Restart

Without a solid foundation, any significant change requires rewriting from scratch. **Today's prototype is tomorrow's technical debt.**

> *Specifications provide the stable foundation for incremental evolution.*

#### No Replicable Methodology

Every AI project is ad-hoc. No standard process, no defined artifacts, no way to scale knowledge across teams or projects.

> *Spec-driven development is the missing methodology.*

---

## Why Specifications

Specifications serve as a **universal interface** that benefits all stakeholders:

| Audience | Benefit |
|----------|---------|
| **Human Developers** | Clear implementation guidance, testable requirements |
| **Domain Experts** | Reviewable, validatable documentation of business knowledge |
| **QA Engineers** | Derivable test cases, acceptance criteria as specification |
| **AI Assistants** | Structured context for high-quality, aligned generation |
| **Regulators & Auditors** | Traceable evidence of decisions, compliance, and governance |

The spec is the artifact that:
- **Survives** the change of stack, model, or framework
- **Creates** traceability from strategy to code to deployment
- **Scales** knowledge across teams, projects, and organizations
- **Enables** both human and AI agents to operate with domain alignment

> **If it wasn't written as a spec, it wasn't discovered.**

---

## Positioning

### vs. Vibe Coding (no rigor)

Vibe coding produces working prototypes fast but creates black boxes: no traceability, no maintainability, no governance. Spec-driven development preserves speed while adding the structure that makes systems maintainable and auditable.

### vs. Waterfall Specifications (no agility)

Traditional specification approaches are heavyweight, disconnected from code, and obsolete before implementation finishes. Our specs are **living artifacts** — versioned, validated continuously, and co-evolving with the codebase.

### vs. Current SDD Tools (no domain taxonomy)

Emerging tools like GitHub Spec Kit, Kiro, and Tessl bring valuable spec-first workflows. But they treat specifications as generic documents — workflow without taxonomy.

GitHub Spec Kit, for example, provides a clean Specify → Plan → Tasks → Implement flow. Our framework embraces this workflow (as Work Artifacts) while adding what's missing:

- **Domain knowledge taxonomy** — structured functional and technical knowledge specific to industries like banking
- **Contextual activation** — the ability to surface the right domain knowledge at the right SDLC phase
- **Knowledge governance** — confidence levels, lifecycle management, and organizational reuse
- **Orthogonal axes** — Knowledge (persistent) and Work (ephemeral) are separate concerns, connected by the `activates` relation. Knowledge accumulates across projects; work artifacts are scoped and disposable

---

## Our Thesis

The emerging Spec-Driven Development practice (recognized by Thoughtworks, GitHub, Martin Fowler, and validated by ICSE 2026 research showing architectural specs improve LLM-generated code quality) addresses a real need. But current approaches stop at "specs before code."

Our differentiation:

1. **Taxonomy of domain knowledge** — both functional (business domains, rules, regulations) and technical (architecture patterns, NFRs, quality standards)
2. **Contextual activation across the SDLC** — the right knowledge surfaces at the right phase
3. **Layered specification hierarchy** — from architecture to features, with governance at every level
4. **Industry-specific depth** — starting with CIB (Corporate & Investment Banking), extensible to other verticals
5. **Knowledge + Work as orthogonal axes** — not just "specs before code" but a unified taxonomy where persistent knowledge and ephemeral work artifacts are separate concerns, connected by contextual activation and governed by decisions

The result is not just a development methodology but a **knowledge operating system** that makes AI genuinely useful in complex, regulated environments.
