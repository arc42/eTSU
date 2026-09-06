# Workflow: Relationship audit  (the graph / link linter)

Keep the **edge graph** complete and reciprocal, so the wiki navigates both ways and
every projection (context diagram, coverage matrices, story map — ADR-0018) rests on
real edges. This is the structural counterpart to `audit.md`, which checks page
*content*; this one checks whether the right *edges between* pages exist. Run it
periodically, after a batch ingest, or on request.

## What it looks for — by tier (confidence drives the action)

Findings are ranked by how mechanical/certain they are. Confidence decides whether a
finding is **auto-fixed** or **queued for the human** — never silently rewrite a
judgment call (same stance as `audit.md`).

1. **Concept identity across types (≈100 % — auto-fix).** Pages of different types that
   share the same kebab slug-suffix (or an identical `title:`) denote the *same domain
   concept* — e.g. `GLO-010-schwimmbad` ⇄ `DM-003-schwimmbad`. They must be reciprocally
   linked in `related:`. Add the missing back-link on whichever side omits it.
2. **Asymmetric `related:` (high — auto-fix).** A lists B in `related:` but B omits A.
   Repair reciprocity — but **only** for the symmetric relation `related:`. Never touch
   the *directional* fields (`parent:`, `sources:`, `goal:`): their reverse side is a
   projection (Children, the source's `ingested-pages:`, Goal-coverage — ADR-0018), not a
   back-link.
3. **Entity ⇄ import-format / boundary-owner (medium — candidate).** A data entity marked
   *Konfiguration* (loaded from a file — body says „per CSV/Datei eingelesen", or a
   `raw/drafts/*-format-vorschlag.md` shares its slug) should link the boundary node that
   owns its format: `FR-006` for config bootstrap, the relevant `EIF-` for an external
   feed (ADR-0021) — and that node should list the entities it governs. Suggest; let the
   human confirm. Also flag a **raw-path string** (e.g. `` `raw/drafts/…-format-vorschlag.md` ``)
   used where a wikilink to a boundary owner belongs.
4. **Unlinked mentions (low–medium — candidate).** Prose names a *defined* glossary term
   (its `title:` or an `aliases:` entry) without wrapping it in a wikilink. Inverse of
   `audit.md`'s "missing pages" check. Higher false-positive rate ⇒ suggest only, with a
   high threshold (skip incidental/self mentions).

## How to run it — deterministic first, LLM only for the fuzzy tier

1. **Build the edge index.** For every page collect: `id`, `type`, `title`, slug-suffix,
   the `related:` / `parent:` / `sources:` / `goal:` frontmatter lists, and the set of
   `[[…]]` wikilinks in the body. Mostly grep-able; no LLM needed.
2. **Tiers 1–3 are computed, not judged.** Cluster by slug-suffix/title for Tier 1; diff
   the `related:` edges in both directions for Tier 2; scan config/import markers plus
   `*-format-vorschlag.md` drafts for Tier 3. Tier 1 + the Tier-2 `related:` reciprocity
   gaps are implemented deterministically in **`_system/scripts/concept-cluster-audit.py`**
   (`python3 _system/scripts/concept-cluster-audit.py` from the repo root) — act on its
   `GAPS` list. The same script prints each cluster's definition-leads side by side, which
   feeds the *content*-drift review owned by `audit.md` (conflicting canonical meanings →
   `ISS-NNN`, never auto-merge).
3. **Tier 4 is the only LLM pass.** Scan prose for glossary titles/aliases that appear
   without a wikilink and decide whether each mention is referential or incidental.
4. **Classify & act.** Auto-apply Tier-1 (and clearly-symmetric Tier-2) `related:`
   back-links; route everything judgmental to a candidate list / `ISS-NNN`.

## Output
1. A **relationship report** in chat, grouped by tier and confidence, each candidate
   stating the exact edge proposed (e.g. „add `[[DM-003-schwimmbad]]` to `GLO-010`
   `related:`").
2. **Auto-fix** only Tier-1 reciprocal `related:` back-links (and exact-match symmetric
   Tier-2). Bump `updated:` on every page you touch.
3. New/updated `ISS-NNN` for every candidate worth tracking (Tier 3/4, directional
   oddities).
4. Append to `_system/log.md`: `## [YYYY-MM-DD] relations | <scope>` + counts
   (fixed / candidates / issues).

## Prevention (so this stays cleanup, not a treadmill)
Tier 1 is cheap to prevent at write time: `ingest.md` (step 4) adds the reciprocal
concept-identity link the moment a same-slug pair is created. The relationship audit then
only mops up history and the fuzzier tiers.
