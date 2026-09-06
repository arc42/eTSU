# Requirements-Wiki Dashboard

A read-only, Docker-based dashboard over the `wiki/` layer (plus the ADRs in
`_system/adr/`). It parses the markdown pages live on each request (nothing is
written back) and renders them as tiles ("Kacheln").

## Run

From the repository root:

```sh
./dashboard.sh          # build + start, opens http://localhost:8080
./dashboard.sh down     # stop
./dashboard.sh logs     # follow logs
./dashboard.sh rebuild  # clean rebuild
```

No local Python/Flask install is required — everything runs in the container.
The `wiki/` folder is bind-mounted read-only at `/wiki`, so the dashboard always
reflects the current state of the wiki; just refresh the browser after editing.
Every page footer shows the data-refresh timestamp (page load time, in the `TZ`
timezone — default `Europe/Berlin`).

## Tiles

| Tile | Status | Content |
|------|--------|---------|
| **Glossar** | live | term count + a scrollable per-term relation list; links to a rendered glossary table at `/glossary` |
| **Ziele & Vision** | dummy | placeholder until the content type exists |
| **Stakeholder** | live | persona count + scrollable list; links to `/stakeholders` (profile, influence, interest) |
| **Issues** | live | issue count + open count; links to a filterable list (Alle/Offen/Geschlossen) at `/issues`, where clicking a row shows that issue's full content below |
| **ADRs** | live | decision count + scrollable list; links to `/adrs` — a list filterable by status, where clicking a row shows the full ADR text below. Violet accent to set it apart. |

The in-tile lists show ~4–5 rows and scroll for the rest. "Relationen" counts the
distinct other wiki pages a page links to (frontmatter `related:` plus body
`[[wikilinks]]`), excluding self-references and `raw/` provenance links. An issue
counts as **closed** when its status is `resolved` or `wontfix`. ADRs use the
Nygard format (`# ADR-NNNN:` heading, `**Status:**`, `**Date:**` — no
frontmatter); the `0000-template.md` is skipped, and the status filter buttons are
derived from the statuses actually present.

## Diagramme (mermaid)

The **system-context diagram** is not stored — it is *projected live* from the wiki
edges (ADR-0013, ISS-010): `build_context_diagram()` reads each external interface's
`flows:` and each stakeholder's `provides:`/`receives:` and emits a mermaid flowchart
(center = system, blue box; systems & organizations = light-grey boxes; human roles =
actor symbol 👤). Stakeholders are merged into shared nodes, hidden, or shaped (person
vs. organization) via their `context_role` / `nature` frontmatter (ADR-0014). It is
embedded on the context detail page (`/page/context/…`) and the req42 Scope page
(`/req42/scope`).

mermaid.js is **vendored for offline use** at `static/vendor/mermaid.min.js` (no CDN at
runtime; see that folder's README for version/license) and loaded via
`templates/_mermaid.html`. The same loader also renders any fenced ` ```mermaid ` block in
a page body — so additional diagrams just go straight into the markdown.

## Layout

```
_system/apps/dashboard/
  app.py             Flask app + wiki/ADR parser + context-diagram projection
  templates/         base / index / glossary / issues / stakeholders / adrs /
                     detail / req42 / req42_block / search / _mermaid (loader)
  static/style.css   dashboard styling
  static/vendor/     vendored mermaid.min.js (offline diagrams)
  Dockerfile         python:3.12-slim + gunicorn
  compose.yaml       service def, mounts ${WIKI_DIR}:/wiki:ro and ${ADR_DIR}:/adr:ro
```

## Obsidian

Hidden automatically: `_system/` is in `.obsidian/app.json` → `userIgnoreFilters`,
and `"showUnsupportedFiles": false` keeps the non-markdown code files out of the
file explorer. No extra configuration needed.
