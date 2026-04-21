# Guide: Consolidation — Closing the Work → Knowledge Loop

Consolidation is the process by which **completed work feeds back into organizational knowledge**. Without it, teams learn things during implementation that never make it back into specs — and the next team starts from scratch.

```
Knowledge ──activates──→ Work ──consolidates──→ Knowledge (updated)
```

> For the theoretical foundation, see the Consolidation section in [unified-taxonomy.md](../../knowledge-architecture/unified-taxonomy.md). For the Evolutive pillar, see [pillars.md](../../foundation/pillars.md).

## When to Consolidate

Consolidation happens when a WRK-SPEC moves to `completed` status. It's part of the definition of done — work isn't truly done until knowledge is updated.

## The Consolidation Checklist

Run through this checklist when closing a WRK-SPEC:

### 1. Architecture Decisions → ADRs

**Ask**: *"Did we make any significant technical decisions during this work?"*

If yes, write an ADR for each. Common triggers:
- Chose between competing approaches
- Rejected the originally planned approach
- Discovered a constraint not captured in existing specs
- Made a trade-off that future teams should know about

> See [governance-cycle.md](governance-cycle.md) for ADR format.

### 2. Domain Learnings → Updated Knowledge Specs

**Ask**: *"Did we discover domain rules, edge cases, or invariants not captured in existing DOM specs?"*

If yes:
- **Minor additions**: Update the existing DOM spec (bump version, add the rule)
- **New subdomain**: Create a new DOM spec
- **Correction**: Update the existing spec and note the correction in the Evidence section

### 3. Architecture Patterns → Updated ARCH Specs

**Ask**: *"Did we establish patterns that should be reused?"*

If yes:
- Update the relevant ARCH spec, or
- Create a new ARCH spec if the pattern is novel
- Create a RULE if the pattern should be mandatory

### 4. Product/Feature Insights → Updated PROD/FEAT Specs

**Ask**: *"Did we learn something about user needs or product behavior?"*

This is less common but valuable:
- Updated acceptance criteria based on user testing
- New non-functional requirements discovered during load testing

### 5. Open Questions → Resolved or Escalated

**Ask**: *"Were all open questions from the WRK-SPEC answered?"*

- Answered → Capture the answer in the appropriate Knowledge Artifact
- Still open → Escalate: create an RFC or a new WRK-SPEC to investigate

## Example: VaR Engine Redesign Consolidation

After completing `WRK-SPEC-001` (VaR Engine Redesign):

| Discovery | Action | Artifact |
|-----------|--------|----------|
| Partitioning by asset class outperformed partitioning by portfolio | Write ADR | ADR-003: Partition Strategy for VaR Computation |
| Cache invalidation requires event-driven TTL, not time-based | Update ARCH-002 | Add cache invalidation pattern to event-driven architecture spec |
| Regulatory VaR requires specific rounding rules not in DOM-RISK-001 | Update DOM-RISK-001 | Add rounding rules section, bump to v1.2.0 |
| Shadow mode comparison revealed 0.01% precision divergence is acceptable | Write RULE | RULE-005: Acceptable VaR Precision Tolerance |
| Intraday recalculation question still open | Create new work | WRK-SPEC-002: Intraday VaR Recalculation |

## Consolidation Workflow

```
1. WRK-SPEC marked as completed
     │
2. Review each WRK-TASK's implementation notes
     │
3. Run through consolidation checklist (above)
     │
4. Create/update Knowledge and Governance artifacts
     │
5. Validate the knowledge graph
     │  node apps/spec-graph/spec-graph.mjs --specs <dir> validate
     │
6. Archive the Work Artifacts (status → archived)
     │
7. PR with all changes — link to the completed WRK-SPEC
```

## Tips

- **Don't skip this step.** It's tempting to move on to the next feature. Block 1–2 hours for consolidation at the end of each WRK-SPEC.
- **The tech lead owns consolidation**, even if developers contribute. The lead has the best view of what was learned.
- **Small, frequent consolidation is better** than a big batch at the end of a quarter. If a WRK-TASK reveals something important, update knowledge immediately — don't wait for the WRK-SPEC to complete.
- **Use confidence levels**: New knowledge from consolidation typically starts at `medium` (validated by implementation but not yet reviewed by broader team). Schedule a review to promote to `high`.
