---
id: ISS-014
type: issue
title: Starter ADRs reference issue IDs that do not exist in this vault
status: open
created: 2026-09-09
updated: 2026-09-09
sources: []
related:
  - "[[ISS-016-moore-format-cited-without-an-anchor]]"
  - "[[ISS-009-real-time-metric-untestable]]"
  - "[[ISS-010-system-boundary-undefined]]"
tags: [issue]
severity: minor
kind: question
raised-by: agent
resolved: null
---

# Starter ADRs reference issue IDs that do not exist in this vault

**What's unresolved.** Several shipped ADRs cite `ISS-` pages from the
*starter's own* development history — about placeholder actors ("Role A",
"Role C", "System X") and features this project does not have. Those pages were
never shipped in this vault, so the links are broken, and the numbers they use
have now been re-issued to real eTSU issues.

**Affects.** Link hygiene in `_system/adr/`; the meaning of a bare "ISS-NNN"
reference across the vault.

**Context / evidence.**

| Referenced by | Dangling target | Number now used by |
|---|---|---|
| `ADR-0017` | `ISS-009-worklist-stub-strategy` | [[ISS-009-real-time-metric-untestable]] |
| `ADR-0013`, `ADR-0018` | `ISS-010-context-diagram-projection-audit-loop` | [[ISS-010-system-boundary-undefined]] |
| `ADR-0014` | `ISS-011` (bare, "two planning roles") | [[ISS-011-context-flows-inferred-not-sourced]] |
| `ADR-0020` | `ISS-016-remove-active-soft-delete` | [[ISS-016-moore-format-cited-without-an-anchor]] |

Filenames differ, so Obsidian resolves nothing incorrectly — the links are
simply dead. The residual cost is that the string "ISS-010" means two things
depending on which document you are reading.

The numbering was **not** worked around during ingest: skipping IDs to dodge
references belonging to a different vault's history would leave permanent gaps
in this project's sequence for no gain.

**Options.**
1. Leave the ADR text as-is — it is an imported decision record and rewriting
   history is worse than a dead link. Add a one-line note at the top of
   `_system/adr/README` (or `ADR-0001`) explaining that pre-eTSU ADRs may cite
   issues from the starter's own development. Recommended.
2. Strip the dangling wikilinks from the starter ADRs, leaving plain text.
3. Renumber this vault's issues to start above `ISS-016`. Not recommended —
   churns every link written so far to solve a cosmetic problem.

**Resolution.** *Open.*
