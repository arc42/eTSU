# tsu-demo Starter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `tsu-demo`, a content-free English requirements wiki extracted from the Aquarius demo, that runs a dashboard cleanly at zero entries and fills up live during a workshop.

**Architecture:** A curated file-by-file copy from the Aquarius vault into a fresh repo whose root *is* the vault root. All machinery (13 content types, templates, method anchors, 4 workflows, 24 ADRs, Flask dashboard) is inherited; all 103 content pages are dropped. Aquarius's hardcoded identity moves into a single `_system/wiki.yaml`, and every dashboard route is made to render a deliberate empty state.

**Tech Stack:** Python 3 / Flask 3.0.3 / PyYAML 6.0.2 / Markdown 3.7 / gunicorn, Jinja2 templates, Docker Compose, Cytoscape + Mermaid (vendored JS), Obsidian-flavoured Markdown vault.

**Spec:** `docs/superpowers/specs/2026-09-06-tsu-demo-starter-design.md`

## Global Constraints

- **Source vault (read-only, never modify):** `/Users/gernotstarke/projects/arc42/aquarius/aquarius-reqirements` — referred to below as `$SRC`.
- **Target repo:** `/Users/gernotstarke/projects/arc42/tsu-demo` — referred to below as `$DST`. Repo root == vault root.
- **Language:** English everywhere — UI strings, code comments, workflows, templates, ADRs, docs. No German survives except inside `docs/req42/req42-framework-DE.md`, which is a cited external reference document and stays as-is.
- **No Aquarius domain content.** After every task, `grep -riE 'aquarius|kinderschwimm|schwimm|wettkampf|verein|figur|kader|drsl' $DST --include='*.md' --include='*.py' --include='*.html'` must return hits only in `docs/superpowers/` (spec/plan) and `README.md` (provenance note).
- **Tests are plain-assert scripts, not pytest.** They live in `_system/apps/dashboard/tests/`, are run as `python tests/<name>.py` from the dashboard directory, and `sys.path.insert` their parent to import `app`. Match this style exactly; do not introduce pytest.
- **The dashboard self-terminates** (ADR-0022). Any test that imports `app` MUST set `DASH_STARTUP_GRACE=3600` and `DASH_HEARTBEAT_GRACE=3600` in `os.environ` **before** `import app`, or the watchdog thread will SIGTERM the test process after 90 seconds.
- **`WIKI_DIR` and `ADR_DIR` are read at import time** as module-level constants in `app.py`. Tests must set them in `os.environ` before `import app`.
- **Commit after every task** with the trailer:
  ```
  Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_013K4BFcVdpe7pfftrR31UxH
  ```

## Parallelisation

Tasks 1 → 2 → 3 → 4 are a strict chain (each edits `app.py`/templates structurally).
After Task 4: **Tasks 6 and 7 are sequential with each other only if the same file is touched** — 6 edits `app.py`, 7 edits `templates/*.html`, so they can run in parallel.
**Tasks 5, 8, 9, 10, 11 are mutually independent** and can all run in parallel once Task 4 lands (Task 5 needs the empty-state code; 8/9/10/11 touch only prose files).
Task 12 is last.

---

### Task 1: Repo skeleton and verbatim copies

**Files:**
- Create: `$DST/.gitignore`
- Create: `$DST/wiki/{glossary,goals,stakeholders,context,external-interfaces,data-models,activity-models,use-cases,functional-requirements,quality-requirements,constraints,issues}/.gitkeep`
- Create: `$DST/raw/{sources,ingested,assets,examples}/.gitkeep`
- Copy: `_templates/` (12 files), `_system/anchors/` (9 files), `_system/workflows/{relations,report,ingest,audit}.md`, `_system/adr/` (24 files), `_system/scripts/`, `_system/apps/dashboard/`, `.claude/skills/`, `.obsidian/`, `docs/req42/`, `docs/methods/`, `docs/show-different-graphs.md`, `docs/GETTING-STARTED.md`, `CLAUDE.md`, `dashboard.sh`
- Modify: `$DST/_system/apps/dashboard/compose.yaml` (container name)

**Interfaces:**
- Consumes: nothing (first task).
- Produces: the full directory tree every later task edits in place. Later tasks assume `$DST` paths mirror `$SRC` paths exactly.

- [ ] **Step 1: Create the folder scaffold**

```bash
SRC=/Users/gernotstarke/projects/arc42/aquarius/aquarius-reqirements
DST=/Users/gernotstarke/projects/arc42/tsu-demo
cd "$DST"
for d in glossary goals stakeholders context external-interfaces data-models \
         activity-models use-cases functional-requirements quality-requirements \
         constraints issues; do
  mkdir -p "wiki/$d" && touch "wiki/$d/.gitkeep"
done
for d in sources ingested assets examples; do
  mkdir -p "raw/$d" && touch "raw/$d/.gitkeep"
done
mkdir -p _system/workflows _system/adr _system/scripts _templates .claude docs
```

- [ ] **Step 2: Copy the machinery verbatim**

```bash
cp -R "$SRC/_templates/." _templates/
cp -R "$SRC/_system/anchors" _system/
cp "$SRC/_system/workflows/"{relations,report,ingest,audit}.md _system/workflows/
cp -R "$SRC/_system/adr/." _system/adr/
cp -R "$SRC/_system/scripts/." _system/scripts/
mkdir -p _system/apps && cp -R "$SRC/_system/apps/dashboard" _system/apps/
cp -R "$SRC/.claude/skills" .claude/
cp -R "$SRC/.obsidian" .
cp -R "$SRC/docs/req42" "$SRC/docs/methods" docs/
cp "$SRC/docs/show-different-graphs.md" "$SRC/docs/GETTING-STARTED.md" docs/
cp "$SRC/CLAUDE.md" "$SRC/dashboard.sh" .
chmod +x dashboard.sh
```

- [ ] **Step 3: Remove what must not travel**

`.obsidian/workspace.json` and `workspaces.json` are machine-specific pane layouts. The Aquarius hero images and the dashboard's `.venv` must not travel either.

```bash
rm -f .obsidian/workspace.json .obsidian/workspaces.json
rm -f _system/apps/dashboard/static/aquarius-header-title.png \
      _system/apps/dashboard/static/aquarius-header-title.webp
rm -rf _system/apps/dashboard/.venv
```

- [ ] **Step 4: Write `.gitignore`**

```
.DS_Store
_system/apps/dashboard/.venv
.obsidian/workspace.json
.obsidian/workspaces.json
```

- [ ] **Step 5: Rename the container**

In `_system/apps/dashboard/compose.yaml` replace:

```yaml
    container_name: aquarius-requirements-dashboard
```

with:

```yaml
    container_name: tsu-demo-dashboard
```

- [ ] **Step 6: Verify the tree**

Run:
```bash
cd "$DST"
test $(ls _templates/*.md | wc -l) -eq 13 && echo "templates OK"
test $(ls _system/anchors/*.md | wc -l) -eq 9 && echo "anchors OK"
test $(ls _system/adr/*.md | wc -l) -eq 25 && echo "adrs OK"
test $(find wiki -name '*.md' | wc -l) -eq 0 && echo "wiki empty OK"
ls _system/apps/dashboard/templates/*.html | wc -l   # expect 16
```
Expected: `templates OK`, `anchors OK`, `adrs OK`, `wiki empty OK`, `16`.

(`_templates` is 13 files including `goal.md`; `_system/adr` is 25 files including `0000-template.md`.)

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "chore: scaffold tsu-demo from the Aquarius vault machinery"
```

---

### Task 2: `_system/wiki.yaml` and de-branding the dashboard identity

Aquarius hardcodes its name in six places. Move them all behind one config file the workshop group fills in during bootstrap.

**Files:**
- Create: `$DST/_system/wiki.yaml`
- Create: `$DST/_system/apps/dashboard/tests/test_wiki_config.py`
- Modify: `$DST/_system/apps/dashboard/app.py` (config loader, context processor, `_mermaid_goal_tree`, `build_context_diagram`)
- Modify: `$DST/_system/apps/dashboard/templates/base.html`, `templates/index.html`
- Modify: `$DST/_system/apps/dashboard/compose.yaml`, `$DST/dashboard.sh`

**Interfaces:**
- Consumes: the tree from Task 1.
- Produces:
  - `app.wiki_config() -> dict` with keys `system_name: str` (never empty — falls back to `"Requirements Wiki"`), `system_name_set: bool`, `tagline: str`.
  - A Jinja context processor injecting `system_name`, `system_name_set`, `tagline` into every template.
  - Env var `WIKI_CONFIG` overriding the config path (used by Docker and tests).

- [ ] **Step 1: Write the failing test**

Create `_system/apps/dashboard/tests/test_wiki_config.py`:

```python
"""Plain-assert test for wiki_config() — no pytest dependency.

Run from the dashboard dir inside a venv that has the app's requirements:
    .venv/bin/python tests/test_wiki_config.py
"""
import os
import sys
import tempfile
from pathlib import Path

_tmp = Path(tempfile.mkdtemp())
(_tmp / "wiki").mkdir()
(_tmp / "adr").mkdir()
os.environ["WIKI_DIR"] = str(_tmp / "wiki")
os.environ["ADR_DIR"] = str(_tmp / "adr")
os.environ["WIKI_CONFIG"] = str(_tmp / "wiki.yaml")
# the dashboard SIGTERMs itself without a browser heartbeat (ADR-0022)
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402

CONFIG = Path(os.environ["WIKI_CONFIG"])


def test_missing_config_falls_back():
    if CONFIG.exists():
        CONFIG.unlink()
    cfg = app.wiki_config()
    assert cfg["system_name"] == "Requirements Wiki", cfg
    assert cfg["system_name_set"] is False, cfg
    assert cfg["tagline"] == "", cfg


def test_blank_config_falls_back():
    CONFIG.write_text('system_name: ""\ntagline: ""\n', encoding="utf-8")
    cfg = app.wiki_config()
    assert cfg["system_name"] == "Requirements Wiki", cfg
    assert cfg["system_name_set"] is False, cfg


def test_filled_config_is_used():
    CONFIG.write_text('system_name: "Bookshelf"\ntagline: "Lending, tracked"\n',
                      encoding="utf-8")
    cfg = app.wiki_config()
    assert cfg["system_name"] == "Bookshelf", cfg
    assert cfg["system_name_set"] is True, cfg
    assert cfg["tagline"] == "Lending, tracked", cfg


def test_config_is_read_live_not_cached():
    CONFIG.write_text('system_name: "First"\n', encoding="utf-8")
    assert app.wiki_config()["system_name"] == "First"
    CONFIG.write_text('system_name: "Second"\n', encoding="utf-8")
    assert app.wiki_config()["system_name"] == "Second", \
        "config must be re-read per call so the workshop can rename live"


def test_malformed_config_does_not_crash():
    CONFIG.write_text("system_name: [unclosed\n", encoding="utf-8")
    cfg = app.wiki_config()
    assert cfg["system_name"] == "Requirements Wiki", cfg


if __name__ == "__main__":
    test_missing_config_falls_back()
    test_blank_config_falls_back()
    test_filled_config_is_used()
    test_config_is_read_live_not_cached()
    test_malformed_config_does_not_crash()
    print("OK: wiki_config()")
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
cd "$DST/_system/apps/dashboard"
python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt
.venv/bin/python tests/test_wiki_config.py
```
Expected: FAIL with `AttributeError: module 'app' has no attribute 'wiki_config'`.

- [ ] **Step 3: Add the config loader to `app.py`**

Insert immediately after the `ADR_DIR` definition (currently around line 53, just before the `WIKILINK_RE` comment):

```python
# Project identity. Everything Aquarius hardcoded (page title, footer, hero,
# goal-tree root, context-diagram centre) reads from here so a fresh vault can
# be renamed in one place. Read per call, never cached: during a workshop the
# group fills this in live and just refreshes the page.
_env_cfg = os.environ.get("WIKI_CONFIG")
CONFIG_PATH = Path(_env_cfg) if _env_cfg else Path(__file__).resolve().parents[2] / "wiki.yaml"

DEFAULT_SYSTEM_NAME = "Requirements Wiki"


def wiki_config() -> dict:
    """Project identity from `_system/wiki.yaml`.

    Returns `system_name` (never empty — falls back to DEFAULT_SYSTEM_NAME),
    `system_name_set` (False while the vault is still unnamed, so views can
    show a "name your system" hint) and `tagline`. A missing, empty or
    malformed file yields the defaults rather than an error: an unnamed vault
    is the normal state on day one.
    """
    try:
        data = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        data = {}
    if not isinstance(data, dict):
        data = {}
    name = str(data.get("system_name") or "").strip()
    return {
        "system_name": name or DEFAULT_SYSTEM_NAME,
        "system_name_set": bool(name),
        "tagline": str(data.get("tagline") or "").strip(),
    }


@app.context_processor
def inject_identity():
    """Make the project identity available to every template."""
    return wiki_config()
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
cd "$DST/_system/apps/dashboard" && .venv/bin/python tests/test_wiki_config.py
```
Expected: `OK: wiki_config()`

- [ ] **Step 5: Create `_system/wiki.yaml`**

```yaml
# Project identity for this requirements wiki.
# Filled in during bootstrap (_system/workflows/bootstrap.md). While blank the
# dashboard shows neutral defaults.
system_name: ""      # e.g. "Bookshelf" — the system whose requirements this vault holds
tagline: ""          # one line shown under the hero, e.g. "Lending, tracked"
```

- [ ] **Step 6: Replace the hardcoded identity in `app.py`**

In `_mermaid_goal_tree()`, replace:

```python
    lines = ["graph TD", '  V["Vision Aquarius"]:::vision']
```

with:

```python
    root = _clean_label(wiki_config()["system_name"])
    lines = ["graph TD", f'  V["Vision {root}"]:::vision']
```

In `build_context_diagram()`, replace the signature:

```python
def build_context_diagram(center: str = "AQUARIUS") -> str | None:
```

with:

```python
def build_context_diagram(center: str | None = None) -> str | None:
```

and add as the first line of its body (before any existing statement):

```python
    center = center or _clean_label(wiki_config()["system_name"])
```

- [ ] **Step 7: Replace the hardcoded identity in the templates**

In `templates/base.html`, replace:

```html
  <title>{% block title %}Requirements-Dashboard{% endblock %} · Aquarius</title>
```
with
```html
  <title>{% block title %}Requirements Dashboard{% endblock %} · {{ system_name }}</title>
```

and replace:
```html
    <div class="foot-title">Live-Ansicht · Aquarius-Requirements-Wiki</div>
```
with
```html
    <div class="foot-title">Live view · {{ system_name }} requirements wiki</div>
```

In `templates/index.html`, replace the hero block (the `<img class="hero-banner" …>` element and the `<p class="lead">` line following it) with a text hero, since the Aquarius artwork was removed in Task 1:

```html
<header class="hero">
  <h1 class="hero-title">{{ system_name }}</h1>
  {% if tagline %}<p class="lead">{{ tagline }}</p>{% endif %}
  {% if not system_name_set %}
  <p class="lead empty-hint">This vault has no name yet — run the bootstrap
    workflow, or set <code>system_name</code> in <code>_system/wiki.yaml</code>.</p>
  {% endif %}
</header>
```

Add to the end of `static/style.css`:

```css
/* text hero — replaces the artwork banner in the neutral starter */
.hero { margin: .2rem 0 1.4rem; }
.hero-title { font-size: 2.2rem; margin: 0 0 .3rem; letter-spacing: -0.01em; }
```

- [ ] **Step 8: Wire the config through Docker**

In `compose.yaml`, add to `environment:`:

```yaml
      WIKI_CONFIG: "/config/wiki.yaml"
```

and add to `volumes:`:

```yaml
      # Project identity (_system/wiki.yaml), read-only like the rest.
      - "${CONFIG_FILE:-../../wiki.yaml}:/config/wiki.yaml:ro"
```

In `dashboard.sh`, next to the existing `WIKI_DIR` / `ADR_DIR` exports, add:

```bash
export CONFIG_FILE="$ROOT/_system/wiki.yaml"
```

- [ ] **Step 9: Verify no Aquarius identity remains in the dashboard**

Run:
```bash
grep -rniE 'aquarius' "$DST/_system/apps/dashboard/" || echo "clean"
```
Expected: `clean`.

- [ ] **Step 10: Commit**

```bash
git add -A
git commit -m "feat(dashboard): read project identity from _system/wiki.yaml"
```

---

### Task 3: Survive an empty vault (`app.py`)

The dashboard has never rendered against a vault with zero pages. Make every route work, and delete the hardcoded Kinderschwimmliga data model.

**Files:**
- Create: `$DST/_system/apps/dashboard/tests/test_empty_vault.py`
- Modify: `$DST/_system/apps/dashboard/app.py` (`DM_ENTITIES`/`DM_EDGES` removal, `index()`, `data_model_view()`)

**Interfaces:**
- Consumes: `app.wiki_config()` from Task 2.
- Produces:
  - `app.build_data_model_full_diagram() -> str | None` — now returns `None` when `wiki/data-models/` is empty (was: always a string).
  - `app.build_data_model_kind_diagram() -> str | None` — same change.
  - The home data-model tile's `diagram` key may be `None`; templates must guard on it (Task 4).

- [ ] **Step 1: Write the failing test**

Create `_system/apps/dashboard/tests/test_empty_vault.py`:

```python
"""Every route must render against a vault with zero pages — no pytest.

This is the starter repo's core guarantee: on day one of a workshop the wiki
is empty and the dashboard is on a projector. A 500 here is the worst possible
first impression.

Run from the dashboard dir:
    .venv/bin/python tests/test_empty_vault.py
"""
import os
import sys
import tempfile
from pathlib import Path

WIKI_FOLDERS = [
    "glossary", "goals", "stakeholders", "context", "external-interfaces",
    "data-models", "activity-models", "use-cases", "functional-requirements",
    "quality-requirements", "constraints", "issues",
]

_tmp = Path(tempfile.mkdtemp())
_wiki = _tmp / "wiki"
for _f in WIKI_FOLDERS:
    (_wiki / _f).mkdir(parents=True)
(_tmp / "adr").mkdir()
os.environ["WIKI_DIR"] = str(_wiki)
os.environ["ADR_DIR"] = str(_tmp / "adr")
os.environ["WIKI_CONFIG"] = str(_tmp / "wiki.yaml")
# without a browser heartbeat the watchdog SIGTERMs this process (ADR-0022)
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402

# /leaving is deliberately NOT exercised: it arms the self-shutdown watchdog,
# which would SIGTERM this test process. Its behaviour is covered by ADR-0022.
GET_ROUTES = [
    "/", "/glossary", "/graph/glossary", "/issues", "/stakeholders", "/adrs",
    "/search", "/goals", "/data-model", "/req42", "/req42/backlog",
    "/req42/scope", "/req42/models", "/req42/quality", "/req42/constraints",
]
NOT_FOUND_ROUTES = [
    "/page/glossary/GLO-001-nothing",
    "/functional-requirements/FR-001-nothing",
]


def test_all_get_routes_render_empty():
    client = app.app.test_client()
    for route in GET_ROUTES:
        resp = client.get(route)
        assert resp.status_code == 200, (route, resp.status_code)
        body = resp.get_data(as_text=True)
        assert "Traceback" not in body, route
        assert "jinja2.exceptions" not in body, route


def test_missing_pages_are_404_not_500():
    client = app.app.test_client()
    for route in NOT_FOUND_ROUTES:
        resp = client.get(route)
        assert resp.status_code == 404, (route, resp.status_code)


def test_ping_is_204():
    client = app.app.test_client()
    assert client.post("/ping").status_code == 204


def test_data_model_diagrams_are_none_when_no_entities():
    assert app.build_data_model_full_diagram() is None
    assert app.build_data_model_kind_diagram() is None


if __name__ == "__main__":
    test_all_get_routes_render_empty()
    test_missing_pages_are_404_not_500()
    test_ping_is_204()
    test_data_model_diagrams_are_none_when_no_entities()
    print(f"OK: {len(GET_ROUTES)} routes render on an empty vault")
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
cd "$DST/_system/apps/dashboard" && .venv/bin/python tests/test_empty_vault.py
```
Expected: FAIL. The `/req42/models` etc. slugs do not exist yet (they are still `modelle`, `qualitaet`, `randbedingungen` until Task 6) **and** `build_data_model_full_diagram()` still returns a hardcoded string.

> **Note for the implementer:** rename the three `REQ42_BLOCKS` slugs now, as part of Step 3, rather than waiting for Task 6 — the test pins the English slugs. Task 6 then only translates the visible titles and notes.

- [ ] **Step 3: Delete the hardcoded data model and rename the slugs**

In `app.py`, delete the entire `DM_ENTITIES = [...]` and `DM_EDGES = [...]` constants together with the `# --- data model projection …` comment block that introduces them, then rewrite the two builders:

```python
def build_data_model_full_diagram() -> str | None:
    """Full class diagram of every modelled entity.

    Projection from `wiki/data-models/` is not implemented yet; until it is,
    the view renders its empty state rather than a stale hardcoded model.
    Returns None while there are no data-model pages.
    """
    if not load_folder("data-models"):
        return None
    return None


def build_data_model_kind_diagram() -> str | None:
    """Compact diagram for the home tile. See build_data_model_full_diagram()."""
    if not load_folder("data-models"):
        return None
    return None
```

> Both builders return `None` unconditionally today — the `load_folder` guard documents the intended trigger and keeps the empty/non-empty distinction in one place for whoever implements the real projection. This is the spec's explicit non-goal; do not build the projection here.

Delete `_mermaid_dm_edge()` as well — it has no remaining caller.

In `REQ42_BLOCKS`, change three slugs and their hrefs to English:

| Block | Old `slug` / `href` | New `slug` / `href` |
|---|---|---|
| 05 Supporting Models | `modelle` / `/req42/modelle` | `models` / `/req42/models` |
| 06 Quality Requirements | `qualitaet` / `/req42/qualitaet` | `quality` / `/req42/quality` |
| 07 Constraints | `randbedingungen` / `/req42/randbedingungen` | `constraints` / `/req42/constraints` |

Then run `grep -rn 'modelle\|qualitaet\|randbedingungen' .` inside the dashboard directory and fix every remaining reference (templates and any test).

- [ ] **Step 4: Fix the home tile for an empty vault**

In `index()`, replace the data-model tile dict with one that carries a nullable diagram and a real empty state:

```python
        {
            "key": "data-model", "label": "Data model", "href": "/data-model",
            "icon": "🧩", "active": True,
            "diagram": build_data_model_kind_diagram(),
            "claim": (f"{n_entities} entities" if n_entities else
                      "No entities yet — model them as DM- pages"),
        },
```

and compute `n_entities = len(load_folder("data-models"))` above the `tiles = [` list.

- [ ] **Step 5: Run the test to verify it passes**

```bash
cd "$DST/_system/apps/dashboard" && .venv/bin/python tests/test_empty_vault.py
```
Expected: `OK: 15 routes render on an empty vault`

If a route still 500s, read the traceback and guard the specific call — do **not** wrap routes in blanket `try/except`. Likely culprits named in the spec: `build_vision_tile`, `_mermaid_goal_tree`, `build_backlog`, `build_glossary_graph`, `build_search_records`.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat(dashboard): render every route against an empty vault"
```

---

### Task 4: Deliberate empty states in the templates

Rendering without crashing is not enough. On a projector, each zero-count tile must tell the room what to do next.

**Files:**
- Modify: `$DST/_system/apps/dashboard/templates/index.html`, `glossary.html`, `stakeholders.html`, `issues.html`, `goals.html`, `backlog.html`, `data_model.html`, `graph.html`, `adrs.html`, `req42.html`
- Modify: `$DST/_system/apps/dashboard/static/style.css`
- Modify: `$DST/_system/apps/dashboard/tests/test_empty_vault.py`

**Interfaces:**
- Consumes: `build_data_model_kind_diagram()` returning `None` (Task 3); `system_name` / `system_name_set` context (Task 2).
- Produces: no new code interfaces. Every empty view contains the literal string `raw/` in its call to action — this is what the test asserts on.

- [ ] **Step 1: Extend the test with empty-state assertions**

Add to `tests/test_empty_vault.py`, and add the call to the `__main__` block:

```python
# routes whose empty state must tell the reader what to do next
CTA_ROUTES = ["/", "/glossary", "/stakeholders", "/goals", "/req42/backlog",
              "/data-model", "/issues"]


def test_empty_views_offer_a_next_step():
    client = app.app.test_client()
    for route in CTA_ROUTES:
        body = client.get(route).get_data(as_text=True)
        assert "raw/" in body, \
            f"{route} empty state does not tell the reader to add a source"
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
cd "$DST/_system/apps/dashboard" && .venv/bin/python tests/test_empty_vault.py
```
Expected: FAIL with `/ empty state does not tell the reader to add a source`.

- [ ] **Step 3: Add the shared empty-state partial**

Create `templates/_empty.html`:

```html
{% macro empty_state(what) %}
<p class="empty-state">
  No {{ what }} yet — drop a source into <code>raw/</code> and ask the agent:
  <em>“ingest the new file in raw/”</em>.
</p>
{% endmacro %}
```

Add to `static/style.css`:

```css
/* empty states — the first thing a workshop audience sees */
.empty-state {
  margin: .8rem 0; padding: .9rem 1.1rem; border-radius: 8px;
  border: 1px dashed var(--rule, #9aa3b2); opacity: .85; line-height: 1.5;
}
.empty-state code { font-size: .95em; }
```

- [ ] **Step 4: Use the partial in every list view**

In each of `glossary.html`, `stakeholders.html`, `issues.html`, `goals.html`, `backlog.html`, `data_model.html`, `graph.html`, `adrs.html`, `req42.html`, add at the top of the content block:

```html
{% from "_empty.html" import empty_state %}
```

and wrap the main listing so the empty case renders the macro instead. Pattern, using `glossary.html` as the worked example — the same shape applies to each file with its own collection variable and noun:

```html
{% if rows %}
  {# ... the existing table / list markup, unchanged ... #}
{% else %}
  {{ empty_state("glossary terms") }}
{% endif %}
```

Nouns to use per file: `glossary.html` → `"glossary terms"`; `stakeholders.html` → `"stakeholders"`; `issues.html` → `"issues"`; `goals.html` → `"goals"`; `backlog.html` → `"backlog items"`; `data_model.html` → `"data-model entities"`; `graph.html` → `"glossary terms"`; `adrs.html` → `"architecture decisions"`; `req42.html` → `"requirements"`.

- [ ] **Step 5: Guard the home tiles**

In `index.html`, the data-model tile currently renders `t.diagram` unconditionally. Guard it:

```html
{% if t.diagram %}
  {# existing mermaid block #}
{% else %}
  {{ empty_state("data-model entities") }}
{% endif %}
```

and in the generic tile loop, render `{{ empty_state(t.label|lower) }}` when `t.count is defined and t.count == 0 and not t.rows`.

- [ ] **Step 6: Run the test to verify it passes**

```bash
cd "$DST/_system/apps/dashboard" && .venv/bin/python tests/test_empty_vault.py
```
Expected: `OK: 15 routes render on an empty vault`

- [ ] **Step 7: Look at it**

```bash
cd "$DST" && ./dashboard.sh
```
Open http://localhost:8080 and click through every tile. Each must show the dashed empty-state box, not a blank panel or a stray heading. Then `./dashboard.sh down`.

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "feat(dashboard): deliberate empty states with a next-step call to action"
```

---

### Task 5: Fixture vault and ported regression tests

The four inherited tests assert on Aquarius pages (`FR-008`, `GLO-027-familie`, `STK-009-offizieller`) that no longer exist. Give them a small neutral fixture vault instead — which also makes the starter's test suite independent of its content, exactly the property a template repo wants.

**Files:**
- Create: `$DST/_system/apps/dashboard/tests/fixtures/wiki/` — a minimal neutral vault
- Modify: `$DST/_system/apps/dashboard/tests/{test_backlog,test_glossary_graph,test_glossary_ego_graph,test_relations_panel}.py`

**Interfaces:**
- Consumes: nothing from other tasks; runs against its own fixture.
- Produces: `tests/fixtures/wiki/` as the shared oracle for all four tests. Any later change to page parsing must keep these fixtures valid.

- [ ] **Step 1: Build the fixture vault**

Create pages under `tests/fixtures/wiki/` using the real `_templates/` frontmatter. Use a deliberately boring, non-domain example (a library lending system) so nobody mistakes it for workshop content:

- `glossary/GLO-001-book.md`, `GLO-002-loan.md`, `GLO-003-member.md`, `GLO-004-shelf.md`
  - `GLO-001-book` `related:` `[[GLO-002-loan]]`, `[[GLO-004-shelf]]`
  - `GLO-002-loan` `related:` `[[GLO-001-book]]`, `[[GLO-003-member]]`
  - `GLO-003-member` `related:` `[[GLO-002-loan]]`, `[[STK-001-librarian]]`
  - `GLO-004-shelf` `related:` `[[GLO-001-book]]` — one term with a single edge
- `stakeholders/STK-001-librarian.md` — `related:` `[[GLO-003-member]]`, `[[GLO-002-loan]]`
- `stakeholders/STK-002-reader.md` — `related:` `[[GLO-001-book]]`
- `goals/GOAL-001-library.md` (`stereotype: vision`) and `GOAL-002-faster-lending.md` (`stereotype: objective`, `parent: [[GOAL-001-library]]`)
- `functional-requirements/`:
  - `FR-001-lending.md` — `stereotype: epic`, `goal: [[GOAL-002-faster-lending]]`
  - `FR-002-checkout.md` — `stereotype: feature`, `parent: [[FR-001-lending]]`
  - `FR-003-scan-a-book.md`, `FR-004-confirm-loan.md` — `stereotype: story`, `parent: [[FR-002-checkout]]`
  - `FR-005-return-a-book.md` — `stereotype: story`, `parent: [[FR-001-lending]]` (a story hung straight off the epic, mirroring the shape the old `FR-001` test covered)

Every page needs the universal frontmatter (`id, type, title, status, created, updated, sources, related, tags`) and a `## Definition` / body section appropriate to its template, so the body parsers have something to find.

- [ ] **Step 2: Point each test at the fixture**

At the top of all four test files, before `import app`, insert:

```python
import os
from pathlib import Path

_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "wiki"
os.environ["WIKI_DIR"] = str(_FIXTURE)
os.environ["ADR_DIR"] = str(_FIXTURE.parent / "adr")
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"
```

Create an empty `tests/fixtures/adr/` with a `.gitkeep`. Update each file's module docstring: the old one says "WIKI_DIR is left unset so app.py falls back to the repo's wiki/ folder, making today's real FR hierarchy the test oracle" — that is now false. Replace it with "WIKI_DIR points at tests/fixtures/wiki, a small neutral vault, so the suite is independent of whatever content this starter is filled with."

- [ ] **Step 3: Rewrite the oracles**

Replace every Aquarius identifier with its fixture counterpart:

- `test_backlog.py`: `FR-008` → `FR-001`; expected features `["FR-009","FR-010","FR-011"]` → `["FR-002"]`; `n_features` 3 → 1; `n_stories` 7 → 3; the per-feature story sets → `{"FR-003","FR-004"}` for `FR-002`; the `direct_stories` superset check → `{"FR-005"}`. Keep every internal-consistency assertion (`total_epics == len(epics)`, the two summed-count assertions, `orphans == []`) exactly as-is — those hold for any valid vault and are the most valuable part of the test.
- `test_glossary_graph.py`: `GLO-027-familie` (a term with degree 0) → `GLO-004-shelf`, and change the expected degree from `0` to `1`, since the fixture gives it one edge. Keep every structural invariant (no self-loops, no duplicate undirected edges, GLO nodes are core, `url` shape, degree == incident non-cross edges).
- `test_glossary_ego_graph.py`: the `GLO-027-familie` special case → `GLO-004-shelf`; adjust the "no GLO-GLO edge" assertion, which no longer holds — assert instead that its ego graph contains exactly one glossary-internal edge. Keep the loop over all terms and its invariants unchanged.
- `test_relations_panel.py`: `STK-009-offizieller` → `STK-001-librarian`; `"GLO-007" in out_ids` → `"GLO-003" in out_ids`; `{"STK-002","STK-003"} <= out_ids` → drop (the fixture has no stakeholder-to-stakeholder edges) and replace with `assert "GLO-002" in out_ids`; the FR-backlink assertion holds if you add `related: [[STK-001-librarian]]` to `FR-001-lending`.

- [ ] **Step 4: Run all tests**

```bash
cd "$DST/_system/apps/dashboard"
for t in tests/test_*.py; do echo "--- $t"; .venv/bin/python "$t" || echo "FAILED: $t"; done
```
Expected: every file prints its `OK:` line, no `FAILED:`.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "test(dashboard): run the graph and backlog suites against a neutral fixture vault"
```

---

### Task 6: Translate `app.py` to English

**Files:**
- Modify: `$DST/_system/apps/dashboard/app.py`

**Interfaces:**
- Consumes: the renamed slugs from Task 3 (already English — do not rename again).
- Produces: `FOLDER_LABELS`, `_ID_LABELS` and `REQ42_BLOCKS[*]["title"]` in English. Task 7's templates display these values; the two tasks must agree on the exact wording below.

- [ ] **Step 1: Translate `REQ42_BLOCKS`**

For each of the 12 entries, promote the existing `en:` value into `title:` and delete the now-redundant `en:` key. The resulting titles are:

`01 Business Goals`, `02 Stakeholders`, `03 Scope`, `04 Product Backlog`, `05 Supporting Models`, `06 Quality Requirements`, `07 Constraints`, `08 Domain Terminology`, `09 Assets`, `10 Teams`, `11 Roadmaps`, `12 Risks & Assumptions`.

Translate the four German `note:` fields:

| Block | New `note:` |
|---|---|
| 04 | `One type, stereotype epic\|feature\|story; hierarchy via parent: (ADR-0012).` |
| 09 | `Project resources — deliberately not captured.` |
| 10 | `Organisation / team setup — deliberately not captured.` |
| 11 | `Release planning — deliberately not captured.` |
| 12 | `Issues (especially kind: risk) plus [!assumption] markers.` |

- [ ] **Step 2: Translate `FOLDER_LABELS`**

```python
FOLDER_LABELS = {
    "context": "Context",
    "external-interfaces": "External interface",
    "functional-requirements": "Functional requirement",
    "use-cases": "Use case",
    "activity-models": "Activity model",
    "data-models": "Data model",
    "quality-requirements": "Quality requirement",
    "constraints": "Constraint",
    "glossary": "Glossary term",
    "stakeholders": "Stakeholder",
    "issues": "Issue",
}
```

Update the comment above it: `# Human-readable DE type label per wiki folder` → `# Human-readable type label per wiki folder, for the "Type" column.`

- [ ] **Step 3: Translate `_ID_LABELS`**

```python
    "GLO": "Glossary", "STK": "Stakeholders", "DM": "Data models", "CTX": "Context",
    "EIF": "External interfaces", "GOAL": "Goals", "FR": "Functional requirements",
```
…continuing the same mapping for every remaining prefix in the dict.

- [ ] **Step 4: Translate the tile labels and units in `index()`**

`"Glossar"` → `"Glossary"`, `"Begriffe"` → `"terms"`, `"Stakeholder"` → `"Stakeholders"`, `"Personas"` → `"personas"`, `"Entscheidungen"` → `"decisions"`, `"Einträge"` → `"entries"`, `"Suche"` → `"Search"`, `"Datenmodell"` → `"Data model"`, `"Ziele"`/`"Visionen & Ziele"` → `"Goals"`/`"Vision & goals"`, `"Ziel"` → `"Goal"`, `"Begriffsnetz"` → `"Term network"`, `"Tabelle"` → `"Table"`, `"Domänenbegriffe"` → `"Domain terminology"`, `"Unterstützende Modelle"` → `"Supporting models"`, `"Qualitätsanforderung(en)"` → `"Quality requirement(s)"`, `"Funktionale Anforderung(en)"` → `"Functional requirement(s)"`, `"Aktivitätsmodell(e)"` → `"Activity model(s)"`, `"Schnittstelle"` → `"Interface"`, `"Offen"` → `"Open"`.

Also translate `f"{req42_in_scope} von 12 Blöcken"` → `f"{req42_in_scope} of 12 blocks"`, and `"Zustand (Begriffe)"` → `"State (terms)"`.

- [ ] **Step 5: Translate the German comments and docstrings**

Every German comment and docstring in `app.py` — including the lifecycle block (`_HEARTBEAT_GRACE`, `_STARTUP_GRACE`, `_LEAVE_GRACE`, `_shutdown`, `_watchdog`, `heartbeat_ping`, `heartbeat_leaving`) and the `# Watchdog beim Import starten…` comment — becomes English. Preserve the meaning precisely; these comments explain ADR-0022's shutdown semantics and are the only place that reasoning lives in code.

Leave the regex character classes containing umlauts (`[A-Za-zÄÖÜäöü]`) **unchanged** — they are a superset that still matches English labels, and narrowing them risks breaking body parsing.

- [ ] **Step 6: Verify**

```bash
cd "$DST/_system/apps/dashboard"
grep -nE '(ä|ö|ü|ß|Ä|Ö|Ü)' app.py | grep -v 'A-Za-zÄÖÜäöü'
```
Expected: no output.

```bash
for t in tests/test_*.py; do .venv/bin/python "$t" || echo "FAILED: $t"; done
```
Expected: all `OK:`, no `FAILED:`.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "i18n(dashboard): translate app.py to English"
```

---

### Task 7: Translate the templates to English

96 German lines across 16 template files — not just labels: every `lead` paragraph, breadcrumb, filter button, tooltip and empty hint.

**Files:**
- Modify: all 16 files in `$DST/_system/apps/dashboard/templates/`

**Interfaces:**
- Consumes: the English label wording fixed in Task 6 — reuse it exactly rather than inventing synonyms (e.g. the glossary is `Glossary`, not `Terms`).
- Produces: nothing consumed by later tasks.

- [ ] **Step 1: Translate every user-visible string**

Work file by file. Recurring items and their agreed English:

| German | English |
|---|---|
| `Übersicht` (breadcrumb root) | `Overview` |
| `Alle` / `Alle ansehen` / `Alle Treffer ansehen →` | `All` / `View all` / `View all matches →` |
| `Keine ADRs in dieser Ansicht.` | `No ADRs in this view.` |
| `Keine Issues in dieser Ansicht.` | `No issues in this view.` |
| `Keine Treffer.` / `Keine Treffer — Enter für Volltextsuche` | `No matches.` / `No matches — press Enter for full-text search` |
| `Glossar` / `Begriff` / `Begriffe` | `Glossary` / `Term` / `terms` |
| `Begriffsnetz` | `Term network` |
| `Datenmodell` / `Entität` / `Entitäten` | `Data model` / `Entity` / `entities` |
| `Vision & Ziele` / `Ziel` | `Vision & goals` / `Goal` |
| `Verwaiste Anforderungen` | `Orphaned requirements` |
| `Aufschlüsselung` / `Aufschlüsselung ansehen →` | `Breakdown` / `View breakdown →` |
| `noch keine Stories` / `keine Epics verlinkt` | `no stories yet` / `no epics linked` |
| `Älteste` | `Oldest` |
| `Annahme` | `Assumption` |
| `Offen` | `Open` |
| `Systemkontext · live projiziert aus …` | `System context · projected live from interfaces & data flows (ADR-0013)` |

Rewrite the multi-sentence `lead` paragraphs in `data_model.html`, `graph.html`, `backlog.html`, `adrs.html`, `goals.html` and `req42.html` as natural English prose rather than word-by-word translation — they explain the projections and are read aloud during the workshop.

`glossary.html` line 6 currently reads `Ubiquitäre Sprache der Kinderschwimmliga — eine kanonische Bedeutung je Begriff.` Replace with: `Ubiquitous language of {{ system_name }} — one canonical meaning per term.`

- [ ] **Step 2: Translate the JavaScript comments in `base.html`**

The lifecycle comments (`Lebenszyklus: ein leichter Heartbeat …`, `„settle"-Ping gegen ein spät eintreffendes /leaving`, `echtem Schließen stoppt der Server …`) become English. They document ADR-0022's client half.

- [ ] **Step 3: Verify**

```bash
cd "$DST/_system/apps/dashboard"
grep -rnE '(ä|ö|ü|ß|Ä|Ö|Ü)' templates/
```
Expected: no output.

```bash
.venv/bin/python tests/test_empty_vault.py
```
Expected: `OK: 15 routes render on an empty vault`

- [ ] **Step 4: Look at it**

```bash
cd "$DST" && ./dashboard.sh
```
Click every tile and every breadcrumb. Confirm no German text and no broken Jinja. Then `./dashboard.sh down`.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "i18n(dashboard): translate the templates to English"
```

---

### Task 8: Translate the schema prose and rewrite ADR-0005

**Files:**
- Modify: `$DST/CLAUDE.md`, `$DST/_templates/goal.md`, `$DST/_templates/source.md`, `$DST/_system/workflows/ingest.md`, `$DST/_system/workflows/audit.md`, `$DST/_system/anchors/req42.md`, `$DST/.claude/skills/grill-requirements/SKILL.md`
- Rename + rewrite: `$DST/_system/adr/0005-fachsprache-deutsch.md` → `0005-ubiquitous-language-english.md`

**Interfaces:**
- Consumes: nothing.
- Produces: the ADR filename `0005-ubiquitous-language-english.md`, referenced by `CLAUDE.md`, `ingest.md`, `goal.md`, the grill skill and Task 9's `index.md`. All must cite the new name.

- [ ] **Step 1: Rewrite ADR-0005**

```bash
cd "$DST"
git mv _system/adr/0005-fachsprache-deutsch.md _system/adr/0005-ubiquitous-language-english.md
```

Rewrite its content in the Nygard shape used by the other ADRs (`# ADR-0005: …`, `- **Status:** accepted`, `- **Date:** 2026-09-06`, `## Context`, `## Decision`, `## Consequences`). The decision: **the ubiquitous language of this wiki is English** — every requirement page is captured in English; the agent may converse in any language. Add a `## Note` saying this is a per-project choice: a team whose domain language is not English should re-decide it in a superseding ADR on day one, since the glossary is worthless if it is not in the words the domain experts actually use.

- [ ] **Step 2: Translate `CLAUDE.md`**

Two German passages: the `Conventions → Language` bullet (rewrite to state English, citing ADR-0005 by its new filename) and the German fragments in the content-type table rows for Goal, Context and Functional requirement (`req42 Block 01 „Zielsetzung"`, `Dach-Narrativ`, `PAM-Teilziel`, `Abgrenzung`, …). Also replace the literal `Die Fachsprache für Aquarius ist Deutsch` sentence and any `Aquarius` mention.

- [ ] **Step 3: Translate `_templates/goal.md`**

All frontmatter comments and the Vision/Objective section prose. The Geoffrey Moore vision template becomes:

```
For **<target group>** who **<need / problem>**, **<system>** is a
**<category>** that **<key benefit>**.

*Optional:* `Unlike <alternative>, <differentiator>.`
```

Remove the reference to `[[GOAL-001-aquarius]]` — replace with "omit it for a positive, inviting vision."

- [ ] **Step 4: Translate the remaining files**

- `_templates/source.md` — its single German line.
- `_system/workflows/ingest.md` — the `**Language:**` clause under the grill gate: state English, cite ADR-0005's new filename.
- `_system/workflows/audit.md` — the German `Kontext-Kanten & Projektion` check. English title: `Context edges & projection`. Preserve the substance: the edges (`EIF.flows`, `STK.provides`/`receives`) are the single source of truth (ADR-0013); check that every flow names an existing partner/role, that flows are mutually consistent, and that `build_context_diagram()` renders valid mermaid; there is no drift by construction, so this is a consistency check, not a redraw loop. Drop the `(vgl. ISS-011)` cross-reference — that issue does not exist here.
- `_system/anchors/req42.md` — its single German line.
- `.claude/skills/grill-requirements/SKILL.md` — the `**Language (ADR-0005):**` paragraph.

- [ ] **Step 5: Verify**

```bash
cd "$DST"
grep -rnE '(ä|ö|ü|ß|Ä|Ö|Ü)' CLAUDE.md _templates/ _system/workflows/ _system/anchors/ .claude/
```
Expected: no output.

```bash
grep -rn '0005-fachsprache-deutsch\|GOAL-001-aquarius\|Fachsprache' . --include='*.md' | grep -v docs/superpowers
```
Expected: no output.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "i18n(schema): translate CLAUDE.md, templates and workflows; English ubiquitous language (ADR-0005)"
```

---

### Task 9: Bookkeeping scaffolds and repo documentation

**Files:**
- Create: `$DST/_system/index.md`, `$DST/_system/log.md`, `$DST/README.md`
- Modify: `$DST/_system/README.md`, `$DST/docs/GETTING-STARTED.md`

**Interfaces:**
- Consumes: ADR-0005's new filename from Task 8 (the ADR section of `index.md` lists it).
- Produces: `index.md` section headings that `ingest.md` step 6 writes into — the heading names must match the content types in `CLAUDE.md` exactly.

- [ ] **Step 1: Write the empty `_system/index.md`**

Headings only, no entries, mirroring the Aquarius structure:

```markdown
# Index

Content catalog, one line per page, grouped by type. The agent updates this on
every ingest (`_system/workflows/ingest.md`, step 6).

## Glossary

## Goals

## Stakeholders

## Context

## External interfaces

## Data models

## Activity models

## Use cases

## Functional requirements

## Quality requirements

## Constraints

## Issues

## Sources

## Architecture Decisions (ADR)

- [0000-template](adr/0000-template.md) — ADR-0000, the Nygard template
```

Then add one line per inherited ADR (0001–0024) under the ADR heading, in the same `- [filename](adr/filename.md) — ADR-NNNN, <one-line summary>` shape. Read each ADR's title for the summary; do not invent them.

- [ ] **Step 2: Write the empty `_system/log.md`**

Keep the Aquarius header and format comment verbatim (it documents the greppable prefix), and delete all 690 lines of Aquarius entries beneath it.

- [ ] **Step 3: Update `_system/README.md`**

Add a bullet for `wiki.yaml`: `` `wiki.yaml` — project identity (system name, tagline). Filled in during bootstrap; the dashboard reads it live. `` Also add `scripts/` and `apps/` bullets, which the Aquarius version omits.

- [ ] **Step 4: Write `$DST/README.md`**

Cover, in this order: what this repo is (a ready-to-run, content-free requirements wiki); the three-layer Karpathy pattern in three sentences; quick start (`./dashboard.sh`, then open the folder in Obsidian, then point Claude Code at it); a pointer to `docs/GETTING-STARTED.md` and `docs/WORKSHOP.md`; and a short provenance note: *"Extracted from the arc42 Aquarius demo (github.com/arc42/aquarius), which is the same machinery filled with a worked example. Dashboard improvements there are not automatically synced here."*

- [ ] **Step 5: Update `docs/GETTING-STARTED.md`**

Already English. Three changes: replace the "Unzip `requirements-wiki.zip`" one-time-setup step with cloning/opening this repo; update the "Where things live" tree to this repo's actual layout (root is the vault; add `wiki.yaml`, `raw/examples/`, `reset.sh`, `dashboard.sh`); and add the dashboard to the daily loop — `./dashboard.sh` gives a live browsable view alongside Obsidian.

- [ ] **Step 6: Verify**

```bash
cd "$DST"
grep -c '^## ' _system/index.md          # expect 14
grep -c '^## \[' _system/log.md          # expect 0
test -f README.md && echo "README OK"
```
Expected: `14`, `0`, `README OK`.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "docs: empty index/log scaffolds, repo README, updated getting-started"
```

---

### Task 10: Workshop machinery

**Files:**
- Create: `$DST/_system/workflows/bootstrap.md`, `$DST/reset.sh`, `$DST/raw/examples/interview-notes-example.md`, `$DST/docs/WORKSHOP.md`
- Modify: `$DST/CLAUDE.md` (point at the new workflow), `$DST/dashboard.sh` (`--local` mode)

**Interfaces:**
- Consumes: `_system/wiki.yaml` from Task 2 (bootstrap fills it in); `reset.sh` restores it to blank.
- Produces: `./reset.sh [--force]` and `./dashboard.sh local`.

- [ ] **Step 1: Write `_system/workflows/bootstrap.md`**

The first-30-minutes procedure, in the same voice and shape as `ingest.md` (numbered steps, a "Quality bar" section at the end). Steps: (1) name the system and write `_system/wiki.yaml`; (2) confirm the ubiquitous language, superseding ADR-0005 if the group's domain language is not English; (3) capture `GOAL-001` as the vision using `_templates/goal.md` and the Moore frame; (4) capture the first glossary terms — the words the group has already argued about; (5) capture the first stakeholder; (6) update `_system/index.md` and append to `_system/log.md`; (7) hand off to `ingest.md` for the first real source. Note that bootstrap is **not** grill-gated — the grill gate applies to ingesting sources, and gating the very first page would stall a cold start.

Add a line to `CLAUDE.md`'s "Files you maintain" or workflow pointer section referencing `bootstrap.md` as the cold-start procedure.

- [ ] **Step 2: Write `reset.sh`**

```bash
#!/usr/bin/env bash
#
# Restore the naked state: delete all captured content, keep all machinery.
# Use between workshop runs, or to recover from a live ingest that went wrong.
#
#   ./reset.sh           ask for confirmation, then reset
#   ./reset.sh --force    skip the confirmation
#
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "${1:-}" != "--force" ]; then
  echo "This deletes every page in wiki/, every source in raw/, and empties"
  echo "_system/index.md, _system/log.md and _system/wiki.yaml."
  read -r -p "Reset $ROOT to the naked state? [y/N] " reply
  [ "$reply" = "y" ] || { echo "Aborted."; exit 1; }
fi

find "$ROOT/wiki" -name '*.md' -delete
find "$ROOT/raw" -maxdepth 1 -type f -delete
find "$ROOT/raw/sources" "$ROOT/raw/ingested" -name '*.md' -delete
git -C "$ROOT" checkout -- _system/index.md _system/log.md _system/wiki.yaml
echo "✓ Reset. wiki/ is empty; machinery untouched."
```

`chmod +x reset.sh`.

> The `git checkout` restores the three bookkeeping files to their committed scaffolds — which is why Task 9 must commit them first.

- [ ] **Step 3: Write the fallback demo source**

`raw/examples/interview-notes-example.md`: about one page of fictional stakeholder-interview notes for a neutral domain (a library lending system — the same one the test fixtures use, so the two reinforce each other). Include deliberate raw-material texture: two people using different words for the same thing, one unquantified quality wish ("it should be fast"), one contradiction, and one unnamed stakeholder. That gives a live ingest something real to find and something real to raise Issues about.

Add a one-line header note: *"Not workshop content — a fallback source for demonstrating ingest when live material isn't ready. Copy it up into `raw/` to use it."*

- [ ] **Step 4: Write `docs/WORKSHOP.md`**

The facilitator script: a suggested agenda with timings; which workflow to run at each point (`bootstrap` → `ingest` → `grill` → `audit` → `report`); what to narrate while the agent works; the recovery moves (`./reset.sh`, `git checkout`, the `raw/examples/` fallback); and a pre-flight checklist (Docker running, Claude Code authenticated, `./dashboard.sh` opens clean, projector legibility checked).

- [ ] **Step 5: Add `--local` mode to `dashboard.sh`**

Add a `local` command to the existing `case` statement that runs Flask directly, for machines where Docker will not start:

```bash
  local)
    cd "$ROOT/_system/apps/dashboard"
    if [ ! -d .venv ]; then
      python3 -m venv .venv
      .venv/bin/pip install -q -r requirements.txt
    fi
    export WIKI_DIR ADR_DIR CONFIG_FILE
    export WIKI_CONFIG="$CONFIG_FILE"
    echo "✓ Dashboard (local, no Docker) on http://localhost:8000"
    open_browser_at "http://localhost:8000"
    exec .venv/bin/python app.py
    ;;
```

Refactor the existing `open_browser` into `open_browser_at <url>` so both modes share it, and update the usage comment block at the top of the file and the `*)` error branch to list `local`.

- [ ] **Step 6: Verify**

```bash
cd "$DST"
bash -n reset.sh && bash -n dashboard.sh && echo "syntax OK"
./dashboard.sh local    # visit http://localhost:8000, then Ctrl-C
```
Expected: `syntax OK`, and the dashboard renders its empty state without Docker.

Then verify the reset is a no-op on an already-clean tree:
```bash
./reset.sh --force && git status --short
```
Expected: no modified files.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: workshop machinery — bootstrap workflow, reset script, demo source, facilitator guide"
```

---

### Task 11: Translate and neutralise the ADRs

**Cuttable for the first workshop run.** Nine dense German documents that nobody reads live. Do it if time allows; skip it and the repo still works.

**Files:**
- Modify: `$DST/_system/adr/` — 0006, 0007, 0013, 0014, 0016, 0018, 0022, 0023, 0024 (full translation); 0010, 0015, 0017, 0019, 0020, 0021 (English already, domain examples only); 0024 (brand neutralisation)

**Interfaces:**
- Consumes: nothing.
- Produces: nothing. Pure documentation.

- [ ] **Step 1: Translate the nine German ADRs**

Preserve the Nygard structure (`## Context`, `## Decision`, `## Consequences`) and every cross-reference (`[[ADR-00NN]]`, template and folder names) exactly. Translate the reasoning faithfully — these documents are why the wiki is shaped as it is, and a workshop participant who reads one should get the full argument.

- [ ] **Step 2: Neutralise the domain examples**

Across all 24 ADRs, replace Kinderschwimmliga examples with neutral placeholders — `Entity A`, `System X`, `Role R`, `GLO-001`, `DM-002`. Do **not** substitute another fictional domain: a second worked example competes for attention with the domain the workshop is actually modelling.

`ADR-0020` (19 domain hits) and `ADR-0021` (11) are the heaviest; `ADR-0014` (6) and `ADR-0019` (7) next.

- [ ] **Step 3: Rewrite ADR-0024 (graphical brand)**

Strip the Aquarius brand specifics (logo files, colour choices, the header artwork removed in Task 1). Keep the principle: the dashboard carries a project identity, it comes from `wiki.yaml`, and the req42 logo is the one fixed mark.

- [ ] **Step 4: Verify**

```bash
cd "$DST"
grep -rnE '(ä|ö|ü|ß|Ä|Ö|Ü)' _system/adr/
grep -rniE 'aquarius|kinderschwimm|schwimm|wettkampf|verein|figur|kader|drsl' _system/adr/
```
Expected: no output from either.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "docs(adr): translate to English and neutralise domain examples"
```

---

### Task 12: The naked run

The acceptance test. Not automatable — it is the workshop, rehearsed.

**Files:** none modified (unless the run finds defects).

**Interfaces:**
- Consumes: everything.
- Produces: a green light, or a defect list to fix before the workshop.

- [ ] **Step 1: Verify the repo is clean of Aquarius**

```bash
cd "$DST"
grep -riE 'aquarius|kinderschwimm|schwimm|wettkampf|verein|figur|kader|drsl' . \
  --include='*.md' --include='*.py' --include='*.html' --include='*.sh' --include='*.yaml' \
  | grep -v 'docs/superpowers/' | grep -v '^./README.md'
```
Expected: no output.

- [ ] **Step 2: Verify the full test suite**

```bash
cd "$DST/_system/apps/dashboard"
for t in tests/test_*.py; do echo "--- $t"; .venv/bin/python "$t" || echo "FAILED: $t"; done
```
Expected: every file prints `OK:`, no `FAILED:`.

- [ ] **Step 3: The cold start**

```bash
cd /tmp && rm -rf tsu-demo-check && git clone "$DST" tsu-demo-check && cd tsu-demo-check
./dashboard.sh
```
Click every tile and every breadcrumb. Every view shows its empty state; nothing is blank, broken or German.

- [ ] **Step 4: The first entry**

In the clone, run the bootstrap workflow with Claude Code: name the system, write `GOAL-001`, add two glossary terms. Refresh the dashboard.

Expected: the hero shows the chosen system name; the glossary tile reads 2; the goals tile shows the vision; `_system/index.md` and `_system/log.md` have their first entries.

- [ ] **Step 5: The first ingest**

Copy `raw/examples/interview-notes-example.md` into `raw/` and run the ingest workflow end to end.

Expected: the grill gate fires before any page is written; 8–15 pages are created; at least one Issue is raised; the source is archived to `raw/ingested/` with an `SRC-001` record in `raw/sources/`; the term network renders with real edges. This is the step that catches a mistranslated `**Definition.**` heading — if a detail page shows an empty section, a template and its parser have drifted apart.

- [ ] **Step 6: Reset and confirm repeatability**

```bash
./reset.sh --force && git status --short
```
Expected: no modified files — the repo is back to naked and ready for the next run.

- [ ] **Step 7: Record the outcome**

Append a `## [YYYY-MM-DD] naked run` entry to `$DST/docs/WORKSHOP.md` under a "Rehearsal log" heading, noting what worked and any defects found. Fix defects before the workshop; commit fixes individually.

```bash
cd "$DST" && git add -A && git commit -m "docs: record the naked-run rehearsal"
```
