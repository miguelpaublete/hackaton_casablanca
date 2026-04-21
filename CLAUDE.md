# CLAUDE.md — Knowledge-Driven Development Framework

## Project Context

This is the **canonical framework** for Knowledge-Driven Development (KDD). It consolidates and supersedes:
- `AI4Arquitecture/KID_v2.md` — Strategic/commercial vision (KID)
- `AI4Modernization/core/spec-driven-approach/methodology.md` — Technical operationalization

Those documents remain as historical references. This project is the single source of truth.

## Language

English. This framework targets international delivery teams and multi-geography clients.

## Structure

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
├── docs/                        # Operational documentation
│   ├── getting-started.md       # Entry point for new adopters
│   ├── guides/                  # How-to guides (create specs, plan work, governance)
│   ├── reference/               # Quick lookup (artifact matrix, checklists, adoption levels)
│   └── patterns/                # Recipes (brownfield, vertical taxonomy, spec-as-prompt)
│
├── examples/specs/              # Example Knowledge Artifacts (CIB domain)
├── examples/work/               # Example Work Artifacts (WRK-SPEC, WRK-PLAN, WRK-TASK)
└── examples/verticals/          # Vertical taxonomy examples (CIB)
```

## Conventions

- All documents are Markdown
- Formal contracts use native formats: OpenAPI, AsyncAPI, JSON Schema
- Spec IDs follow the pattern: `TYPE-AREA-NNN` (e.g., `DOM-RISK-001`) for Knowledge Artifacts, `WRK-TYPE-NNN` (e.g., `WRK-SPEC-001`) for Work Artifacts
- Confidence levels: HIGH / MEDIUM / LOW
- Status lifecycle: Draft → Active → Deprecated (knowledge specs), Draft → Active → Completed → Archived (work specs), Proposed → Accepted → Superseded (ADRs)
- Three artifact axes: Knowledge (persistent), Work (ephemeral), Governance (bridge) — see `knowledge-architecture/unified-taxonomy.md`

## Working with this framework

When creating or updating specs:
1. Check `knowledge-architecture/spec-anatomy.md` for the standard structure
2. Use the correct spec type from `knowledge-architecture/spec-types.md`
3. Place domain knowledge according to the vertical taxonomy (see `examples/verticals/cib-taxonomy.md` for CIB)
4. Ensure YAML frontmatter is complete and valid
5. Run `node apps/spec-graph/spec-graph.mjs --specs <dir> validate` to check integrity

## Knowledge Graph CLI

Install: `cd apps/spec-graph && npm install && cd ../..`

```bash
node apps/spec-graph/spec-graph.mjs --specs <dir> <command> [options]
```

Commands: `build [--html]`, `visualize`, `impact <id>`, `orphans`, `validate`, `stats`, `filter`, `path <a> <b>`, `context <id> [--depth N]`.

See [README.md](README.md#knowledge-graph-cli) for full command reference and programmatic library API.

## Claude Code Slash Commands

- `/spec-graph <command> [args]` — Query the knowledge graph inline (impact, filter, path, context, etc.)
- `/spec-context <task description>` — Contextual activation: find relevant specs for a task, read them, and synthesize a brief. Implements the Agentic pillar pattern.

## Vertical focus

The initial taxonomy is detailed for **CIB (Corporate & Investment Banking)**. Other verticals (Retail Banking, Insurance, Telco, Utilities) will be added as extensions.
