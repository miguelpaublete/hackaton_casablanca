# Spec Checklist (Pre-PR)

Use this checklist before submitting a spec for review. Based on the validation rules in [spec-anatomy.md](../../knowledge-architecture/spec-anatomy.md).

## Frontmatter

- [ ] `id` is present and follows the pattern (`TYPE-AREA-NNN` or `WRK-TYPE-NNN`)
- [ ] `type` is one of: `knowledge`, `work`, `governance`
- [ ] `layer` matches the type (e.g., `domain` for knowledge, `spec` for work)
- [ ] `title` is present and descriptive
- [ ] `status` is a valid lifecycle value for the type
- [ ] `confidence` is set (knowledge artifacts only): `low`, `medium`, or `high`
- [ ] `version` is present and follows semver
- [ ] `owner` is set to a real team or person

## Dependencies

- [ ] Every `dependencies[].id` references an existing spec
- [ ] Every `dependencies[].type` uses a valid relation: `implements`, `constrained-by`, `extends`, `uses-data-from`, `depends-on`, `supersedes`
- [ ] No circular dependencies
- [ ] Relations make semantic sense (e.g., FEAT doesn't constrain ARCH)

## Work Artifacts (additional checks)

- [ ] `activates` lists at least one Knowledge Artifact (for WRK-SPEC)
- [ ] `parent` is set and references an existing Work Artifact (for WRK-PLAN and WRK-TASK)
- [ ] `scope` is defined with `includes`/`excludes` (for WRK-TASK, when applicable)

## Body Sections

### Knowledge Artifacts

- [ ] **Intent** section explains *why* the spec exists
- [ ] **Definition** section contains the actual specification
- [ ] **Acceptance Criteria** section has testable items
- [ ] **Evidence** section references validation sources

### Work Artifacts

- [ ] **Problem Statement** (WRK-SPEC) or **Objective** (WRK-TASK) is clear
- [ ] **Activated Knowledge** section explains why each activated spec is relevant (WRK-SPEC)
- [ ] **Task Decomposition** lists all WRK-TASKs with estimates (WRK-PLAN)
- [ ] **Acceptance Criteria** are specific and testable

### Governance Artifacts

- [ ] **Context** explains the situation (RFC, ADR)
- [ ] **Decision/Proposal** is clearly stated
- [ ] **Rationale** explains the reasoning
- [ ] **Alternatives Considered** are documented (RFC, ADR)

## Validation

- [ ] CLI validation passes:
  ```bash
  node apps/spec-graph/spec-graph.mjs --specs <dir> validate
  ```
- [ ] No orphaned specs (no incoming or outgoing dependencies without justification):
  ```bash
  node apps/spec-graph/spec-graph.mjs --specs <dir> orphans
  ```

## Review Readiness

- [ ] PR description explains *why* this spec exists, not just what it contains
- [ ] `owner` and `reviewers` are tagged
- [ ] If this modifies an existing spec: version is bumped and changes are noted
- [ ] If this supersedes another spec: the old spec is marked `deprecated` and `supersedes` field is set
