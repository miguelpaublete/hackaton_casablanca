# Guide: Create a Knowledge Spec

Knowledge Artifacts capture persistent organizational knowledge — architecture decisions, domain rules, product vision, feature definitions, and documentation. They outlive any single project.

## Step 1: Choose the Type and Layer

| Layer | Type ID | Use when... | Example |
|-------|---------|-------------|---------|
| Architecture | `ARCH` | Defining cross-cutting technical decisions | Event-driven architecture, API gateway pattern |
| Domain | `DOM` | Capturing business rules and domain logic | VaR calculation rules, transfer limits |
| Product | `PROD` | Describing product-level capabilities | Portfolio analytics platform vision |
| Feature | `FEAT` | Specifying a concrete feature | Real-time P&L dashboard |
| Documentation | `DOC` | Recording conventions, guides, standards | API naming conventions, onboarding guide |

**Decision heuristic:**
- If it constrains many features → `ARCH`
- If a domain expert owns it → `DOM`
- If a product owner owns it → `PROD`
- If it describes user-facing behavior → `FEAT`
- If it explains how to do something → `DOC`

> Full type definitions: [spec-types.md](../../knowledge-architecture/spec-types.md)

## Step 2: Create the Frontmatter

```yaml
---
id: DOM-RISK-001              # TYPE-AREA-NNN
type: knowledge               # always "knowledge" for this axis
layer: domain                 # architecture | domain | product | feature | documentation
title: Market Risk Calculation (VaR)
status: draft                 # draft → active → deprecated
confidence: medium            # low | medium | high
version: "0.1.0"
owner: risk-analytics-team
domain: markets               # functional domain
subdomain: risk-management    # subdomain within the vertical
tags: [var, market-risk, regulatory]
dependencies:
  - id: ARCH-002
    type: constrained-by      # implements | constrained-by | extends | uses-data-from
  - id: DOM-REG-001
    type: implements
reviewers: []                 # populated during review
---
```

### Required fields

| Field | Description |
|-------|-------------|
| `id` | Unique identifier: `TYPE-AREA-NNN` |
| `type` | Always `knowledge` |
| `layer` | One of: `architecture`, `domain`, `product`, `feature`, `documentation` |
| `title` | Human-readable title |
| `status` | `draft` → `active` → `deprecated` |
| `confidence` | `low` (inferred), `medium` (validated OR reviewed), `high` (validated AND reviewed) |
| `version` | Semver string |
| `owner` | Team or person responsible |

### Optional fields

| Field | Description |
|-------|-------------|
| `domain` | Functional domain from your vertical taxonomy |
| `subdomain` | Subdomain within the domain |
| `dependencies` | List of `{id, type}` pairs |
| `reviewers` | List of reviewers |
| `tags` | Free-form tags for discovery |
| `supersedes` | ID of the spec this replaces |

> Full frontmatter reference: [spec-anatomy.md](../../knowledge-architecture/spec-anatomy.md)

## Step 3: Write the Body

Every Knowledge spec follows this structure:

### Intent

*Why does this spec exist? What problem does it solve?*

Keep it to 2–3 sentences. This is the most important section — if someone reads nothing else, they should understand the purpose.

### Definition

*The actual content.* Structure depends on the layer:

- **ARCH**: Decision, rationale, consequences, alternatives considered
- **DOM**: Rules, invariants, calculations, data models
- **PROD**: Capabilities, user outcomes, success metrics
- **FEAT**: User stories, behavior, UI/UX requirements
- **DOC**: Procedures, conventions, standards

Use tables, diagrams, and code blocks to make rules unambiguous.

### Acceptance Criteria

*How do we know this spec is correctly implemented?*

Write as a checklist. Each criterion should be independently verifiable.

```markdown
## Acceptance Criteria

- [ ] VaR engine computes 1-day VaR at 95% confidence
- [ ] Historical simulation uses 250-business-day window
- [ ] Position-level risk attribution is available
```

### Evidence

*What validates this spec?*

- Test results, regulatory references, expert sign-offs
- Link to external documents or systems where applicable

### Traceability

*How does this spec connect to others?*

- Which specs depend on this one
- Which work artifacts have implemented it

> This section is often auto-populated by tooling at L2+.

## Step 4: Declare Dependencies

Dependencies express how specs relate. Use the right relation type:

| Relation | Meaning | Example |
|----------|---------|---------|
| `implements` | This spec implements a higher-level spec | FEAT implements PROD |
| `constrained-by` | This spec must respect constraints from another | DOM constrained-by ARCH |
| `extends` | This spec adds detail to another at the same layer | DOM-RISK-002 extends DOM-RISK-001 |
| `uses-data-from` | This spec consumes data defined in another | FEAT uses-data-from DOM |
| `depends-on` | Generic dependency | Any layer |
| `supersedes` | This spec replaces another | New version of a deprecated spec |

## Step 5: Validate

Run the CLI validator to check frontmatter integrity and dependency resolution:

```bash
node apps/spec-graph/spec-graph.mjs --specs <your-specs-dir> validate
```

Fix any errors before proceeding. Common issues:
- Missing required frontmatter fields
- Dependencies referencing non-existent spec IDs
- Invalid status or confidence values

## Step 6: PR Review

Before submitting, run through the [spec checklist](../reference/spec-checklist.md).

In the PR:
- Explain *why* this spec exists (not just what it contains)
- Tag the `owner` and relevant `reviewers`
- If this spec changes dependencies, note the impact (use `spec-graph impact <id>`)

After merge, update `confidence` based on review outcome:
- Reviewed + validated → `high`
- Reviewed OR validated → `medium`
- Neither → `low`
