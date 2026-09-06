# tsu-demo — Naked Requirements-Wiki Starter

- **Status:** accepted
- **Date:** 2026-09-06
- **Source vault:** `/Users/gernotstarke/projects/arc42/aquarius/aquarius-reqirements`
- **Target repo:** `/Users/gernotstarke/projects/arc42/tsu-demo`

## Purpose

A ready-to-run, content-free requirements wiki for live use in an English-language
requirements workshop. The facilitator drives one instance on a projector; the group
watches an empty dashboard fill up as real requirements are captured through the
ingest and audit workflows.

The repo is a curated extraction from the Aquarius demo: all the machinery, none of
the Kinderschwimmliga content.

## Decisions taken

| Decision | Choice |
|---|---|
| Extraction strategy | Fresh repo, curated copy-in (file-by-file, reviewed on the way in) |
| Nakedness | Schema inherited (types, templates, anchors, ADRs); `wiki/` empty |
| Language | English throughout — machinery *and* captured content |
| Workshop mode | Facilitator drives one shared vault on a beamer |
| Repo layout | Repo root == vault root |

## Non-goals

- Per-participant setup, zip distribution, preflight scripts. Beamer mode only.
- Keeping the starter in sync with Aquarius. This is a one-time extraction; the
  README records the provenance and manual re-sync is accepted.
- A live data-model projection. The Aquarius hardcode is removed, not replaced.

## Architecture

Unchanged from Aquarius — that is the point. Three layers plus schema:

1. **`raw/`** — human-owned immutable sources. Top level is the inbox; ingested
   originals are archived to `raw/ingested/`; agent-authored provenance records live
   in `raw/sources/`.
2. **`wiki/`** — agent-maintained typed content units, one folder per type.
3. **schema** — `CLAUDE.md` + `_templates/` + `_system/anchors/`.

`_system/` holds the machinery: workflows, ADRs, anchors, scripts, the dashboard app,
plus `index.md` and `log.md` bookkeeping.

The dashboard is a read-only Flask app that parses the vault live on each request. It
runs in Docker via `./dashboard.sh`, mounting `wiki/` and `_system/adr/` read-only.

### One structural change: `_system/wiki.yaml`

Aquarius hardcodes its identity in seven places across `app.py` and the templates. The
starter reads them from a single config file:

```yaml
system_name: ""      # e.g. "Bookshelf" — set during bootstrap
tagline: ""          # one line under the hero
```

Consumers: page `<title>`, footer caption, hero heading, the goal-tree root label
(`"Vision {system_name}"`), and `build_context_diagram(center=…)`. Empty values must
render sensibly — the config is blank until session 1 fills it in.

## Component inventory

Copy tiers from the source vault. Every file lands in the same relative path.

### Tier 1 — verbatim

- `_system/anchors/` — all 9 files (`smart`, `pam`, `invest`, `moscow`,
  `user-story-format`, `acceptance-criteria`, `story-mapping`, `req42`, `README`)
- `_templates/` — 12 of 13 files (all but `goal.md`, see Tier 2)
- `_system/workflows/relations.md`, `_system/workflows/report.md`
- `_system/scripts/concept-cluster-audit.py`
- `.claude/skills/requirements-wiki/SKILL.md`
- `.obsidian/` — app.json, appearance.json, core-plugins.json, community-plugins.json,
  graph.json, themes, the terminal plugin. **Not** `workspace.json` / `workspaces.json`
  (machine-specific pane layout).
- `docs/req42/`, `docs/methods/`, `docs/show-different-graphs.md`
- `_system/apps/dashboard/` — `Dockerfile`, `compose.yaml`, `.dockerignore`,
  `requirements.txt`, `static/vendor/`, `static/glossary-graph.js`, `static/style.css`,
  `static/req42-logo-white.png`, `tests/`
- `dashboard.sh`, `.gitignore`

### Tier 2 — translate to English

- `_system/apps/dashboard/app.py` — ~33 German string literals: `FOLDER_LABELS`,
  `_ID_LABELS`, tile `label`/`unit` values, `REQ42_BLOCKS`
- `_system/apps/dashboard/templates/*.html` — ~30 strings: headings, empty states,
  link captions
- `_system/workflows/ingest.md` — the ADR-0005 language clause
- `_system/workflows/audit.md` — the German "Kontext-Kanten & Projektion" section
- `_templates/goal.md` — the only template with German prose
- `.claude/skills/grill-requirements/SKILL.md` — its language clause
- `CLAUDE.md` — the two German passages
- ADRs 0006, 0007, 0013, 0014, 0016, 0018, 0022, 0023, 0024 — fully German
- ADRs 0010, 0015, 0017, 0019, 0020, 0021 — English prose, Kinderschwimmliga examples

**Translation rules:**
- `REQ42_BLOCKS`: promote the existing `en:` field to `title:`. Anglicise the URL
  slugs to match (`qualitaet`→`quality`, `randbedingungen`→`constraints`,
  `modelle`→`models`) and update every `href`, template link and test that names them.
- Domain examples in ADRs become neutral placeholders (`Entity A`, `SystemX`), not a
  substitute domain — a second fictional domain would compete with the workshop's own.
- Body-structure markers (`## Vision`, `**Definition.**`, `**Attributes.**`) are
  parsed by `app.py` and emitted by `_templates/`. Translate both sides together or
  the parsers silently return empty.

### Tier 3 — rewrite

- `ADR-0005` — retitle from `fachsprache-deutsch` to `0005-ubiquitous-language-english.md`,
  content replaced. Note in it that the choice is per-project and may be re-decided.
- `ADR-0024` (graphical brand) — strip Aquarius brand specifics; keep the principle.
- `_system/index.md` — headings only, every section empty
- `_system/log.md` — header only, no entries
- `_system/README.md` — mention `wiki.yaml`
- `docs/GETTING-STARTED.md` — already English; update the folder tree and drop the
  `requirements-wiki.zip` unzip step (this is a git repo, not a zip)
- `README.md` — new: what this is, provenance from Aquarius, how to start
- Hero image — neutral placeholder replacing `aquarius-header-title.webp/png`

### Tier 4 — excluded

All 103 `wiki/**` pages, 14 `raw/sources/`, `raw/drafts/`, `raw/ingested/`,
`raw/methods/`, `raw/assets/`, `sandbox/`, `GernotsProjekte/`, Aquarius imagery,
`docs/superpowers/` history from Aquarius, `.claude/settings.local.json`.

Empty content folders are created with `.gitkeep`: `wiki/{glossary,goals,stakeholders,`
`context,external-interfaces,data-models,activity-models,use-cases,`
`functional-requirements,quality-requirements,constraints,issues}`, `raw/sources/`,
`raw/ingested/`, `raw/assets/`.

## The empty-state pass

The critical path. Aquarius has never rendered against an empty vault; several code
paths assume content exists.

**Known hazards** (verify each, do not assume):
- `build_vision_tile(load_goals(), …)` with no vision page
- `_mermaid_goal_tree()` — returns `None` when vision or objectives are missing;
  confirm callers handle `None`
- `backlog_tile` — `total_epics`/`total_features`/`total_stories` at zero
- the data-model tile's `claim` string, hardcoded to `Kernknoten: Kind`
- `DM_ENTITIES` / `DM_EDGES` — a constant list of 13 Kinderschwimmliga entities and 17
  edges feeding `build_data_model_full_diagram()` and `build_data_model_kind_diagram()`
- `build_context_diagram(center="AQUARIUS")` with no `EIF`/`STK` edges
- `/graph/glossary` with no terms
- `/search` with an empty index

**Required behaviour:** every one of the 16 routes returns HTTP 200 against an empty
vault and renders a deliberate empty state. Each content tile shows a count of 0 and a
one-line call to action naming the concrete next step, e.g.

> No glossary terms yet — drop a source in `raw/` and ask the agent to ingest it.

`DM_ENTITIES`/`DM_EDGES` are deleted. The data-model tile and `/data-model` render
their diagram only when `wiki/data-models/` is non-empty; otherwise the empty state.
A live projection from page frontmatter is explicitly out of scope.

## Testing

- The 4 inherited test files must pass. They reference Aquarius fixtures; port or
  re-fixture them with neutral data.
- **New: `tests/test_empty_vault.py`** — boots the app with `WIKI_DIR` pointing at an
  empty tree and asserts 200 plus the absence of a traceback on all 16 routes:
  `/`, `/glossary`, `/graph/glossary`, `/issues`, `/stakeholders`, `/adrs`, `/search`,
  `/goals`, `/data-model`, `/req42`, `/req42/backlog`, `/req42/<slug>` for each of the
  5 slugs, `/page/<folder>/<stem>` and `/functional-requirements/<stem>` (expect 404,
  not 500), `/ping`, `/leaving`.
- **Manual acceptance — "the naked run":** fresh clone → `./dashboard.sh` → click every
  tile → run a real ingest of one source through `ingest.md` → confirm counters move
  0→1, the glossary graph shows its first node, and `index.md` / `log.md` gain their
  first entries.

## New workshop machinery

- **`_system/workflows/bootstrap.md`** — the first-30-minutes procedure: name the
  system and write `_system/wiki.yaml`, confirm the ubiquitous language, capture
  `GOAL-001` (vision), the first glossary terms, the first stakeholder. Ends by
  pointing at `ingest.md` for the first real source.
- **`reset.sh`** — restore the naked state: delete `wiki/**/*.md`, `raw/sources/*`,
  `raw/ingested/*`, `raw/` inbox files, truncate `index.md` / `log.md` to their
  scaffolds, blank `wiki.yaml`. Prompts for confirmation; `--force` to skip.
- **`raw/examples/`** — one neutral demo source (a short fictional interview
  transcript, ~1 page) as a safety net when participant material isn't ready. Outside
  the inbox so it is never ingested by accident.
- **`docs/WORKSHOP.md`** — the facilitator script: agenda, which workflow to run at
  which point, what to narrate while the agent works, recovery moves when a live
  ingest goes wrong.
- **Non-Docker fallback** in `dashboard.sh` — a `--local` mode running Flask directly
  (`uv run` or venv) for machines where Docker won't start.

## Risks

- **Silent parser breakage.** Translating a heading in `_templates/` without the
  matching regex in `app.py` produces empty sections rather than errors. Mitigation:
  translate both sides in one change; the empty-vault test will not catch this, so
  the naked run must include one real ingest.
- **Projector legibility.** `style.css` is tuned for desktop reading. Not addressed
  in this spec; check on the actual beamer before the workshop.
- **ADR translation volume.** Nine dense German architecture documents are the single
  largest chunk of work and the least visible during a workshop. Cuttable for run one.

## Sequencing

1. Skeleton, `.gitignore`, empty folders, Tier-1 verbatim copies
2. `wiki.yaml` + the empty-state pass + `test_empty_vault.py` ← critical path
3. Tier-2 UI translation (`app.py`, templates, `REQ42_BLOCKS` + slugs)
4. Tier-2/3 prose: `CLAUDE.md`, workflows, `goal.md`, skills, `index.md`, `log.md`,
   `README.md`, `GETTING-STARTED.md`
5. `bootstrap.md`, `reset.sh`, `raw/examples/`, `WORKSHOP.md`, `--local` fallback
6. ADR translation ← cuttable
7. The naked run
