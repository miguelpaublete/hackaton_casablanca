# Pattern: Building a Vertical Taxonomy

How to construct a domain taxonomy for your industry vertical, enabling structured knowledge organization and activation.

> For an example taxonomy, see [CIB Taxonomy](../../examples/verticals/cib-taxonomy.md). For the knowledge architecture context, see [unified-taxonomy.md](../../knowledge-architecture/unified-taxonomy.md).

## What is a Vertical Taxonomy?

A vertical taxonomy is a **hierarchical organization of domains and subdomains** specific to an industry. It provides the naming structure for spec IDs and the browsing structure for knowledge discovery.

```
Vertical (e.g., CIB)
├── Functional Domain (e.g., Markets & Trading)
│   ├── Subdomain (e.g., Risk Management)
│   │   ├── DOM-RISK-001
│   │   ├── DOM-RISK-002
│   │   └── ...
│   └── Subdomain (e.g., Post-Trade)
│       └── ...
└── Functional Domain (e.g., Corporate Banking)
    └── ...
```

## Why Build One?

Without a taxonomy:
- Spec IDs are inconsistent (`DOM-001` vs `DOM-VaR-001` vs `DOMAIN-RISK-VaR`)
- Knowledge is hard to discover ("where are the risk rules?")
- Activation is guesswork ("which specs are relevant to this feature?")

With a taxonomy:
- Consistent naming: `DOM-RISK-001` immediately tells you it's a domain spec in the risk subdomain
- Discoverable: browse by functional domain to find all related specs
- Activatable: activate an entire subdomain when working in that area

## Step-by-Step: Creating Your Taxonomy

### Step 1: Identify Functional Domains

Start with the highest-level business areas. Aim for 3–6 top-level domains.

**Approach**: Ask business stakeholders: *"What are the major areas of our business?"*

Example for insurance:
```
Insurance
├── Underwriting
├── Claims
├── Policy Administration
├── Distribution
├── Actuarial
└── Regulatory & Compliance
```

### Step 2: Decompose into Subdomains

Each functional domain breaks into subdomains. Aim for 3–8 subdomains per domain.

**Approach**: Ask domain experts: *"Within [domain], what are the distinct capability areas?"*

```
Claims
├── First Notice of Loss (FNOL)
├── Claims Assessment
├── Fraud Detection
├── Settlement
└── Subrogation
```

### Step 3: Add Cross-Cutting Capabilities

Most verticals have shared capabilities that span multiple domains:

```
Cross-Cutting
├── Client Lifecycle (KYC, onboarding)
├── Regulatory & Compliance
├── Data Management
└── Operations
```

### Step 4: Define the Technical Domain Tree

This tree is **shared across verticals** — it describes technical patterns, not business domains:

```
Technical
├── Architecture Patterns (application, integration, data, security)
├── NFR Catalog (performance, reliability, security, operability)
├── Technology Standards (languages, platforms, data stores)
└── Quality Standards (code, API, testing, documentation)
```

### Step 5: Create the Activation Matrix

Map which knowledge layers are most relevant at each phase of work:

| Phase | Primary | Secondary |
|-------|---------|-----------|
| Requirements | DOM (business rules), PROD (vision) | ARCH (constraints) |
| Design | ARCH (patterns), DOM (invariants) | PROD, FEAT |
| Build | FEAT (behavior), DOM (rules) | ARCH (patterns) |
| Test | DOM (acceptance), FEAT (behavior) | ARCH (NFRs) |
| Deploy | ARCH (infrastructure) | DOM (operational rules) |

## Taxonomy Template

Use this template for your vertical:

```markdown
# [Vertical Name] Taxonomy

## Functional Domain Tree

### [Domain 1]
- [Subdomain 1.1]: Brief description
- [Subdomain 1.2]: Brief description
- [Subdomain 1.3]: Brief description

### [Domain 2]
- [Subdomain 2.1]: Brief description
- ...

### Cross-[Vertical] Capabilities
- [Shared Capability 1]: Brief description
- [Shared Capability 2]: Brief description

## Business Rules Catalog

| Category | Examples | Typical Source |
|----------|----------|---------------|
| Validation | Input constraints, format rules | Product + compliance |
| Calculation | Formulas, algorithms, rounding | Domain experts |
| Workflow | State machines, approval chains | Operations |
| Regulatory | Mandatory checks, reporting | Legal + compliance |

## Technical Domain Tree
(Use the standard tree — shared across verticals)

## Activation Matrix
(Map knowledge layers to work phases for this vertical)
```

## Tips

- **Start coarse, refine later.** A 3-domain taxonomy that the team uses is better than a 20-domain taxonomy nobody maintains.
- **Validate with domain experts.** The taxonomy should match how the business thinks, not how the code is organized.
- **Spec IDs follow the taxonomy.** `DOM-RISK-001` is in the Risk Management subdomain. If a spec doesn't fit the taxonomy, either the spec scope is wrong or the taxonomy needs updating.
- **Expect evolution.** The taxonomy will change as you learn. That's fine — update it, rename subdomains, and reorganize. Use `supersedes` for spec ID changes.
- **One vertical at a time.** If your organization spans multiple verticals (e.g., banking + insurance), create separate taxonomy files. Share the Technical Domain Tree.
