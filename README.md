# Knowledge-Driven Development Framework

> The key is not just "specs before code" but **what knowledge to structure and how to activate it contextually**.

Knowledge-Driven Development (KDD) is a methodology that establishes structured specifications as the universal interface between discovery, design, and implementation — for both human developers and AI agents.

---

## What's Different

Current SDD approaches (GitHub Spec Kit, Kiro, Tessl) bring valuable spec-first workflows. This framework adds five differentiators:

1. **Domain knowledge taxonomy** — structured functional and technical knowledge for specific industries
2. **Contextual activation** — the right knowledge surfaces at the right SDLC phase
3. **Layered specification hierarchy** — five knowledge layers + three work layers with governance, confidence levels, and lifecycle management
4. **Industry-specific depth** — starting with CIB (Corporate & Investment Banking), extensible to other verticals
5. **Unified three-axis taxonomy** — Knowledge (persistent), Work (ephemeral), and Governance (bridge) as orthogonal axes, connected by contextual activation

---

## Three Pillars

| Pillar | Question | Core idea |
|--------|----------|-----------|
| **Spec-Driven** | How do we structure knowledge? | Everything as structured, versioned specs |
| **Evolutive** | How does knowledge grow? | Every project delivers knowledge back |
| **Agentic** | How do we amplify capabilities? | AI agents operate on specs, not ad-hoc prompts |

## Three Artifact Axes

| Axis | Artifacts | Persistence |
|------|----------|-------------|
| **Knowledge** | ARCH, DOM, PROD, FEAT, DOC | Persistent — organizational |
| **Work** | WRK-SPEC, WRK-PLAN, WRK-TASK | Ephemeral — scoped to a change |
| **Governance** | RFC, ADR, RULE | Mixed — decisions persist |

---

## Framework Structure

```
spec-driven/
├── foundation/                  # Layer 1: Strategic foundations
│   ├── manifesto.md             # The "why" — problems + thesis
│   ├── pillars.md               # 3 pillars: Spec-Driven, Evolutive, Agentic
│   └── principles.md            # 4 design principles
│
├── knowledge-architecture/      # Layer 2: Knowledge architecture
│   ├── unified-taxonomy.md      # ★ Three-axis taxonomy: Knowledge + Work + Governance
│   ├── spec-types.md            # Artifact types + governance lifecycle
│   └── spec-anatomy.md          # Standard spec structure + YAML frontmatter
│
├── apps/                        # Applications
│   └── spec-graph/              # Knowledge graph CLI + library
│       ├── spec-graph.mjs       # CLI (thin wrapper)
│       ├── spec-graph-lib.mjs   # Core library (importable pure functions)
│       ├── spec-graph-viewer.html # Interactive D3.js graph viewer
│       └── package.json         # Dependencies (commander, gray-matter)
│
├── examples/
│   ├── specs/                   # Knowledge Artifacts — 21 CIB domain specs
│   │   ├── architecture/        # ARCH-001..004
│   │   ├── domain/              # DOM-RISK-001, DOM-TRADE-001, etc.
│   │   ├── product/             # PROD-FX-001, PROD-EQ-001, etc.
│   │   ├── feature/             # FEAT-RISK-001, FEAT-TRADE-001, etc.
│   │   └── documentation/       # DOC-API-001
│   ├── work/                    # Work Artifacts — VaR engine redesign
│   │   ├── WRK-SPEC-001-var-engine-redesign.md
│   │   ├── WRK-PLAN-001-var-engine-redesign.md
│   │   ├── WRK-TASK-001-var-calculation-service.md
│   │   └── WRK-TASK-002-var-api-endpoint.md
│   └── verticals/               # Vertical taxonomy examples
│       └── cib-taxonomy.md      # CIB functional + technical domain trees
│
└── _build/                      # Derived artifacts (gitignored)
```

> Future layers planned: `sdlc-integration/` (SDLC phase integration), `ai-augmentation/` (spec-as-prompt patterns, agents).

### Layer 1: Foundation — *Why and What*

| Document | Content |
|----------|---------|
| [Manifesto](foundation/manifesto.md) | The double problem (fragmented knowledge + AI without methodology), positioning vs. alternatives, our thesis |
| [Pillars](foundation/pillars.md) | Three pillars — Spec-Driven, Evolutive, Agentic |
| [Principles](foundation/principles.md) | Four design principles — Everything as Code, Layered Hierarchy, Universal Applicability, Incremental Adoption |

### Layer 2: Knowledge Architecture — *How Knowledge is Organized*

| Document | Content |
|----------|---------|
| [Unified Taxonomy](knowledge-architecture/unified-taxonomy.md) | **Three-axis architecture.** Knowledge + Work + Governance axes, artifact map, activation matrices, contextual activation mechanics, differential advantages |
| [Spec Types](knowledge-architecture/spec-types.md) | All artifact types (RFC, SPEC, ADR, Guide, Template, Rule), 5 knowledge layers, 3 work layers, governance cycle, confidence levels |
| [Spec Anatomy](knowledge-architecture/spec-anatomy.md) | Standard spec structure, YAML frontmatter schema, dependency relations, complete example (DOM-RISK-001) |

### Examples

| Directory | Content | Count |
|-----------|---------|-------|
| [`examples/specs/`](examples/specs/) | Knowledge Artifacts — CIB domain (ARCH, DOM, PROD, FEAT, DOC) | 21 specs |
| [`examples/work/`](examples/work/) | Work Artifacts — VaR engine redesign (WRK-SPEC → WRK-PLAN → WRK-TASK) | 4 specs |
| [`examples/verticals/`](examples/verticals/) | Vertical taxonomies — CIB functional & technical domain trees | 1 vertical |

---

## Documentation

For operational guides on how to adopt and use KDD in your team, see **[docs/getting-started.md](docs/getting-started.md)**.

| Section | What it covers |
|---------|---------------|
| [Getting Started](docs/getting-started.md) | Entry point — your first spec in 10 minutes |
| [Guides](docs/guides/) | Step-by-step: create specs, plan work, govern changes |
| [Reference](docs/reference/) | Quick lookup: artifact matrix, checklists, adoption levels |
| [Patterns](docs/patterns/) | Recipes: brownfield adoption, vertical taxonomies, spec-as-prompt |

---

## Quick Start

```bash
# 1. Install dependencies
cd apps/spec-graph && npm install && cd ../..

# 2. Validate all examples (knowledge + work artifacts)
node apps/spec-graph/spec-graph.mjs --specs examples validate

# 3. View stats — specs by layer, domain, confidence, relation types
node apps/spec-graph/spec-graph.mjs --specs examples stats

# 4. Build interactive graph viewer
node apps/spec-graph/spec-graph.mjs --specs examples build --html
open _build/graph.html

# 5. Impact analysis — what's affected if VaR rules change?
node apps/spec-graph/spec-graph.mjs --specs examples impact DOM-RISK-001

# 6. Contextual activation — get the knowledge bundle for a spec
node apps/spec-graph/spec-graph.mjs --specs examples context WRK-SPEC-001 --depth 2
```

---

## Knowledge Graph CLI

The spec frontmatters **are** the graph — distributed across files. The `spec-graph` CLI derives a queryable graph at build-time.

| Command | Description |
|---------|-------------|
| `build` | Generate `_build/graph.json` (add `--html` for interactive D3.js viewer) |
| `visualize` | Generate `_build/graph.mermaid` diagram |
| `impact <id>` | Transitive impact analysis — what specs are affected by a change |
| `orphans` | List specs with no inbound or outbound edges |
| `validate` | Integrity check — broken refs, duplicates, cycles (CI gate) |
| `stats` | Metrics overview — specs by layer, domain, confidence |
| `filter` | Filter specs by `--layer`, `--domain`, `--confidence`, `--status`, `--tag` |
| `path <a> <b>` | Shortest path between two specs |
| `context <id>` | Contextual activation bundle (`--depth N` for broader traversal) |

All commands accept `--specs <dir>` to specify the specs directory (default: current directory).

```bash
node apps/spec-graph/spec-graph.mjs --specs <dir> <command> [options]
```

### Programmatic Library

The core functions are exported from `apps/spec-graph/spec-graph-lib.mjs` for integration into custom tools:

| Function | Purpose |
|----------|---------|
| `scanSpecs(dir)` / `buildGraph(dir)` | Parse specs into graph |
| `impactBFS(id, edges, nodes)` | Transitive impact analysis |
| `filterSpecs(graph, criteria)` | Composable filtering (AND logic) |
| `findPath(from, to, edges, nodes)` | Shortest path (BFS) |
| `buildContext(id, graph, { depth })` | Contextual activation bundle |
| `findOrphans`, `validateGraph`, `detectCycles` | Graph integrity checks |
| `generateMermaid` | Mermaid diagram generation |
| `LAYER_COLORS`, `INVERSE_RELATIONS` | Constants for visualization and enrichment |

---

## Five Knowledge Layers

| Layer | ID Pattern | Scope |
|-------|-----------|-------|
| Architecture | `ARCH-NNN` | Patterns, decisions, infrastructure |
| Domain | `DOM-AREA-NNN` | Business rules, regulations |
| Product | `PROD-JOURNEY-NNN` | User journeys, flows |
| Feature | `FEAT-MODULE-NNN` | Specific functionality |
| Documentation | `DOC-TYPE-NNN` | Guides, runbooks |

## Governance Cycle

```
RFC (propose) → SPEC (formalize) → ADR (decide & learn)
     ↑                                      │
     └──────────── feedback loop ───────────┘
```

---

## Vertical Focus

The initial taxonomy is detailed for **CIB (Corporate & Investment Banking)**. Planned extensions:

- **Retail Banking** — Channels, products (deposits, cards, loans), customer journeys
- **Insurance** — Underwriting, claims, actuarial, distribution
- **Telco** — Network, BSS/OSS, customer management, billing
- **Utilities** — Grid management, metering, billing, regulatory compliance

---

## External References

- **Thoughtworks Technology Radar 2025** — Spec-Driven Development as key practice
- **GitHub Spec Kit** — Specify → Plan → Tasks → Implement workflow
- **Martin Fowler / Böckeler** — Kiro, Spec Kit, Tessl; spec-first vs. spec-as-source levels
- **ICSE 2026** — Architectural specs improve LLM-generated code quality
