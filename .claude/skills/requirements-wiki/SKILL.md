---
name: requirements-wiki
description: >
  Build and maintain a software-systems requirements wiki using the Karpathy
  LLM-wiki pattern on an Obsidian vault. Use whenever the user wants to ingest a
  source (interview, transcript, spec, ticket) into requirements knowledge, audit
  the wiki for contradictions/gaps/stale claims, report on requirements (open
  issues, coverage, stakeholder matrix, quality scenarios, traceability), or
  bootstrap a new requirements vault. Triggers: "ingest this into the wiki",
  "audit the requirements", "what open issues do we have", "requirements
  coverage", mentions of glossary/ubiquitous language, stakeholders/personas, use
  cases, user stories, features, quality requirements, constraints. Content types:
  glossary term, stakeholder, data model, activity model, use case, user story,
  feature, quality requirement, constraint, and issue (a first-class meta-type).
---

# Requirements Wiki

Operate a requirements knowledge base built on the Karpathy LLM-wiki pattern:
**compile knowledge once into a persistent, interlinked wiki and keep it current**,
rather than re-deriving from raw sources on every query.

## First: locate the vault and read its schema

1. Find the vault root (the directory containing `CLAUDE.md`, `raw/`, `wiki/`,
   `_templates/`, `_system/`). Walk up from the working directory if needed.
2. **Read the vault's `CLAUDE.md`** — it is authoritative for structure, content
   types, ID scheme, and conventions. This skill is the procedure; `CLAUDE.md` is
   the data-specific schema. If they ever disagree, `CLAUDE.md` wins.
3. Read the relevant procedure in `_system/workflows/` before running it.

If no vault exists and the user wants one, scaffold it: create the layer folders and
copy the canonical `_templates/` and `_system/anchors/` from an existing vault (or
recreate them from `CLAUDE.md`'s schema), then write `CLAUDE.md` and `_system/`.

## Core discipline (applies to every operation)

- Apply `_system/anchors/` standards and cite them: goals via [[SMART]] or [[PAM]],
  stories via [[user-story-format]] + [[INVEST]], priorities via [[MoSCoW]].
  Enforcement is advisory — flag misfits as Issues, don't block or rewrite.
- One file per unit, ID `TYPE-NNN`, filename `TYPE-NNN-kebab-title.md`, frontmatter
  from the matching `_templates/` file. IDs are stable, never reused.
- Cross-reference with Obsidian wikilinks `[[FEAT-002-checkout]]` — never bare prose.
- Link every derived claim to its source in `sources:`.
- **Never silently resolve a contradiction or judgment call.** Raise an `ISS-NNN`
  Issue linking both sides and present options. Issues are a content type in
  `wiki/issues/` like any other; there is no standing dashboard — produce an
  open-issues report on demand.
- Keep `_system/index.md` and `_system/log.md` current. Log prefix is exact:
  `## [YYYY-MM-DD] <op> | <subject>`.

## Operations (full steps in `_system/workflows/`)

- **Ingest** — source → typed pages. **Mandatory first:** activate the
  `grill-requirements` skill and stress-test the source before writing anything —
  ingest is gated on this pass (see `_system/workflows/ingest.md`). Then capture
  provenance (`SRC-NNN` + sha256), read, discuss takeaways, extend-don't-duplicate,
  write pages, flag issues, update index, append log. Expect 8–15 pages touched.
- **Audit** — health-check: contradictions, stale claims, orphans, broken links,
  untestable quality requirements, unsourced claims, source drift, coverage gaps.
  Auto-fix only mechanical issues; queue judgment calls as Issues.
- **Report** — derive a view (open issues, coverage, stakeholder matrix, quality
  scenarios, glossary, traceability). File lasting reports back as wiki pages.

## Domain conventions

- **The ubiquitous language is English** ([[0005-ubiquitous-language-english|ADR-0005]]).
  Write every requirement page in English; converse/ask in any language that suits
  the human, but capture content in English. `_system/anchors/` and machinery stay
  English too.
- Glossary = DDD ubiquitous language; one canonical meaning per bounded context.
- Quality requirements use ISO 25010 attributes + an ATAM scenario
  (source/stimulus/environment/response/**measure**). No measure ⇒ `testable: false`
  ⇒ Issue.
- Constraints follow arc42 categories (technical/organizational/legal/...).
- Stakeholders are simplified personas rated on influence × interest.
