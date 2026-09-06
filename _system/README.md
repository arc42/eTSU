# _system

Internal machinery for the wiki. Not requirements content — this is *about* the wiki.

- `workflows/` — the operating procedures the agent follows: **ingest**, **audit**
  (content lint), **relations** (graph/link lint), **report**. `CLAUDE.md` points here.
- `adr/` — Architecture Decision Records documenting how this wiki is structured
  and why. Add a new ADR whenever a structural convention changes.
- `anchors/` — reusable methodological standards (SMART, PAM, user-story-format,
  INVEST, MoSCoW) cited across content types. Method, not domain knowledge; see its
  own README.
- `wiki.yaml` — project identity (system name, tagline). Filled in during
  bootstrap; the dashboard reads it live.
- `scripts/` — standalone maintenance scripts, e.g. `concept-cluster-audit.py`
  (deterministic support for `workflows/relations.md`).
- `apps/` — auxiliary applications shipped with the wiki, e.g. `dashboard/`, the
  read-only Flask app started by `dashboard.sh`.
