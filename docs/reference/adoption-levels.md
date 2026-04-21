# Adoption Levels (L1–L5)

KDD is designed for incremental adoption. Each level builds on the previous one. Start at L1 and progress as the team matures.

> For the design rationale behind incremental adoption, see [Principle 4 in principles.md](../../foundation/principles.md).

## Overview

| Level | Name | Core practice | Prerequisites |
|-------|------|--------------|---------------|
| **L1** | Document | Write specs in Markdown with YAML frontmatter | Text editor, git |
| **L2** | Validate | Automated validation of spec integrity | spec-graph CLI, CI pipeline |
| **L3** | Automate | Generate artifacts from specs | Code generators, templates |
| **L4** | Generate | AI agents consume specs as context | LLM integration, activation pipeline |
| **L5** | Orchestrate | Agents autonomously activate knowledge and execute work | Agent framework, full knowledge graph |

---

## L1 — Document

**What you do**: Write specs as Markdown files with YAML frontmatter. Store them in version control alongside code.

**What you get**:
- Single source of truth for domain rules and architecture decisions
- Version history via git
- Searchable, reviewable knowledge base

**Criteria for L1**:
- [ ] Team has a `specs/` directory in their repository
- [ ] At least the critical domain rules are captured as DOM specs
- [ ] Architecture decisions are recorded as ARCH specs or ADRs
- [ ] Specs follow the standard anatomy (frontmatter + standard sections)
- [ ] Specs are reviewed in PRs like code

**What an L1 project looks like**:
```
project/
├── src/
├── specs/
│   ├── domain/
│   │   ├── DOM-PAYMENTS-001-transfer-limits.md
│   │   └── DOM-PAYMENTS-002-fee-calculation.md
│   ├── architecture/
│   │   └── ARCH-001-api-gateway.md
│   └── governance/
│       └── ADR-001-database-choice.md
└── README.md
```

**Typical timeline**: 1–2 sprints to establish the practice.

---

## L2 — Validate

**What you do**: Run automated validation on specs. Enforce in CI.

**What you get**:
- Broken dependencies caught before merge
- Frontmatter consistency enforced automatically
- Orphan specs detected early

**Criteria for L2** (in addition to L1):
- [ ] `spec-graph validate` runs in CI and blocks PRs on failure
- [ ] `spec-graph orphans` runs as a warning (not blocking initially)
- [ ] Dependency graph is visualizable (`spec-graph build --html`)
- [ ] Team reviews the dependency graph periodically

**What an L2 project looks like**:
```yaml
# .github/workflows/spec-validation.yml
- name: Validate specs
  run: node apps/spec-graph/spec-graph.mjs --specs specs validate
- name: Check orphans
  run: node apps/spec-graph/spec-graph.mjs --specs specs orphans
```

**Typical timeline**: 1 sprint to add CI validation after L1 is established.

---

## L3 — Automate

**What you do**: Generate code artifacts from specs — API stubs, database schemas, test scaffolds, documentation.

**What you get**:
- Guaranteed consistency between spec and implementation
- Reduced boilerplate effort
- Spec becomes the source, code becomes the output

**Criteria for L3** (in addition to L2):
- [ ] At least one code generation pipeline exists (e.g., OpenAPI → server stubs)
- [ ] Generated artifacts are not manually edited (regenerated on spec change)
- [ ] Templates for common spec types exist and are used

**Example**: An ARCH spec defining API standards generates an OpenAPI skeleton. A DOM spec defining validation rules generates a validation module.

**Typical timeline**: 2–3 sprints to build the first generation pipeline.

---

## L4 — Generate

**What you do**: AI agents consume specs as context to produce code, tests, and documentation. The spec-as-prompt pattern becomes standard practice.

**What you get**:
- Domain-aligned AI output (less hallucination, more accuracy)
- Faster feature delivery with knowledge-backed generation
- Consistent architecture across agent-generated code

**Criteria for L4** (in addition to L3):
- [ ] WRK-SPEC → WRK-PLAN → WRK-TASK flow is standard practice
- [ ] `activates` field is used consistently in Work Artifacts
- [ ] AI agents receive activated specs as context before generating code
- [ ] Agent output is reviewed against activated specs' acceptance criteria

**What an L4 workflow looks like**:
1. Tech lead writes WRK-SPEC with activated knowledge
2. Agent receives WRK-SPEC + activated DOM/ARCH specs as context
3. Agent generates WRK-PLAN with task decomposition
4. Per task: agent receives WRK-TASK + relevant specs → generates code
5. Code is reviewed against spec acceptance criteria

> See [spec-as-prompt.md](../patterns/spec-as-prompt.md) for implementation patterns.

**Typical timeline**: 2–4 sprints after L3, depending on LLM tooling maturity.

---

## L5 — Orchestrate

**What you do**: Agents autonomously navigate the knowledge graph to activate relevant specs, plan work, execute tasks, and consolidate learnings — with human oversight at key checkpoints.

**What you get**:
- End-to-end knowledge-driven delivery
- Continuous knowledge evolution (work produces knowledge)
- Scalable delivery with preserved domain alignment

**Criteria for L5** (in addition to L4):
- [ ] Agents run the full activation pipeline (explicit → transitive → filtered → budgeted)
- [ ] Consolidation is partially automated (agents propose knowledge updates after work completion)
- [ ] The governance cycle (RFC → SPEC → ADR) is integrated into the agent workflow
- [ ] Human review gates exist at WRK-SPEC approval and consolidation approval

**What an L5 workflow looks like**:
1. Human describes a goal: "Improve VaR calculation performance"
2. Agent queries knowledge graph, activates relevant specs
3. Agent drafts WRK-SPEC → human reviews and approves
4. Agent decomposes into WRK-PLAN → WRK-TASKs → generates code
5. On completion, agent proposes knowledge updates (new ADRs, updated specs)
6. Human reviews consolidation → knowledge is updated

**Typical timeline**: This is the long-term vision. Expect 2–3 quarters of progressive maturation after L4.

---

## Choosing Your Starting Level

| Your situation | Start at |
|---------------|----------|
| No specs, no structured knowledge | **L1** |
| Some specs exist but no validation | **L2** |
| Specs + CI validation in place | **L3** |
| Already using AI for code generation | **L4** |
| Full knowledge graph + agent tooling | **L5** |

Most teams should start at **L1** and progress to **L2** within the first month. L3+ depends on tooling investment and team maturity.
