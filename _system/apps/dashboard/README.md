# Requirements-Wiki Dashboard

A read-only dashboard over the `wiki/` layer (plus the ADRs in `_system/adr/`).
It parses the markdown pages live on each request — nothing is ever written
back — and renders them as tiles.

## Run

From the repository root:

```sh
./dashboard.sh          # build + start in Docker, opens http://localhost:8080
./dashboard.sh down     # stop
./dashboard.sh logs     # follow logs
./dashboard.sh rebuild  # clean rebuild
./dashboard.sh local    # no Docker: run Flask directly on http://localhost:8000
```

The Docker path needs no local Python install — everything runs in the
container. `local` is the escape hatch for machines where Docker will not
start: it builds a `.venv/` here on first run (~20 s) and serves the same app.

The `wiki/` folder is bind-mounted read-only at `/wiki`, so the dashboard always
reflects the current state of the vault; just refresh the browser after editing.
Every page footer shows the data-refresh timestamp (page load time, `%Y-%m-%d`,
in the `TZ` timezone — default `UTC`).

The dashboard shuts itself down a few seconds after its browser tab is closed
(ADR-0022), so it never lingers as an orphan process or container.

## Tiles

The home page (`/`) is nine tiles, in render order:

| Tile | Content |
|------|---------|
| **Vision** | the claim line from the vision goal page plus every objective with its epic count; links to `/goals`. Before a vision exists it shows an empty state pointing at the bootstrap workflow. |
| **req42** | entries per req42 building block (9 of 12 in scope), each row linking into `/req42` |
| **Search** | in-tile incremental search over every page title/ID; full results at `/search` |
| **Glossary** | term count + a scrollable per-term relation list; rendered glossary table at `/glossary`, term network at `/graph/glossary` |
| **Product Backlog** | epic/feature/story counts + per-epic breakdown; story map at `/req42/backlog` |
| **Stakeholders** | persona count + scrollable list; profile, influence and interest at `/stakeholders` |
| **ADRs** | decision count + scrollable list; `/adrs` is filterable by status and expands the full text of a row |
| **Issues** | issue count + open count; filterable list (All / Open / Closed) at `/issues` |
| **Data model** | entity count and the per-kind sketch; full catalog at `/data-model` |

Every tile that has no content yet renders a shared empty state naming the next
step, rather than a placeholder — a fresh vault is the normal day-one state.

The in-tile lists show ~4–5 rows and scroll for the rest. The relation count is
the number of distinct other wiki pages a page links to (frontmatter `related:`
plus body `[[wikilinks]]`), excluding self-references and `raw/` provenance
links. An issue counts as **closed** when its status is `resolved` or `wontfix`.
ADRs use the Nygard format (`# ADR-NNNN:` heading, `- **Status:**`,
`- **Date:**` — no frontmatter); `0000-template.md` is skipped, and the status
filter buttons are derived from the statuses actually present.

## Diagrams (mermaid)

The **system-context diagram** is not stored — it is *projected live* from the
wiki edges (ADR-0013): `build_context_diagram()` reads each external interface's
`flows:` and each stakeholder's `provides:`/`receives:` and emits a mermaid
flowchart (centre = the system, blue box; systems and organizations = light-grey
boxes; human roles = actor symbol 👤). Stakeholders are merged into shared
nodes, hidden, or shaped (person vs. organization) via their `context_role` /
`nature` frontmatter (ADR-0014). It is embedded on the context detail page
(`/page/context/…`) and on the req42 Scope page (`/req42/scope`).

The **goal tree** (vision → objectives) and the **goal/epic map** on
`/req42/backlog` are projections in the same style, built from the goal pages'
`stereotype:`/`parent:` fields and each FR's `goal:` field (ADR-0016, ADR-0018).

mermaid.js is **vendored for offline use** at `static/vendor/mermaid.min.js` (no
CDN at runtime; see that folder's README for versions and licenses) and loaded
via `templates/_mermaid.html`. The same loader renders any fenced ` ```mermaid `
block in a page body, so extra diagrams can go straight into the markdown. The
glossary term network at `/graph/glossary` uses the vendored cytoscape bundle
plus `static/glossary-graph.js`.

## Layout

```
_system/apps/dashboard/
  app.py             Flask app + wiki/ADR parser + all diagram projections
  templates/         base, index, _empty (shared empty state), _mermaid (loader),
                     glossary, graph, stakeholders, issues, adrs, search, detail,
                     goals, backlog, fr, data_model, req42, req42_block
  static/style.css   dashboard styling
  static/glossary-graph.js   the cytoscape term network
  static/*.png       eTSU logo / mark / favicon, req42 logo
  static/vendor/     vendored mermaid + cytoscape (offline diagrams)
  tests/             plain-assert test scripts (no pytest) + a fixture vault
  Dockerfile         python:3.12-slim + gunicorn
  compose.yaml       service def, mounts ${WIKI_DIR}:/wiki:ro and ${ADR_DIR}:/adr:ro
```

## Tests

Plain Python scripts with bare `assert`s — no pytest, no runner. From this
directory, inside the venv `./dashboard.sh local` builds:

```sh
for t in tests/test_*.py; do .venv/bin/python "$t"; done
```

They cover the empty vault (every route must render on day one), a populated
fixture vault, the backlog and goal projections, the glossary graphs,
`wiki_config()`, the ADR metadata in `_system/adr/`, and the contract between
`_templates/` and `app.py`'s parser.

## Obsidian

Hidden automatically: `_system/` is in `.obsidian/app.json` →
`userIgnoreFilters`, and `"showUnsupportedFiles": false` keeps the non-markdown
code files out of the file explorer. No extra configuration needed.
