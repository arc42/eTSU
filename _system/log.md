# Log

Append-only. One entry per operation. Keep the prefix exact so the log is
greppable: `grep '^## \[' _system/log.md | tail -5`.

<!-- Format:
## [YYYY-MM-DD] ingest | <source title>
- created: GLO-004, STK-002, UC-007
- updated: _system/index.md, FEAT-001
- issues: ISS-003 (contradiction: SLA target vs CON-002)
-->

## [2026-09-06] bootstrap | eTSU
- system_name kept as "eTSU" (matches the brief's own wording); tagline set to "Combining Art, AI and Requirements"
- ubiquitous language confirmed as English (ADR-0005 unchanged)
- created: GOAL-001 (vision), GLO-001 (Tour), GLO-002 (Show), STK-001 (Gus Renoir)
- updated: _system/wiki.yaml, _system/index.md
- next: `raw/TSU-brief.md.md` is sitting in the inbox — proceed with the normal, grill-gated `ingest.md` pass
