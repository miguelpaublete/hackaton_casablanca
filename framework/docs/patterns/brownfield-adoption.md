# Pattern: Brownfield Adoption

How to adopt KDD in an existing project with legacy code, existing documentation, and established practices.

> This pattern implements [Principle 3: Universal Applicability](../../foundation/principles.md) — KDD works for brownfield, greenfield, and hybrid projects.

## The Challenge

Existing projects have:
- Domain knowledge scattered across wikis, Confluence pages, Slack threads, and people's heads
- Architecture decisions that were never recorded
- Code that embodies rules nobody documented
- Teams resistant to "yet another documentation initiative"

## Strategy: Start Where It Hurts

Don't try to document everything. Start with the knowledge that causes the most pain when missing.

### Phase 1: Critical Domain Rules (Weeks 1–2)

**Identify** the 3–5 domain rules that:
- Cause bugs when developers get them wrong
- Require asking a specific person every time
- Are different from what you'd naively assume

**Write** them as DOM specs. Keep them short — capture the rule, not the full context.

```markdown
---
id: DOM-BILLING-001
type: knowledge
layer: domain
title: Pro-Rata Billing Calculation
status: active
confidence: medium
version: "1.0.0"
owner: billing-team
---

## Intent
Define the pro-rata billing formula to prevent recurring billing disputes.

## Definition
Pro-rata amount = (Monthly fee / Days in billing period) × Remaining days
- Billing period is always calendar month
- Remaining days include the activation day
- Round to 2 decimal places, half-up

## Acceptance Criteria
- [ ] Billing service uses this formula for mid-cycle activations
- [ ] Edge case: activation on last day of month = 1 day charge
```

### Phase 2: Architecture Decisions (Weeks 3–4)

**Mine** existing decisions from:
- Git history (look for large refactors, technology changes)
- Meeting notes or Slack archives
- Ask senior team members: "What would a new hire get wrong?"

**Write** them as ADRs (retroactive). You don't need an RFC for decisions already made.

### Phase 3: Validation (Week 5)

- Set up `spec-graph validate` in CI
- Run `spec-graph orphans` to find isolated specs
- Start using `dependencies` to connect specs

At this point you're at **L2** — specs exist, are validated, and are connected.

### Phase 4: Integrate with Workflow (Ongoing)

- New features get a WRK-SPEC that activates relevant DOM/ARCH specs
- Architecture changes go through RFC → ADR
- Bug fixes that reveal undocumented rules produce new DOM specs

## Coexistence with Existing Documentation

KDD doesn't require throwing away existing docs. A practical coexistence strategy:

| Existing format | KDD approach |
|----------------|--------------|
| Confluence/wiki pages | Gradually extract rules into DOM specs. Keep Confluence for narratives and meeting notes. |
| Swagger/OpenAPI files | These are already specs — add ARCH or FEAT frontmatter that references them. |
| Code comments | Extract business rules into DOM specs. Leave implementation comments in code. |
| README files | Keep as project entry points. Add links to specs. |
| Architecture diagrams | Reference from ARCH specs. The spec provides the *why*; the diagram provides the *visual*. |

## Common Objections

**"We don't have time to write specs."**
You're already spending time explaining these rules to new team members, debugging misunderstandings, and re-discovering decisions. Specs trade reactive time for proactive time.

**"Our domain is too complex to capture in specs."**
Start with the 20% of rules that cause 80% of the problems. Specs don't need to be exhaustive — they need to be useful.

**"This is just documentation with extra steps."**
The difference is structure (machine-readable frontmatter), validation (CI checks), and activation (specs feed into work). Regular docs sit in a wiki and rot. Specs live with code and are enforced.

## Anti-Patterns to Avoid

- **Big bang spec-writing sprint**: Don't stop feature work to document everything. Adopt incrementally.
- **Specifying the obvious**: If a rule is clear from the code, it doesn't need a spec. Spec the surprising, complex, or cross-team rules.
- **Gold-plating specs**: A 10-line DOM spec that captures a critical rule is more valuable than a 500-line one that nobody reads.
- **Abandoned specs**: If specs aren't reviewed in PRs and referenced in work, they'll rot. The consolidation loop keeps them alive.

## Measuring Success

After 1 month of adoption:
- [ ] At least 5 critical domain rules are captured as specs
- [ ] New team members reference specs instead of asking Slack
- [ ] At least one bug was caught because a spec existed
- [ ] Architecture decisions from the last quarter have ADRs

After 3 months:
- [ ] CI validates spec integrity
- [ ] WRK-SPECs reference activated knowledge
- [ ] The consolidation habit is forming (work → knowledge updates)
