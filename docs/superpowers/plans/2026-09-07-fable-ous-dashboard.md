# Fable-ous Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the read-only requirements dashboard into a req42-ordered, distinctively typeset, self-explaining view with maturity bars, issue flags, a QR join code and provenance chips, and fix the bugs the critique found.

**Architecture:** Flask app `_system/apps/dashboard/app.py` parses the Obsidian vault live on every request and renders Jinja templates; all styling is one stylesheet with two CSS-token palettes (dark default, light opt-in). Every asset is vendored so the dashboard works offline. Changes stay inside `_system/apps/dashboard/` plus `dashboard.sh`, one ADR, and the index line for it.

**Tech Stack:** Python 3.12, Flask 3, Python-Markdown, PyYAML, segno (new, pure Python QR), vanilla JS, vendored woff2 fonts. Tests are plain-`assert` scripts, no pytest.

**Spec:** `docs/superpowers/specs/2026-09-07-fable-ous-dashboard-design.md`

## Global Constraints

- Work on branch `fable-ous-dashboard` (already created). Commit after every task; never commit `.venv/` or `__pycache__/`.
- All work under `_system/apps/dashboard/` unless a task names another path. Never edit anything in `wiki/`, `raw/`, `_templates/`.
- **Offline at runtime:** no CDN, no Google Fonts link, no external requests from the page. Fonts are vendored files under `static/vendor/fonts/`.
- **Two themes, tokens only:** every colour used in `style.css` is a `--token` defined in BOTH the `:root {}` block and the `:root[data-theme="light"] {}` block. Translucent `rgba()` accent washes are the only allowed literal colours.
- **No emoji** in templates or app.py UI strings. Plain typographic arrows (`→`) are fine.
- **Copy:** the word "participant" does not appear in any template, JS string, JSON key, README line or docstring: the word is **client** / **clients**. Plurals are always correct ("1 client", "2 clients").
- **Empty vault renders:** every GET route returns 200 on a vault with zero pages (`tests/test_empty_vault.py` guards this; extend its route list when adding routes).
- **IDs stay stable**; filenames `TYPE-NNN-kebab-title.md`.
- **Test runner** (from `_system/apps/dashboard/`, run before every commit):
  ```bash
  cd _system/apps/dashboard
  [ -x .venv/bin/python ] || (python3 -m venv .venv && .venv/bin/pip install -q --disable-pip-version-check -r requirements.txt)
  for t in tests/test_*.py; do .venv/bin/python "$t" || { echo "FAILED: $t"; break; }; done
  ```
  Every test file is a script: module-level env setup (temp vault, `DASH_STARTUP_GRACE=3600`, `DASH_HEARTBEAT_GRACE=3600`), `import app`, functions named `test_*`, and an `if __name__ == "__main__":` block that calls each one and prints `OK`. Copy the shape of `tests/test_presence.py`.
- Never call `/leaving` in tests (it arms the shutdown watchdog).
- English everywhere. Commit messages end with the Co-Authored-By / Claude-Session trailer shown in the first commit on this branch (`git log -1 --format=%B`).

---

### Task 1: "Clients", plurals, empty-state copy, footer time zone

**Files:**
- Modify: `templates/base.html` (footer presence span, confirm dialog string, JS)
- Modify: `templates/who.html` (heading pill, render(), JSON key)
- Modify: `templates/_empty.html` (new `empty_adrs` macro)
- Modify: `templates/index.html` (ADR tile empty state, Vision tile empty objectives)
- Modify: `templates/adrs.html` (empty state)
- Modify: `app.py` (`presence_list` JSON key, docstrings, `DISPLAY_TZ`)
- Modify: `README.md`, `dashboard.sh` (repo root), `tests/test_presence.py`
- Test: `tests/test_copy.py` (new)

**Interfaces:**
- Produces: `/presence/list` → `{"clients": [...]}` (key renamed from `participants`). Footer markup `<span id="presence-count">N</span> <span id="presence-unit">clients</span>`. Macro `empty_adrs()` in `_empty.html`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_copy.py`:

```python
"""UI copy contract: "client(s)" with correct plurals, empty states that name
the right next step, and no "participant" anywhere. No pytest.

Run from the dashboard dir:
    .venv/bin/python tests/test_copy.py
"""
import json
import os
import re
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
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

import app  # noqa: E402

VISION = """---
id: GOAL-001
type: goal
title: A vision without objectives
status: draft
created: 2026-09-07
updated: 2026-09-07
sources: []
related: []
tags: [goal]
stereotype: vision
tile_claim: "Every piece accounted for."
---

# A vision without objectives
"""


def _client():
    app._PARSE_CACHE.clear()
    return app.app.test_client()


def test_no_participant_wording_anywhere():
    bad = re.compile(r"participant", re.IGNORECASE)
    for p in list((HERE / "templates").glob("*.html")) + [HERE / "app.py", HERE / "README.md"]:
        assert not bad.search(p.read_text(encoding="utf-8")), f"'participant' still in {p.name}"


def test_presence_list_uses_clients_key():
    c = _client()
    c.post("/ping", data=json.dumps({"client_id": "yoda"}), content_type="application/json")
    c.post("/ping", data=json.dumps({"client_id": "someone"}), content_type="application/json")
    d = c.get("/presence/list").get_json()
    assert "clients" in d and "participants" not in d, d


def test_footer_has_a_pluralisable_unit():
    body = _client().get("/glossary").get_data(as_text=True)
    assert 'id="presence-unit"' in body
    assert 'id="presence-count"' in body


def test_adr_empty_state_does_not_suggest_ingest():
    body = _client().get("/adrs").get_data(as_text=True)
    assert "architecture decision" in body.lower()
    assert "raw/" not in body, "ADRs are never produced by ingesting raw/"
    home = _client().get("/").get_data(as_text=True)
    start = home.index("tile-adrs")
    assert "raw/" not in home[start:start + 900]


def test_vision_without_objectives_has_a_hint():
    (_wiki / "goals" / "GOAL-001-vision.md").write_text(VISION, encoding="utf-8")
    try:
        body = _client().get("/").get_data(as_text=True)
        assert "Every piece accounted for." in body
        assert "No objectives yet" in body
    finally:
        (_wiki / "goals" / "GOAL-001-vision.md").unlink()


if __name__ == "__main__":
    test_no_participant_wording_anywhere()
    test_presence_list_uses_clients_key()
    test_footer_has_a_pluralisable_unit()
    test_adr_empty_state_does_not_suggest_ingest()
    test_vision_without_objectives_has_a_hint()
    print("OK: copy contract")
```

Note: `app._PARSE_CACHE` is the module-level parse cache (see `_parse`). If `load_goals()` detects the vision differently than `stereotype: vision`, read `load_goals()` first and adjust the fixture, not the assertion.

- [ ] **Step 2: Run it, confirm it fails**

Run: `.venv/bin/python tests/test_copy.py`
Expected: AssertionError on `test_no_participant_wording_anywhere`.

- [ ] **Step 3: Rename to clients**

In `app.py`: `presence_list` returns `{"clients": rows}`; rewrite the docstrings of `presence_count`, `presence_list`, `_facilitator_client_id` and the comment near line 1961 so the word "participant" is gone ("client" / "viewer" / "everyone else"). In `README.md` line ~30 replace "participant count" with "client count".

In `templates/base.html`:
```html
<span class="presence" id="presence" hidden>
  <span class="presence-dot" aria-hidden="true"></span>
  <span class="presence-count" id="presence-count">0</span>
  <span class="presence-unit" id="presence-unit">clients</span>
</span>
```
In the `updatePresence()` success branch add:
```js
var presenceUnitEl = document.getElementById("presence-unit");
...
presenceCountEl.textContent = d.count;
if (presenceUnitEl) { presenceUnitEl.textContent = d.count === 1 ? "client" : "clients"; }
```
(declare `presenceUnitEl` next to `presenceCountEl`). Confirm dialog:
```js
var n = parseInt(presenceCountEl.textContent, 10) || 0;
var who = n === 1 ? "1 other client" : n + " other clients";
if (!window.confirm("Disconnect " + who + " and stop the dashboard?")) { return; }
```
Comment near "a participant sees the 'session ended' state" → "a client sees".

In `templates/who.html`: pill text `0 clients`; `render(clients)` with `clients.length === 1 ? " client" : " clients"`; `refresh()` reads `d.clients || []`; lead copy: "Everyone with this dashboard open right now — a fun nickname, not a real name. Updates live; close the tab and you drop off the list."

In `tests/test_presence.py`: `grep -n participants tests/test_presence.py` and rename the JSON key in any assertion to `clients`.

- [ ] **Step 4: Empty-state copy**

`templates/_empty.html`, add:
```html
{% macro empty_adrs() %}
<p class="empty-state">
  No architecture decisions yet — the agent records one under <code>_system/adr/</code>
  whenever it makes a structural decision; you can also ask: <em>“record an ADR for …”</em>.
</p>
{% endmacro %}
```
Import it where `empty_state` is imported in `index.html` and `adrs.html`, and use `{{ empty_adrs() }}` for the ADR tile (`{% elif t.key == 'adrs' %}` branch) and the empty ADR page.

Vision tile (`index.html`, the `t.key == 'vision' and t.active` branch): after the `Goals` header,
```html
{% if t.objective_rows %}
<ul class="mini-list mini-list-vision">…existing rows…</ul>
{% else %}
<p class="empty-state empty-state-tight">No objectives yet — ask the agent:
  <em>“derive objectives from the vision”</em>.</p>
{% endif %}
```
Add to `style.css` next to `.empty-state`: `.empty-state-tight { margin: .2rem 0 .4rem; }`.

- [ ] **Step 5: Footer time zone**

`app.py`: `DISPLAY_TZ = os.environ.get("TZ") or ""` and in `inject_refresh_time`:
```python
tz = None
if DISPLAY_TZ:
    try:
        tz = ZoneInfo(DISPLAY_TZ)
    except (ZoneInfoNotFoundError, ValueError):
        tz = None
now = datetime.now(tz) if tz else datetime.now().astimezone()   # host's local zone
```
Repo-root `dashboard.sh`, right after the `export CONFIG_FILE=` line:
```bash
# Footer time in the host's zone, not UTC: Docker containers default to UTC.
if [ -z "${TZ:-}" ] && [ -L /etc/localtime ]; then
  TZ="$(readlink /etc/localtime | sed 's#.*/zoneinfo/##')"
fi
export TZ="${TZ:-UTC}"
```
(`compose.yaml` already forwards `TZ`.)

- [ ] **Step 6: Run the whole suite, then commit**

Run the test runner from Global Constraints. Expected: every file prints `OK`.
```bash
git add -A _system/apps/dashboard dashboard.sh
git commit -m "dashboard: clients wording with plurals, honest empty states, local time zone"
```

---

### Task 2: Live search counts and unwrapped prose

**Files:**
- Modify: `templates/search.html`
- Modify: `app.py` (`render_markdown`, new `_unwrap_prose`)
- Test: `tests/test_markdown.py` (new), `tests/test_copy.py` (one more test)

**Interfaces:**
- Produces: `app._unwrap_prose(body: str) -> str`; `render_markdown` no longer uses `nl2br`.

- [ ] **Step 1: Failing tests**

Create `tests/test_markdown.py` (same module-level setup as `tests/test_copy.py`, temp empty vault):
```python
def test_hard_wrapped_prose_is_one_paragraph():
    html = app.render_markdown("First line of a\nwrapped paragraph.\n\nSecond.", {})
    assert "<br" not in html, html
    assert "<p>First line of a wrapped paragraph.</p>" in html, html


def test_list_directly_after_prose_line_is_a_list():
    html = app.render_markdown("**Goals.** PAM (light)\n- one thing\n- two things", {})
    assert "<ul>" in html and "<li>one thing</li>" in html, html


def test_wrapped_list_item_stays_one_item():
    html = app.render_markdown("- Replace the ad-hoc\n  coordination.\n- Second item", {})
    assert html.count("<li>") == 2, html
    assert "ad-hoc coordination" in html.replace("\n", " "), html


def test_fenced_code_is_untouched():
    html = app.render_markdown("```\nline a\nline b\n```", {})
    assert "line a\nline b" in html, html


def test_explicit_two_space_break_is_kept():
    html = app.render_markdown("roses are red  \nviolets are blue", {})
    assert "<br" in html, html
```
Add to `tests/test_copy.py`:
```python
def test_search_counts_are_live():
    body = _client().get("/search").get_data(as_text=True)
    assert 'id="search-total"' in body
    assert 'data-total=' in body
    assert "function updateCounts" in body
```

- [ ] **Step 2: Run, confirm failures** (`<br` present; `updateCounts` missing).

- [ ] **Step 3: Implement `_unwrap_prose`** in `app.py` directly above `render_markdown`:

```python
# Lines that START a markdown block. A prose line that follows one of these
# is left for Markdown's own lazy-continuation rules; a prose line that
# follows another prose line is a hard wrap in the source file and is joined.
_BLOCK_START_RE = re.compile(r"^(\s*([-*+]|\d+[.)])\s|\s*#|\s*>|\s*\||\s*```|\s{4,}\S|\t|\s*<)")
_LIST_START_RE = re.compile(r"^\s*([-*+]|\d+[.)])\s")


def _unwrap_prose(body: str) -> str:
    """Join hard-wrapped prose lines into one line per paragraph, and give a
    list that follows a prose line the blank line Python-Markdown needs.
    Agents write wiki pages wrapped at ~80 columns; rendering those wraps as
    <br> (the old `nl2br` extension) produced ragged paragraphs. Fenced code,
    explicit two-space line breaks, lists, quotes, tables and headings are
    passed through untouched."""
    out: list[str] = []
    in_fence = False
    for line in body.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        prev = out[-1] if out else ""
        prev_is_prose = bool(prev.strip()) and not _BLOCK_START_RE.match(prev)
        if in_fence or not stripped or _BLOCK_START_RE.match(line):
            if not in_fence and prev_is_prose and _LIST_START_RE.match(line):
                out.append("")            # prose → list needs a separating blank line
            out.append(line)
            continue
        if prev_is_prose and not prev.endswith("  "):
            out[-1] = prev.rstrip() + " " + stripped
        else:
            out.append(line)
    return "\n".join(out)
```
and in `render_markdown` replace the last line with:
```python
return md.markdown(_unwrap_prose(body), extensions=["extra", "sane_lists"])
```
Run the suite: `tests/test_populated_render.py` or others may assert `<br`; if so, update those assertions to the new behaviour (they were asserting the bug).

- [ ] **Step 4: Live counts in `search.html`**

Heading: `<h1 class="page-h1">Search <span class="count-pill" id="search-total" data-total="{{ total }}">{{ total }}</span></h1>`.
Buttons: `<button class="fbtn active" data-type="all" data-total="{{ total }}">All <span class="fnum">{{ total }}</span></button>` and the same `data-total="{{ count }}"` on each facet button.
JS, after `setScore`:
```js
const totalEl = document.getElementById('search-total');
function updateCounts(perType) {
  // perType == null → back to corpus totals (no query)
  let all = 0;
  buttons.forEach(b => {
    const t = b.dataset.type;
    if (t === 'all') return;
    const n = perType ? (perType[t] || 0) : parseInt(b.dataset.total, 10);
    b.querySelector('.fnum').textContent = n;
    all += n;
  });
  const allBtn = document.querySelector('.fbtn[data-type="all"]');
  const total = perType ? all : parseInt(allBtn.dataset.total, 10);
  allBtn.querySelector('.fnum').textContent = total;
  totalEl.textContent = total;
}
```
In `apply()`, when `query` is set, count matches per type over ALL results (ignoring `activeType`, so the pills answer "how many hits of each type") and call `updateCounts(perType)`; in both other branches call `updateCounts(null)`:
```js
if (query) {
  const tokens = query.split(/\s+/).filter(Boolean);
  const scored = [];
  const perType = {};
  allResults.forEach(el => {
    const r = relevance(el, tokens, query);
    if (r > 0) { perType[el.dataset.type] = (perType[el.dataset.type] || 0) + 1; }
    const typeOK = activeType === 'all' || el.dataset.type === activeType;
    if (r > 0 && typeOK) { … push as before … } else { el.hidden = true; }
  });
  updateCounts(perType);
  …
}
```

- [ ] **Step 5: Run suite, commit**

```bash
git add -A _system/apps/dashboard
git commit -m "dashboard: search counts follow the query; unwrap hard-wrapped prose instead of nl2br"
```

---

### Task 3: Visual identity — vendored fonts, flat tokens, no emoji

**Files:**
- Create: `static/vendor/fonts/BricolageGrotesque-var.woff2`, `static/vendor/fonts/JetBrainsMono-400.woff2`, `static/vendor/fonts/JetBrainsMono-600.woff2`
- Modify: `static/vendor/README.md`, `static/style.css`, `templates/index.html`, `templates/base.html`, `app.py` (drop `"icon"` keys)
- Test: `tests/test_design_tokens.py` (new)

**Interfaces:**
- Produces CSS tokens: `--font-text`, `--font-mono`, `--radius: 8px`, `--space-1: .25rem … --space-6: 3rem`, type steps `--step--1 … --step-3`. Tile classes `.tile`, `.tile-head`, `.tile-eyebrow`, `.tile-title`, `.tile-count .num/.unit`, `.tile-cta`, `.mini-list` keep their names (Task 4 fills them).

- [ ] **Step 1: Failing test** `tests/test_design_tokens.py` (no app import needed):

```python
"""Design-system contract for style.css and the templates. No pytest."""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CSS = (HERE / "static" / "style.css").read_text(encoding="utf-8")
FONTS = HERE / "static" / "vendor" / "fonts"
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿\U0001F000-\U0001F2FF]")


def test_fonts_are_vendored():
    for name in ("BricolageGrotesque-var.woff2", "JetBrainsMono-400.woff2", "JetBrainsMono-600.woff2"):
        f = FONTS / name
        assert f.is_file() and f.stat().st_size > 10_000, name
    assert CSS.count("@font-face") == 3
    assert "fonts.googleapis.com" not in CSS


def test_no_gradients_or_glow():
    assert "linear-gradient" not in CSS and "radial-gradient" not in CSS
    assert "--glow" not in CSS


def test_no_emoji_in_ui():
    for p in list((HERE / "templates").glob("*.html")) + [HERE / "app.py"]:
        txt = p.read_text(encoding="utf-8")
        m = EMOJI.search(txt)
        assert not m, f"emoji {m.group()!r} in {p.name}"


def _block(selector):
    i = CSS.index(selector + " {")
    return CSS[i:CSS.index("}", i)]


def test_every_token_exists_in_both_themes():
    dark = set(re.findall(r"--[\w-]+(?=\s*:)", _block(":root")))
    light = set(re.findall(r"--[\w-]+(?=\s*:)", _block(':root[data-theme="light"]')))
    structural = {t for t in dark if not t.startswith(("--font", "--radius", "--space", "--step"))}
    assert structural <= light, f"missing in light theme: {sorted(structural - light)}"
    assert light <= dark, f"only in light theme: {sorted(light - dark)}"


if __name__ == "__main__":
    test_fonts_are_vendored()
    test_no_gradients_or_glow()
    test_no_emoji_in_ui()
    test_every_token_exists_in_both_themes()
    print("OK: design tokens")
```

- [ ] **Step 2: Run it, confirm it fails** (fonts missing).

- [ ] **Step 3: Vendor the fonts** (both OFL 1.1). From `_system/apps/dashboard/static/vendor`:
```bash
mkdir -p fonts && cd fonts
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
curl -sf -A "$UA" "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..800&display=swap" -o /tmp/bric.css
curl -sf -A "$UA" "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap" -o /tmp/jb.css
latin_urls() { sed -n '/\/\* latin \*\//,/}/p' "$1" | grep -o 'https://[^)]*'; }
curl -sf -o BricolageGrotesque-var.woff2 "$(latin_urls /tmp/bric.css | head -1)"
curl -sf -o JetBrainsMono-400.woff2 "$(latin_urls /tmp/jb.css | sed -n 1p)"
curl -sf -o JetBrainsMono-600.woff2 "$(latin_urls /tmp/jb.css | sed -n 2p)"
ls -la *.woff2
```
Each file must be > 10 KB. Check the weights: `/tmp/jb.css` lists the 400 block before the 600 block; verify with `grep -n "font-weight" /tmp/jb.css`. Append to `static/vendor/README.md`:
```markdown
## fonts/ (Bricolage Grotesque, JetBrains Mono)
- **Bricolage Grotesque** (variable, opsz 12–96, wght 300–800; latin subset) — <https://github.com/ateliertriay/bricolage>, SIL Open Font License 1.1. Text, headings and numbers.
- **JetBrains Mono** 400 + 600 (latin subset) — <https://github.com/JetBrains/JetBrainsMono>, SIL Open Font License 1.1. IDs, code, eyebrows.
- **Source:** latin-subset woff2 files as served by the Google Fonts CSS API (`fonts.googleapis.com/css2?family=…`), fetched once and vendored; nothing is loaded from Google at runtime.
```

- [ ] **Step 4: Tokens and type** at the top of `style.css` (before `:root`):
```css
@font-face { font-family: "Bricolage Grotesque"; src: url("vendor/fonts/BricolageGrotesque-var.woff2") format("woff2");
  font-weight: 300 800; font-display: swap; }
@font-face { font-family: "JetBrains Mono"; src: url("vendor/fonts/JetBrainsMono-400.woff2") format("woff2");
  font-weight: 400; font-display: swap; }
@font-face { font-family: "JetBrains Mono"; src: url("vendor/fonts/JetBrainsMono-600.woff2") format("woff2");
  font-weight: 600; font-display: swap; }
```
Inside `:root {}` (dark block only; the test exempts these prefixes):
```css
--font-text: "Bricolage Grotesque", "Segoe UI", Helvetica, Arial, sans-serif;
--font-mono: "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;
--radius: 8px;
--space-1: .25rem; --space-2: .5rem; --space-3: .85rem; --space-4: 1.25rem; --space-5: 2rem; --space-6: 3.25rem;
--step--1: .86rem; --step-0: 1rem; --step-1: 1.2rem; --step-2: 1.55rem; --step-3: clamp(2rem, 1.4rem + 1.8vw, 2.7rem);
```
Then: `body { font-family: var(--font-text); background: var(--bg); … }` (remove the radial gradient), `code { font-family: var(--font-mono); }`, `.page-h1 { font-size: var(--step-3); font-weight: 700; letter-spacing: -.025em; }`, `h2 { letter-spacing: -.01em; }`. Delete the `--glow`, `--vision-1/2/3`, `--vision-edge` tokens from both palettes and every rule that used them (the vision goal card gets `background: var(--card-2); border-left: 3px solid var(--accent);`). Set `--shadow` to `none` in both palettes and remove `box-shadow: var(--shadow)` everywhere except keep the token defined (other rules may reference it).

- [ ] **Step 5: Flat tiles, no emoji**

Replace the `.tile*` block (lines ~145–193) with:
```css
.tiles { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-4); }
@media (max-width: 900px) { .tiles { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 640px) { .tiles { grid-template-columns: 1fr; } }
.tile { display: flex; flex-direction: column; background: var(--card); border: 1px solid var(--line);
  border-radius: var(--radius); padding: var(--space-3) var(--space-4) var(--space-3);
  text-decoration: none; color: var(--ink); position: relative; transition: border-color .15s ease; }
.tile-link:hover, .tile:focus-within { border-color: var(--accent); }
.tile-span-2 { grid-column: span 2; }
@media (max-width: 640px) { .tile-span-2 { grid-column: span 1; } }
.tile-head { display: flex; flex-direction: column; gap: .15rem; margin-bottom: var(--space-2); }
.tile-eyebrow { font: 600 .7rem/1.4 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--ink-dim); }
.tile-title { font-size: var(--step-1); font-weight: 650; margin: 0; letter-spacing: -.01em; }
.tile-count { display: flex; align-items: baseline; gap: .5rem; margin: 0 0 .15rem; }
.tile-count .num { font-size: 2.3rem; font-weight: 500; letter-spacing: -.03em; line-height: 1; font-variant-numeric: tabular-nums; }
.tile-count .unit { color: var(--ink-soft); font-size: var(--step--1); }
.tile-cta { display: inline-block; margin-top: auto; padding-top: var(--space-2); color: var(--accent); font-size: var(--step--1); font-weight: 600; }
.tile-ctas { display: flex; gap: var(--space-4); margin-top: auto; }
.tile-ctas .tile-cta { margin-top: 0; }
.tile-ctas .tile-cta:hover { text-decoration: underline; }
```
Delete `.tile::before` and every `.tile-<key>::before` rule, `.tile-muted`, `.tile-logo`, `.tile-subcount`, `.tile-icon`, and the `.tile-search*` rules. In `index.html` remove every `<span class="tile-icon">…</span>` and change `<h2>{{ t.label }}</h2>` to `<h2 class="tile-title">{{ t.label }}</h2>` (Task 4 rewrites the tile body anyway; here just make it render without emoji). In `app.py` remove every `"icon": "…"` entry from the tile dicts. In `base.html` the theme toggle becomes text only: `<span class="theme-toggle-label">Light theme</span>` and the JS no longer writes `&#9728;`/`&#9790;` (remove the `icon` element and its updates). Grep once more: `grep -nP "[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]" templates/*.html app.py` must be empty (`⚠`, `🔎`, `🎯`, `👥`, `🏛`, `🗂`, `📖`, `🧩` are the known offenders; the `👤` inside the mermaid *diagram source* in `build_context_diagram` counts too — replace it with the word `Person` in the node label).

- [ ] **Step 6: Run everything, screenshot, commit**

Run the test runner. Then a visual check (playwright's headless shell exists on this machine):
```bash
cd _system/apps/dashboard && DASH_STARTUP_GRACE=3600 DASH_HEARTBEAT_GRACE=3600 DASH_LEAVE_GRACE=3600 WIKI_DIR=$PWD/tests/fixtures/wiki ADR_DIR=$PWD/tests/fixtures/adr WIKI_CONFIG=$PWD/../../wiki.yaml .venv/bin/python app.py & sleep 2
CH=$(ls -d ~/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell | tail -1)
"$CH" --headless --no-sandbox --disable-gpu --hide-scrollbars --window-size=1400,1300 --virtual-time-budget=6000 --screenshot=/tmp/home.png http://localhost:8000/
kill %1
```
Look at `/tmp/home.png` (Read tool): no emoji, no stripes, fonts visibly changed (Bricolage has a distinctive single-storey `a`). Commit:
```bash
git add -A _system/apps/dashboard
git commit -m "dashboard: flat visual identity with vendored Bricolage Grotesque + JetBrains Mono, no emoji"
```

---

### Task 4: Home page in req42 order, persistent navigation, latest changes

**Files:**
- Modify: `app.py` (`Page` dataclass, `_parse`, `index()`, new `SOURCES_DIR`, `load_sources()`, `recent_changes()`, `vault_status()`)
- Modify: `templates/index.html` (rewrite tile bodies), `templates/base.html` (topbar → nav), `static/style.css` (nav, hero, status strip, changes tile)
- Modify: `README.md` (tiles table), `Dockerfile` (`RAW_SOURCES_DIR=/sources`), `compose.yaml` (mount), `dashboard.sh` (`SOURCES_DIR`)
- Test: `tests/test_home_layout.py` (new); update `tests/test_empty_vault.py` if its vision-tile slice breaks

**Interfaces:**
- Consumes: tile CSS from Task 3; `empty_state`, `empty_bootstrap`, `empty_adrs` macros.
- Produces: `Page.mtime: float`; `SOURCES_DIR: Path`; `load_sources() -> list[Page]` (folder name `"sources"`); `recent_changes(n=5) -> list[dict]` with keys `id, title, kind, url, when` (`when` is `"3 min ago"` / `"2 h ago"` / `"2026-09-06"`); `vault_status() -> dict(pages, open_issues, sources, last_change)`; every tile dict has `key, label, eyebrow, href, folders (list[str])` and either `count/unit(/sub)` or `active=False`. Tile keys in order: `vision, stakeholders, scope, backlog, models, quality, constraints, glossary, issues, adrs, changes`. Templates use the nav markup `<nav class="mainnav">` and `<input id="nav-search">`.

- [ ] **Step 1: Failing test** `tests/test_home_layout.py` (module setup like `tests/test_copy.py`, plus `os.environ["RAW_SOURCES_DIR"] = str(_tmp / "sources")` with that dir created):

```python
QR = """---
id: QR-001
type: quality-requirement
title: Fast checkout
status: draft
created: 2026-09-07
updated: 2026-09-07
sources: []
related: []
tags: [quality-requirement]
---

# Fast checkout
"""
ORDER = ["tile-vision", "tile-stakeholders", "tile-scope", "tile-backlog", "tile-models",
         "tile-quality", "tile-constraints", "tile-glossary", "tile-issues", "tile-adrs", "tile-changes"]


def _home():
    app._PARSE_CACHE.clear()
    return app.app.test_client().get("/").get_data(as_text=True)


def test_tiles_follow_req42_reading_order():
    body = _home()
    positions = [body.index(k) for k in ORDER]          # raises if a tile is missing
    assert positions == sorted(positions), positions
    assert "tile-req42" not in body and "tile-search" not in body


def test_every_page_has_the_main_nav():
    c = app.app.test_client()
    for route in ("/", "/glossary", "/issues", "/req42/backlog"):
        body = c.get(route).get_data(as_text=True)
        assert 'class="mainnav"' in body, route
        assert 'id="nav-search"' in body, route


def test_quality_tile_counts_and_changes_tile_lists_the_page():
    (_wiki / "quality-requirements" / "QR-001-fast-checkout.md").write_text(QR, encoding="utf-8")
    try:
        body = _home()
        q = body[body.index("tile-quality"):body.index("tile-constraints")]
        assert '<span class="num">1</span>' in q, q
        ch = body[body.index("tile-changes"):]
        assert "QR-001" in ch and "Fast checkout" in ch, ch[:600]
        assert "ago" in ch
    finally:
        (_wiki / "quality-requirements" / "QR-001-fast-checkout.md").unlink()


def test_recent_changes_shape():
    (_wiki / "glossary" / "GLO-001-x.md").write_text(QR.replace("QR-001", "GLO-001").replace("quality-requirement", "glossary-term"), encoding="utf-8")
    try:
        app._PARSE_CACHE.clear()
        rows = app.recent_changes(5)
        assert rows and set(rows[0]) >= {"id", "title", "kind", "url", "when"}, rows
        assert rows[0]["url"] == "/page/glossary/GLO-001-x"
    finally:
        (_wiki / "glossary" / "GLO-001-x.md").unlink()


def test_vault_status_strip():
    body = _home()
    assert 'class="vault-status"' in body
    assert "open issue" in body           # "0 open issues" on the empty vault
```

- [ ] **Step 2: Run, confirm failure** (`tile-scope` missing).

- [ ] **Step 3: `Page.mtime`, sources, recent changes, status**

`Page` dataclass: add `mtime: float = 0.0` as the last field; in `_parse` pass `mtime=mtime`. Next to `ADR_DIR`:
```python
# Provenance records (raw/sources/, Source type, ADR-0006). Read-only mount at
# /sources in Docker; repo fallback for local runs. Only ever read.
_env_src = os.environ.get("RAW_SOURCES_DIR")
SOURCES_DIR = Path(_env_src) if _env_src else Path(__file__).resolve().parents[3] / "raw" / "sources"


@_request_cached
def load_sources() -> list[Page]:
    if not SOURCES_DIR.is_dir():
        return []
    pages = [_parse(p, "sources") for p in sorted(SOURCES_DIR.glob("*.md"))]
    return [p for p in pages if p is not None]
```
After `load_all_pages`:
```python
def _relative_when(ts: float, now: float | None = None) -> str:
    """'just now' / '12 min ago' / '3 h ago' / '2026-09-06' — coarse on purpose."""
    now = time.time() if now is None else now
    d = max(0, int(now - ts))
    if d < 60: return "just now"
    if d < 3600: return f"{d // 60} min ago"
    if d < 86400: return f"{d // 3600} h ago"
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def recent_changes(n: int = 5) -> list[dict]:
    """The n most recently modified wiki pages (file mtime — the cheapest
    'what changed' there is; the vault is regenerated a few times per
    workshop, nobody watches it live)."""
    pages = sorted(load_all_pages(), key=lambda p: -p.mtime)[:n]
    return [{"id": p.id, "title": p.title, "kind": FOLDER_LABELS.get(p.folder, p.folder),
             "url": _page_url(p.folder, p.stem), "when": _relative_when(p.mtime)} for p in pages]


def vault_status() -> dict:
    pages = load_all_pages()
    issues = load_folder("issues")
    last = max((p.mtime for p in pages), default=0.0)
    return {"pages": len(pages),
            "open_issues": sum(1 for i in issues if i.status not in CLOSED_STATUSES),
            "sources": len(load_sources()),
            "last_change": _relative_when(last) if last else "—"}
```
`Dockerfile`: add `RAW_SOURCES_DIR=/sources` to the ENV block. `compose.yaml` volumes: `- "${SOURCES_DIR:-../../../raw/sources}:/sources:ro"`. `dashboard.sh`: `export SOURCES_DIR="$ROOT/raw/sources"` next to `ADR_DIR`, and in `local)` add `SOURCES_DIR` to the `export` line plus `export RAW_SOURCES_DIR="$SOURCES_DIR"`.

- [ ] **Step 4: Rebuild `index()`**

Replace the `tiles = [...]` list. Keep `by_relations`, `backlog`, `vision_tile`; drop `req42_rows/req42_total/req42_in_scope` and `search_slim` (and the `<script id="search-index">` + preview JS in `index.html`). `build_vision_tile` gets `"eyebrow": "01 · Business Goals", "folders": ["goals"]` in both return dicts and `"span": 2`. New helper inside `index()`:
```python
def plain(key, label, eyebrow, href, folders, unit, rows=None, links=None, sub=""):
    pages = [p for f in folders for p in load_folder(f)]
    return {"key": key, "label": label, "eyebrow": eyebrow, "href": href, "folders": folders,
            "count": len(pages), "unit": unit, "sub": sub, "active": True,
            "rows": rows if rows is not None else by_relations(pages), "links": links or []}
```
Tiles, in this order:
```python
context = load_folder("context"); eifs = load_folder("external-interfaces")
tiles = [
    vision_tile,
    plain("stakeholders", "Stakeholders", "02 · Stakeholders", "/stakeholders", ["stakeholders"], "personas"),
    plain("scope", "Scope", "03 · Scope", "/req42/scope", ["context", "external-interfaces"],
          "external interfaces", rows=by_relations(eifs),
          sub=("context described" if context else "no context page yet")),
    {**backlog_tile, "eyebrow": "04 · Product Backlog", "folders": ["functional-requirements"]},
    plain("models", "Supporting models", "05 · Supporting Models", "/req42/models",
          ["use-cases", "activity-models", "data-models"], "model pages",
          rows=[{"title": m["title"], "relations": m["relations"]} for m in _supporting_model_entries()]),
    plain("quality", "Quality requirements", "06 · Quality Requirements", "/req42/quality",
          ["quality-requirements"], "scenarios"),
    plain("constraints", "Constraints", "07 · Constraints", "/req42/constraints", ["constraints"], "constraints"),
    plain("glossary", "Glossary", "08 · Domain Terminology", None, ["glossary"], "terms",
          links=[{"label": "Table", "href": "/glossary"}, {"label": "Term network", "href": "/graph/glossary"}]),
    {"key": "issues", "label": "Issues", "eyebrow": "12 · Risks & Assumptions", "href": "/issues",
     "folders": ["issues"], "count": len(open_issues), "unit": "open", "active": True,
     "sub": f"{len(issues)} in total",
     "rows": [{"id": i.id, "title": i.title, "severity": str(i.meta.get("severity") or "")}
              for i in sorted(open_issues, key=lambda i: ({"blocker": 0, "major": 1, "minor": 2}.get(str(i.meta.get("severity") or ""), 3), i.id))][:5]},
    {"key": "adrs", "label": "Architecture decisions", "eyebrow": "ADR · method decisions", "href": "/adrs",
     "folders": [], "count": len(adrs), "unit": "decisions", "active": True,
     "rows": [{"id": a["id"], "title": a["title"], "status": a["status"]} for a in adrs]},
    {"key": "changes", "label": "Latest changes", "eyebrow": "Recently modified", "href": None,
     "folders": [], "active": True, "rows": recent_changes(5)},
]
return render_template("index.html", tiles=tiles, status=vault_status(),
                       needs_mermaid=False)
```
(The data-model mini diagram is a `None` placeholder today; drop `needs_mermaid` plumbing on the home page.)

- [ ] **Step 5: `index.html` tile bodies**

Rewrite the `{% set inner %}` block so every tile renders: `tile-head` (eyebrow + title), then a key-specific body, then rows, then CTA. Structure:
```html
<div class="tile-head">
  <span class="tile-eyebrow">{{ t.eyebrow }}</span>
  <h2 class="tile-title">{{ t.label }}</h2>
</div>
{% if t.key == 'vision' and t.active %}
  <p class="tile-vision-claim">{{ t.claim }}</p>
  {% if t.objective_rows %}<ul class="mini-list">{% for o in t.objective_rows %}<li><span class="ml-title"><code class="ml-id">{{ o.id }}</code> {{ o.title }}</span><span class="ml-count">{{ o.epics }} epic{{ '' if o.epics == 1 else 's' }}</span></li>{% endfor %}</ul>
  {% else %}<p class="empty-state empty-state-tight">No objectives yet — ask the agent: <em>“derive objectives from the vision”</em>.</p>{% endif %}
{% elif t.key == 'vision' %}{{ empty_bootstrap("vision") }}
{% elif t.key == 'changes' %}
  {% if t.rows %}<ul class="mini-list mini-list-changes">{% for r in t.rows %}<li><a class="ml-hit" href="{{ r.url }}"><code class="ml-id">{{ r.id }}</code><span class="ml-title">{{ r.title }}</span><span class="ml-when">{{ r.when }}</span></a></li>{% endfor %}</ul>
  {% else %}{{ empty_state("pages") }}{% endif %}
{% else %}
  <div class="tile-count"><span class="num">{{ t.count }}</span><span class="unit">{{ t.unit }}{% if t.sub %} · {{ t.sub }}{% endif %}</span></div>
  {% if t.key == 'backlog' and t.epic_rows %}<ul class="mini-list">{% for e in t.epic_rows %}<li><span class="ml-title"><code class="ml-id">{{ e.id }}</code> {{ e.title }}</span><span class="ml-count{% if e.n_features == 0 and e.n_stories == 0 %} ml-out{% endif %}">{{ e.n_stories }} {{ 'story' if e.n_stories == 1 else 'stories' }} · {{ e.n_features }} feature{{ '' if e.n_features == 1 else 's' }}</span></li>{% endfor %}</ul>
  {% elif t.rows %}<ul class="mini-list">{% for r in t.rows %}<li><span class="ml-title">{% if r.id %}<code class="ml-id">{{ r.id }}</code> {% endif %}{{ r.title }}</span>{% if r.severity is defined %}<span class="ml-count">{{ r.severity }}</span>{% elif r.relations is defined %}<span class="ml-count">{{ r.relations }} link{{ '' if r.relations == 1 else 's' }}</span>{% endif %}</li>{% endfor %}</ul>
  {% elif t.count == 0 %}{% if t.key == 'adrs' %}{{ empty_adrs() }}{% else %}{{ empty_state(t.unit) }}{% endif %}{% endif %}
{% endif %}
{% if t.links %}<div class="tile-ctas">…</div>{% elif t.href %}<span class="tile-cta">View details →</span>{% endif %}
```
Wrapper: `<a class="tile tile-link tile-{{ t.key }}{% if t.span == 2 %} tile-span-2{% endif %}" href="{{ t.href }}">` when `t.href` and no `t.links`; `<div class="tile tile-{{ t.key }} …">` otherwise (glossary has links, changes has row links). Add the status strip under the hero:
```html
<p class="vault-status">
  <span><strong>{{ status.pages }}</strong> pages</span>
  <span><strong>{{ status.open_issues }}</strong> open issue{{ '' if status.open_issues == 1 else 's' }}</span>
  <span><strong>{{ status.sources }}</strong> source{{ '' if status.sources == 1 else 's' }} ingested</span>
  <span>last change <strong>{{ status.last_change }}</strong></span>
</p>
```
CSS: `.vault-status { display:flex; flex-wrap:wrap; gap: var(--space-2) var(--space-5); margin: 0 0 var(--space-5); color: var(--ink-soft); font-size: var(--step--1); } .vault-status strong { color: var(--ink); font-weight: 600; font-variant-numeric: tabular-nums; } .ml-when { color: var(--ink-dim); font-size: .78rem; white-space: nowrap; margin-left: auto; } .ml-hit { display:flex; align-items: baseline; gap: .4rem; width: 100%; text-decoration: none; color: var(--ink); }`.

- [ ] **Step 6: Navigation in `base.html`**

Replace the conditional `<header class="topbar">` with an unconditional one:
```html
<header class="topbar">
  <a class="brand" href="/"><img class="brand-mark" src="{{ url_for('static', filename='etsu-favicon.png') }}" alt=""> {{ system_name }}</a>
  <nav class="mainnav" aria-label="Main">
    {% for href, label in [('/goals','Goals'), ('/stakeholders','Stakeholders'), ('/req42/scope','Scope'), ('/req42/backlog','Backlog'), ('/req42/quality','Quality'), ('/glossary','Glossary'), ('/issues','Issues'), ('/adrs','ADRs'), ('/req42','req42')] %}
    <a href="{{ href }}"{% if request.path == href or (href != '/req42' and request.path.startswith(href)) %} aria-current="page"{% endif %}>{{ label }}</a>
    {% endfor %}
  </nav>
  <form class="nav-search" action="/search" method="get" role="search">
    <input type="search" name="q" id="nav-search" class="search-input" placeholder="Search  /" autocomplete="off" aria-label="Search the wiki">
  </form>
  <span class="my-nickname" id="my-nickname" hidden>
    <span id="my-nickname-label">You are</span> <strong id="my-nickname-text"></strong>
  </span>
</header>
<main class="wrap">
  {% set crumbs_html %}{% block crumbs %}{% endblock %}{% endset %}
  {% if crumbs_html|trim %}<div class="crumbs-row">{{ crumbs_html }}</div>{% endif %}
  {% block content %}{% endblock %}
</main>
```
Note: this is the same capture-the-block pattern base.html uses today (`topbar_nav`), only moved into `<main>`; `index.html` defines no crumbs block, so the row disappears on home. Keyboard: in the lifecycle script add
```js
document.addEventListener("keydown", function (e) {
  var tag = (e.target.tagName || "").toLowerCase();
  if (e.key === "/" && tag !== "input" && tag !== "textarea" && !e.metaKey && !e.ctrlKey) {
    var s = document.getElementById("nav-search"); if (s) { e.preventDefault(); s.focus(); }
  }
});
```
CSS: `.topbar { display:flex; align-items:center; gap: var(--space-4); padding: .55rem var(--space-5); border-bottom: 1px solid var(--line); background: var(--topbar-bg); backdrop-filter: blur(8px); position: sticky; top: 0; z-index: 10; } .brand { display:inline-flex; align-items:center; gap:.5rem; font-weight: 700; color: var(--ink); text-decoration:none; white-space: nowrap; } .brand-mark { width: 1.35rem; height: 1.35rem; border-radius: 4px; } .mainnav { display:flex; gap: .15rem; overflow-x: auto; scrollbar-width: none; } .mainnav a { padding: .35rem .6rem; border-radius: 6px; color: var(--ink-soft); text-decoration: none; font-size: var(--step--1); white-space: nowrap; } .mainnav a:hover { color: var(--ink); background: var(--chip-bg); } .mainnav a[aria-current="page"] { color: var(--ink); background: var(--chip-bg); font-weight: 600; } .nav-search { margin-left: auto; } .nav-search .search-input { width: 13rem; min-width: 0; padding: .35rem .8rem; font-size: var(--step--1); } .crumbs-row { margin: 0 0 var(--space-3); } @media (max-width: 780px) { .topbar { flex-wrap: wrap; } .nav-search { margin-left: 0; flex: 1 1 100%; } .nav-search .search-input { width: 100%; } }`. The table `thead { top: 57px }` sticky offset must match the new topbar height — measure in the screenshot and adjust.

Hero: keep logo + title + tagline; remove `hero-nickname` from `index.html` (the topbar shows it now on every page; delete the `{% block header_nickname %}{% endblock %}` override in `index.html`).

- [ ] **Step 7: README + run + commit**

Update the README "Tiles" table to the eleven tiles and add a "Navigation" paragraph (nav bar, `/` shortcut, search page). Run the suite (fix `test_empty_vault.py`'s vision-tile slice if the 900-char window no longer contains the empty state: widen to 1400). Screenshot as in Task 3, check the four rows, the nav, and the status strip. Commit:
```bash
git add -A _system/apps/dashboard dashboard.sh
git commit -m "dashboard: home page in req42 reading order, persistent nav, latest changes"
```

---

### Task 5: Maturity bars

**Files:**
- Modify: `app.py` (new `maturity()`, wire into tiles and list routes), `templates/_maturity.html` (new macro), `templates/index.html`, `templates/glossary.html`, `templates/stakeholders.html`, `templates/issues.html`, `templates/adrs.html`, `templates/req42_block.html`, `static/style.css`
- Test: `tests/test_maturity.py` (new)

**Interfaces:**
- Produces: `app.maturity(statuses: Iterable[str]) -> dict(total, segments=[{status, n, pct}], label)`; macro `maturity_bar(m, compact=False)`; every tile dict gains `"maturity"`; list routes pass `maturity=` to their template.

- [ ] **Step 1: Failing test** `tests/test_maturity.py` (module setup like `tests/test_copy.py`):
```python
GLO = """---
id: {id}
type: glossary-term
title: {title}
status: {status}
created: 2026-09-07
updated: 2026-09-07
sources: []
related: []
tags: [glossary]
---

# {title}

**Definition.** Something.
"""


def test_maturity_buckets_and_aliases():
    m = app.maturity(["draft", "accepted", "proposed", "superseded", "resolved", "weird", ""])
    by = {s["status"]: s["n"] for s in m["segments"]}
    assert by == {"accepted": 2, "review": 1, "draft": 3, "deprecated": 1}, by
    assert m["total"] == 7
    assert sum(s["pct"] for s in m["segments"]) in (99, 100, 101)
    assert [s["status"] for s in m["segments"]] == ["accepted", "review", "draft", "deprecated"]
    assert app.maturity([]) == {"total": 0, "segments": [], "label": "nothing yet"}


def test_bar_renders_on_home_tile_and_list_page():
    for i, st in ((1, "draft"), (2, "accepted")):
        (_wiki / "glossary" / f"GLO-00{i}-t{i}.md").write_text(GLO.format(id=f"GLO-00{i}", title=f"T{i}", status=st), encoding="utf-8")
    try:
        app._PARSE_CACHE.clear()
        c = app.app.test_client()
        home = c.get("/").get_data(as_text=True)
        tile = home[home.index("tile-glossary"):home.index("tile-issues")]
        assert 'maturity-seg maturity-accepted" style="flex-basis: 50%"' in tile, tile
        assert "maturity-draft" in tile
        page = c.get("/glossary").get_data(as_text=True)
        assert 'class="maturity' in page
    finally:
        for i in (1, 2):
            (_wiki / "glossary" / f"GLO-00{i}-t{i}.md").unlink()
```

- [ ] **Step 2: Run, confirm failure** (`app.maturity` missing).

- [ ] **Step 3: Implement** in `app.py` after `CLOSED_STATUSES`:
```python
# The four-step lifecycle every content type shares (CLAUDE.md: draft → review →
# accepted → deprecated). ADR and issue statuses are mapped onto it so one thin
# bar reads the same on every tile.
MATURITY_ORDER = ["accepted", "review", "draft", "deprecated"]
_MATURITY_ALIASES = {
    "proposed": "review", "in-progress": "review",
    "resolved": "accepted", "ingested": "accepted",
    "open": "draft",
    "superseded": "deprecated", "rejected": "deprecated", "wontfix": "deprecated",
}


def maturity(statuses) -> dict:
    """Bucket status strings into MATURITY_ORDER and return the segments of a
    stacked bar (percent widths) plus a text label for the tooltip/aria."""
    counts = {k: 0 for k in MATURITY_ORDER}
    for s in statuses:
        s = _MATURITY_ALIASES.get(str(s or "").strip().lower(), str(s or "").strip().lower())
        counts[s if s in counts else "draft"] += 1
    total = sum(counts.values())
    segments = [{"status": k, "n": counts[k], "pct": round(100 * counts[k] / total)}
                for k in MATURITY_ORDER if counts[k]]
    label = " · ".join(f'{s["n"]} {s["status"]}' for s in segments) or "nothing yet"
    return {"total": total, "segments": segments, "label": label}
```
Wire: in `index()` after building `tiles`, `for t in tiles: t["maturity"] = maturity(...)` — for tiles with `folders`: statuses of `load_folder(f)` pages; `adrs`: `[a["status"] for a in adrs]`; `changes`: skip. Routes `/glossary`, `/stakeholders`, `/issues`, `/adrs`, `/req42/<slug>` pass `maturity=maturity([p.status for p in <their pages>])`.

`templates/_maturity.html`:
```html
{% macro maturity_bar(m, compact=False) %}
{% if m and m.total %}
<div class="maturity{% if compact %} maturity-compact{% endif %}" role="img" aria-label="Maturity: {{ m.label }}" title="{{ m.label }}">
  {% for s in m.segments %}<span class="maturity-seg maturity-{{ s.status }}" style="flex-basis: {{ s.pct }}%"></span>{% endfor %}
</div>
{% endif %}
{% endmacro %}
{% macro maturity_legend() %}
<p class="maturity-legend" aria-hidden="true">
  <span class="maturity-key maturity-accepted"></span>accepted
  <span class="maturity-key maturity-review"></span>in review
  <span class="maturity-key maturity-draft"></span>draft
  <span class="maturity-key maturity-deprecated"></span>deprecated
</p>
{% endmacro %}
```
Place `{{ maturity_bar(t.maturity) }}` directly under `.tile-count` in `index.html`; `{{ maturity_legend() }}` at the end of the `vault-status` strip; on each list page directly under the `<h1 class="page-h1">`. CSS (tokens only):
```css
.maturity { display: flex; gap: 2px; height: 4px; margin: .45rem 0 var(--space-3); }
.maturity-seg { display: block; flex: 0 0 auto; border-radius: 2px; min-width: 3px; }
.maturity-accepted { background: var(--accent-2); }
.maturity-review { background: var(--accent); }
.maturity-draft { background: var(--ink-dim); }
.maturity-deprecated { background: var(--line); }
.maturity-legend { display: flex; flex-wrap: wrap; gap: .3rem 1rem; font-size: .76rem; color: var(--ink-dim); margin: 0; }
.maturity-key { display: inline-block; width: .9rem; height: 4px; border-radius: 2px; margin-right: .35rem; vertical-align: middle; }
.page-h1 + .maturity { max-width: 22rem; margin-top: .2rem; }
```

- [ ] **Step 4: Run suite, screenshot, commit** `"dashboard: maturity bars on tiles and list pages"`.

---

### Task 6: Open-issue flags on tiles

**Files:**
- Modify: `app.py` (`open_issue_counts()`, wire into `index()`), `templates/index.html`, `templates/issues.html` (`?filter=` preselect), `static/style.css`
- Test: `tests/test_issue_flags.py` (new)

**Interfaces:**
- Produces: `app.open_issue_counts() -> dict[str, int]` (folder → open issues pointing at it); tile dict key `"open_issues": int`.

- [ ] **Step 1: Failing test** (module setup like `tests/test_copy.py`). Fixture pages: `GLO-001-tour.md` (glossary term, status accepted), `ISS-001-open.md` with `status: open`, `severity: major`, `related: ["[[GLO-001-tour]]"]`, `ISS-002-done.md` with `status: resolved` and the same `related`. Body lines only need the `# Title` heading.
```python
def test_open_issue_counts_by_folder():
    app._PARSE_CACHE.clear()
    assert app.open_issue_counts() == {"glossary": 1}


def test_tile_flag_and_plural():
    body = app.app.test_client().get("/").get_data(as_text=True)
    g = body[body.index("tile-glossary"):body.index("tile-issues")]
    assert 'class="tile-flag"' in g and "1 open issue<" in g, g
    s = body[body.index("tile-stakeholders"):body.index("tile-scope")]
    assert "tile-flag" not in s


def test_issues_page_preselects_open_filter():
    body = app.app.test_client().get("/issues?filter=open").get_data(as_text=True)
    assert "URLSearchParams" in body
```

- [ ] **Step 2: Run, confirm failure.**

- [ ] **Step 3: Implement**
```python
def open_issue_counts() -> dict[str, int]:
    """folder -> number of OPEN issues whose links (frontmatter `related:` or
    body wikilinks) resolve to a page in that folder. One issue can count for
    several folders; an issue that links nothing resolvable counts nowhere."""
    links = link_index()
    out: dict[str, int] = {}
    for iss in load_folder("issues"):
        if iss.status in CLOSED_STATUSES:
            continue
        for folder in {links[t][0] for t in iss.link_targets() if t in links}:
            out[folder] = out.get(folder, 0) + 1
    return out
```
In `index()`: `flags = open_issue_counts()` and for every tile except `issues`/`changes`: `t["open_issues"] = sum(flags.get(f, 0) for f in t.get("folders", []))`. In `index.html`, inside `tile-head` after the title:
```html
{% if t.open_issues %}<span class="tile-flag" title="Open issues that point at pages of this type">{{ t.open_issues }} open issue{{ '' if t.open_issues == 1 else 's' }}</span>{% endif %}
```
CSS: `.tile-head { position: relative; } .tile-flag { position: absolute; top: 0; right: 0; font: 600 .72rem/1.6 var(--font-mono); color: var(--warn); border: 1px solid rgba(255,180,84,.4); background: rgba(255,180,84,.1); border-radius: 999px; padding: 0 .55rem; white-space: nowrap; }`.
`issues.html` JS, after the button wiring: `const want = new URLSearchParams(location.search).get('filter'); const pre = want && document.querySelector('.fbtn[data-filter="' + want + '"]'); if (pre) pre.click();`.

- [ ] **Step 4: Run suite, commit** `"dashboard: open-issue flags on home tiles"`.

---

### Task 7: QR "scan to join" and the /join page

**Files:**
- Modify: `requirements.txt` (`segno==1.6.6`), `app.py` (`_lan_ip`, `public_url`, `qr_svg`, `/join`, `index()`), `templates/index.html` (hero), `templates/join.html` (new), `templates/who.html` (link to /join), `static/style.css`, `dashboard.sh`, `compose.yaml`, `README.md`, `tests/test_empty_vault.py` (add `/join`)
- Test: `tests/test_join.py` (new)

**Interfaces:**
- Produces: `app.public_url() -> str` (request context required), `app.qr_svg(url: str, scale: int = 4) -> str` (inline `<svg>`), route `GET /join`. Env `DASH_PUBLIC_URL` (wins when set).

- [ ] **Step 1: Failing test** `tests/test_join.py` — module setup like `tests/test_copy.py` **plus** `os.environ["DASH_PUBLIC_URL"] = "http://192.0.2.7:8080/"` before `import app`:
```python
def test_public_url_prefers_env_and_strips_slash():
    with app.app.test_request_context("/"):
        assert app.public_url() == "http://192.0.2.7:8080"


def test_qr_svg_is_inline_and_theme_aware():
    svg = app.qr_svg("http://192.0.2.7:8080")
    assert svg.startswith("<svg") and "currentColor" in svg


def test_home_and_join_show_the_code():
    c = app.app.test_client()
    home = c.get("/").get_data(as_text=True)
    assert 'class="hero-join"' in home and "<svg" in home and "192.0.2.7:8080" in home
    join = c.get("/join").get_data(as_text=True)
    assert join.count("<svg") == 1 and "192.0.2.7:8080" in join and "Who" in join
```
Also append `"/join"` to `GET_ROUTES` in `tests/test_empty_vault.py`.

- [ ] **Step 2: Run, confirm failure**; `pip install segno==1.6.6` into `.venv` and add the pin to `requirements.txt`.

- [ ] **Step 3: Implement** (imports: `socket`, and `segno` lazily inside `qr_svg`):
```python
def _lan_ip() -> str | None:
    """This host's LAN address, best effort. Connecting a UDP socket sends no
    packet; it only makes the OS pick the outbound interface."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("10.255.255.255", 1))
            return s.getsockname()[0]
        finally:
            s.close()
    except OSError:
        return None


def public_url() -> str:
    """The address other devices in the room should open. DASH_PUBLIC_URL wins
    (dashboard.sh sets it from the host's LAN address — inside Docker the
    container only knows its own bridge address); else the request's port on
    this host's LAN IP; else the request's own origin."""
    env = os.environ.get("DASH_PUBLIC_URL", "").strip()
    if env:
        return env.rstrip("/")
    host, _, port = request.host.partition(":")
    ip = _lan_ip()
    if ip:
        return f"http://{ip}:{port}" if port else f"http://{ip}"
    return request.host_url.rstrip("/")


def qr_svg(url: str, scale: int = 4) -> str:
    """Inline SVG QR code. `dark="currentColor"` lets CSS `color` set the
    module colour, so it follows the theme; no background rectangle."""
    import segno
    return segno.make(url, error="m").svg_inline(scale=scale, border=1, dark="currentColor", light=None, omitsize=True)


@app.route("/join")
def join_page():
    url = public_url()
    return render_template("join.html", join_url=url, join_qr=qr_svg(url, scale=10))
```
`index()` passes `join_url=public_url(), join_qr=qr_svg(public_url())`. Hero in `index.html` (inside `.hero-row`, after `.hero-text`):
```html
<a class="hero-join" href="/join" title="Show a big code to project">
  <span class="hero-qr" aria-hidden="true">{{ join_qr | safe }}</span>
  <span class="hero-join-text"><strong>Scan to open on your device</strong><code>{{ join_url }}</code></span>
</a>
```
`templates/join.html`:
```html
{% extends "base.html" %}
{% block title %}Join{% endblock %}
{% block crumbs %}<nav class="crumbs"><a href="/">Overview</a> <span>/</span> Join</nav>{% endblock %}
{% block content %}
<section class="join">
  <div class="join-qr" aria-label="QR code for {{ join_url }}">{{ join_qr | safe }}</div>
  <div class="join-text">
    <h1 class="page-h1">Open this on your own device</h1>
    <p class="lead">Point your camera at the code, or type the address. You get your own nickname and appear on <a href="/who">Who's here</a>.</p>
    <p class="join-url"><code>{{ join_url }}</code></p>
  </div>
</section>
{% endblock %}
```
CSS: `.hero-join { margin-left: auto; display: flex; align-items: center; gap: var(--space-3); text-decoration: none; color: var(--ink); } .hero-qr { display: block; width: 5.2rem; height: 5.2rem; padding: .3rem; background: var(--plate); color: var(--on-plate); border-radius: 6px; } .hero-qr svg { width: 100%; height: 100%; display: block; } .hero-join-text { display: flex; flex-direction: column; gap: .15rem; font-size: var(--step--1); } .hero-join-text code { color: var(--ink-soft); } .join { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: var(--space-6); align-items: center; padding: var(--space-5) 0; } .join-qr { padding: var(--space-3); background: var(--plate); color: var(--on-plate); border-radius: var(--radius); } .join-qr svg { width: 100%; height: auto; display: block; } .join-url code { font-size: var(--step-2); } @media (max-width: 780px) { .join { grid-template-columns: 1fr; } .hero-join { margin-left: 0; } }`. Add token `--on-plate: #0e1726;` to the dark palette and `--on-plate: #0e1726;` to the light palette (the plate is white in both themes, so the code stays navy-on-white and scannable).
`who.html`: add under the lead: `<p><a class="whos-here" href="/join">Show the join code →</a></p>`.
`dashboard.sh`, after the `TZ` block:
```bash
# Address the QR code points at: the host's LAN IP, not localhost. Override with
# DASH_PUBLIC_URL=http://name.local:8080 when the room has DNS or a tunnel.
lan_ip() {
  if command -v ipconfig >/dev/null 2>&1; then
    ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || true
  elif command -v hostname >/dev/null 2>&1; then
    hostname -I 2>/dev/null | awk '{print $1}'
  fi
}
LAN_IP="$(lan_ip)"
```
and in `up`/`rebuild`: `export DASH_PUBLIC_URL="${DASH_PUBLIC_URL:-http://${LAN_IP:-localhost}:8080}"` before `docker compose … up`, then `echo "✓ Others in the room: $DASH_PUBLIC_URL (QR on the home page, /join to project it)"`; in `local`: the same with port 8000. `compose.yaml` environment: `DASH_PUBLIC_URL: "${DASH_PUBLIC_URL:-}"`. README: a "Join code" paragraph.

- [ ] **Step 4: Run suite, screenshot `/` and `/join`, commit** `"dashboard: QR join code in the hero and a /join page for projection"`.

---

### Task 8: Provenance chips and the /source view

**Files:**
- Modify: `app.py` (`source_index`, `provenance`, `/source/<stem>`), `templates/_provenance.html` (new), `templates/detail.html`, `templates/fr.html`, `static/style.css`, `tests/test_empty_vault.py` (404 route), `README.md`
- Test: `tests/test_provenance.py` (new)

**Interfaces:**
- Consumes: `load_sources()`, `SOURCES_DIR`, `Page` from Task 4.
- Produces: `app.provenance(page: Page) -> list[dict(id, title, stem, type, origin, captured, url|None)]`; route `GET /source/<stem>`; macro `provenance_chips(sources)`.

- [ ] **Step 1: Failing test** — module setup like `tests/test_copy.py` plus `_src = _tmp / "sources"; _src.mkdir(); os.environ["RAW_SOURCES_DIR"] = str(_src)` **before** `import app`. Fixtures written at module level:
```python
(_src / "SRC-001-brief.md").write_text("""---
id: SRC-001
type: source
title: Project brief
status: ingested
created: 2026-09-06
updated: 2026-09-06
tags: [source]
source-type: document
origin: raw/ingested/brief.md
captured: 2026-09-06
sha256: n/a
ingested-pages: ["[[GLO-001-tour]]"]
---

# Project brief

The one-page brief the sponsor sent.
""", encoding="utf-8")
(_wiki / "glossary" / "GLO-001-tour.md").write_text("""---
id: GLO-001
type: glossary-term
title: Tour
status: draft
created: 2026-09-06
updated: 2026-09-06
sources: ["[[raw/sources/SRC-001-brief]]"]
related: []
tags: [glossary]
---

# Tour

**Definition.** A travelling exhibition.
""", encoding="utf-8")
(_wiki / "glossary" / "GLO-002-show.md").write_text("""---
id: GLO-002
type: glossary-term
title: Show
status: draft
created: 2026-09-06
updated: 2026-09-06
sources: []
related: []
tags: [glossary]
---

# Show

**Definition.** One stop of a tour.
""", encoding="utf-8")


def test_provenance_resolves_source_records():
    app._PARSE_CACHE.clear()
    page = app._parse(_wiki / "glossary" / "GLO-001-tour.md", "glossary")
    rows = app.provenance(page)
    assert rows == [{"id": "SRC-001", "title": "Project brief", "stem": "SRC-001-brief", "type": "document",
                     "origin": "raw/ingested/brief.md", "captured": "2026-09-06", "url": "/source/SRC-001-brief"}], rows


def test_chips_on_detail_pages():
    c = app.app.test_client()
    sourced = c.get("/page/glossary/GLO-001-tour").get_data(as_text=True)
    assert 'class="chip chip-src"' in sourced and "SRC-001" in sourced
    unsourced = c.get("/page/glossary/GLO-002-show").get_data(as_text=True)
    assert "chip-unsourced" in unsourced


def test_source_page_renders_and_links_back():
    body = app.app.test_client().get("/source/SRC-001-brief").get_data(as_text=True)
    assert "Project brief" in body and "raw/ingested/brief.md" in body
    assert "/page/glossary/GLO-001-tour" in body        # ingested-pages resolved
    assert app.app.test_client().get("/source/SRC-999-nope").status_code == 404
```

- [ ] **Step 2: Run, confirm failure.**

- [ ] **Step 3: Implement**
```python
@_request_cached
def source_index() -> dict[str, Page]:
    idx: dict[str, Page] = {}
    for p in load_sources():
        idx.setdefault(p.stem, p)
        idx.setdefault(p.id, p)
    return idx


def provenance(page: Page) -> list[dict]:
    """Resolve a page's `sources:` wikilinks to provenance records. Unresolved
    entries are kept (url=None) so the chip can say so instead of vanishing."""
    idx = source_index()
    rows = []
    for ref in page.meta.get("sources") or []:
        base = _fr_stem_from_ref(ref)           # '[[raw/sources/SRC-001-x]]' -> 'SRC-001-x'
        src = idx.get(base)
        if src:
            rows.append({"id": src.id, "title": src.title, "stem": src.stem,
                         "type": str(src.meta.get("source-type") or ""),
                         "origin": str(src.meta.get("origin") or ""),
                         "captured": str(src.meta.get("captured") or ""),
                         "url": f"/source/{src.stem}"})
        else:
            rows.append({"id": base, "title": base, "stem": base, "type": "", "origin": "", "captured": "", "url": None})
    return rows


@app.route("/source/<stem>")
def source_detail(stem):
    src = source_index().get(stem)
    if not src:
        abort(404)
    titles = title_index()
    body = re.sub(r"^\s*#\s+.*(?:\n|$)", "", src.body, count=1)
    facts = [("Type", str(src.meta.get("source-type") or "—")),
             ("Origin", str(src.meta.get("origin") or "—")),
             ("Captured", str(src.meta.get("captured") or "—")),
             ("Checksum", str(src.meta.get("sha256") or "—")[:16])]
    facts_html = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in facts)
    ingested = ", ".join(render_wikilinks(str(r), titles, link_index()) for r in (src.meta.get("ingested-pages") or [])) or "—"
    body_html = f'<dl class="source-facts">{facts_html}<dt>Ingested pages</dt><dd>{ingested}</dd></dl>' + render_markdown(body, titles)
    return render_template("detail.html", kind="Source", id=src.id, title=src.title, status=src.status,
                           created=str(src.meta.get("created", "")), updated=str(src.meta.get("updated", "")),
                           tags=src.meta.get("tags") or [], body_html=body_html, crumb="Sources", crumb_href="/",
                           context_diagram=None, relations=None, ego_graph=None, ego_layers=None,
                           needs_mermaid=False, sources=None)
```
`page_detail` (wiki branch) passes `sources=provenance(page)`; the ADR branch passes `sources=None`; `fr_detail` (the `/functional-requirements/<stem>` route) passes `sources=provenance(<the FR page>)`. Macro `templates/_provenance.html`:
```html
{% macro provenance_chips(sources) %}
<div class="provenance" aria-label="Provenance">
  <span class="provenance-label">Sources</span>
  {% if sources %}{% for s in sources %}
    {% if s.url %}<a class="chip chip-src" href="{{ s.url }}" title="{{ s.type }}{% if s.origin %} · {{ s.origin }}{% endif %}"><code>{{ s.id }}</code> {{ s.title }}</a>
    {% else %}<span class="chip chip-src chip-unresolved" title="No matching record in raw/sources/"><code>{{ s.id }}</code></span>{% endif %}
  {% endfor %}
  {% else %}<span class="chip chip-unsourced" title="No source recorded — treat as an assumption">unsourced</span>{% endif %}
</div>
{% endmacro %}
```
In `detail.html` and `fr.html`, import it and render `{% if sources is not none %}{{ provenance_chips(sources) }}{% endif %}` directly under `.detail-meta` / `.detail-head`. CSS: `.provenance { display:flex; flex-wrap:wrap; align-items:center; gap:.4rem; margin: -.6rem 0 var(--space-4); } .provenance-label { font: 600 .7rem/1.4 var(--font-mono); letter-spacing:.08em; text-transform:uppercase; color: var(--ink-dim); margin-right:.2rem; } .chip { display:inline-flex; align-items:center; gap:.35rem; font-size:.78rem; padding:.1rem .6rem; border-radius:999px; border:1px solid var(--line); color: var(--ink-soft); text-decoration:none; } .chip code { font-size:.9em; } .chip-src:hover { border-color: var(--accent); color: var(--ink); } .chip-unresolved { border-style: dashed; } .chip-unsourced { color: var(--warn); border-color: rgba(255,180,84,.4); background: rgba(255,180,84,.1); } .source-facts { display:grid; grid-template-columns: max-content 1fr; gap:.3rem 1rem; margin: 1rem 0; } .source-facts dt { color: var(--ink-dim); font: 600 .7rem/1.8 var(--font-mono); letter-spacing:.08em; text-transform:uppercase; } .source-facts dd { margin:0; }`. Add `"/source/SRC-001-nothing"` to `NOT_FOUND_ROUTES` in `tests/test_empty_vault.py`. README: a "Provenance" paragraph (chips, `/source/`, the `raw/sources` mount).

- [ ] **Step 4: Run suite, commit** `"dashboard: provenance chips linking every page to its raw/sources record"`.

---

### Task 9: Words instead of glyphs, README, ADR-0025

**Files:**
- Modify: `templates/index.html`, `templates/backlog.html`, `templates/fr.html`, `templates/req42_block.html`, `templates/glossary.html`, `templates/stakeholders.html`, `static/style.css`, `README.md`
- Create: `_system/adr/0025-dashboard-req42-home-and-visual-identity.md`
- Modify: `_system/index.md` (one ADR line)
- Test: `tests/test_copy.py` (two more tests)

- [ ] **Step 1: Failing tests** in `tests/test_copy.py`:
```python
def test_no_bare_glyph_abbreviations():
    tpl = HERE / "templates"
    for p in tpl.glob("*.html"):
        txt = p.read_text(encoding="utf-8")
        assert "⤳" not in txt, p.name
        assert not re.search(r"\}\}S\b|\}\}F\b|n_stories \}\}S", txt), f"S/F abbreviation in {p.name}"


def test_adr_0025_is_indexed():
    adr = HERE.parents[2] / "adr" / "0025-dashboard-req42-home-and-visual-identity.md"
    assert adr.is_file()
    assert "0025-dashboard-req42-home-and-visual-identity" in (HERE.parents[2] / "index.md").read_text(encoding="utf-8")
```

- [ ] **Step 2: Run, confirm failure.**

- [ ] **Step 3: Replace abbreviations.** Create `templates/_macros.html`:
```html
{% macro plural(n, word, words=None) %}{{ n }} {{ word if n == 1 else (words or word ~ 's') }}{% endmacro %}
```
Import in the touched templates (`{% from "_macros.html" import plural %}`) and use: backlog rows `{{ plural(e.n_stories, 'story', 'stories') }} · {{ plural(e.n_features, 'feature') }}` (index.html, backlog.html); `fr.html` `.backlog-counter` the same; `req42_block.html` header `<th class="c-rel">Links</th>`; glossary/stakeholder tiles `{{ plural(r.relations, 'link') }}`; glossary/stakeholders tables keep the `rel-pill` number under the header "Links" (rename `RELATIONS` header). Delete `.ml-rel` CSS. Remove `title="S = Stories, F = Features (below)"` and similar tooltips that explained glyphs.

- [ ] **Step 4: ADR + index + README.** `_system/adr/0025-dashboard-req42-home-and-visual-identity.md` in the Nygard shape of ADR-0023 (`# ADR-0025: …`, `- **Status:** accepted`, `- **Date:** 2026-09-07`, Context / Decision / Consequences). Context: the critique (home page mirrored folders, generic look, no nav, glyph abbreviations, bugs). Decision: home tiles in req42 reading order with block numbers; persistent nav; flat identity with vendored OFL fonts (Bricolage Grotesque, JetBrains Mono) and no emoji; maturity bars; open-issue flags; QR join with `DASH_PUBLIC_URL`; provenance chips + `/source/`; "clients" wording; `nl2br` replaced by prose unwrapping. Consequences: ~250 KB more static assets; `segno` dependency; the `raw/sources` read-only mount; the search tile's inline preview was dropped in favour of the nav search. Add the index line after the ADR-0024 line in `_system/index.md`: `- [0025-dashboard-req42-home-and-visual-identity](adr/0025-dashboard-req42-home-and-visual-identity.md) — ADR-0025, the dashboard's home page follows req42's reading order with a persistent nav, a flat vendored-font identity, maturity bars, issue flags, a QR join code and provenance chips`. README: final pass so every section matches (run, tiles, navigation, join code, provenance, tests, layout listing new templates/files).

- [ ] **Step 5: Run suite, commit** `"dashboard: words instead of glyphs; ADR-0025; README"`.

---

### Task 10: Polish and verification

**Files:**
- Modify: `static/style.css`, any template with a leftover; `tests/test_design_tokens.py` (extend if useful)

- [ ] **Step 1: Dead CSS and leftovers.** `grep -o '\.[a-z][a-z0-9-]*' static/style.css | sort -u` versus `grep -ho 'class="[^"]*"' templates/*.html | tr ' "' '\n\n' | sort -u` — delete rules for classes no template or JS uses (`tile-search*`, `tile-logo`, `tile-subcount`, `ml-rel`, `hero-nickname`, `theme-toggle-icon`, `score-*` if search dropped it, etc.). Remove the `"icon"` keys, `search_slim`, and any unused helper in `app.py` (`python -W error -c "import app"` still imports).

- [ ] **Step 2: Rhythm.** Every margin/padding/gap in the tile, hero, status strip, nav and list-page header uses `--space-*` tokens; headings use `--step-*`. The sticky `thead` offset equals the rendered topbar height (measure in the screenshot; set `top` to that value in px).

- [ ] **Step 3: Light theme.** `test_every_token_exists_in_both_themes` passes. Additionally render `/` with the light palette forced for a screenshot: temporarily run `sed 's/<html lang="en">/<html lang="en" data-theme="light">/' templates/base.html > /tmp/base-light.html` — no: instead start the server and screenshot with a Chromium user-data-dir after setting the theme via URL is not possible; so review light by reading `style.css`: for every rule you added or changed, confirm both palettes define the tokens and no literal colour except `rgba()` washes crept in (`grep -n "#[0-9a-f]\{3,6\}" static/style.css` must only hit the two palette blocks and mermaid classDefs in app.py).

- [ ] **Step 4: Screenshots** (server + headless shell as in Task 3): `/` at 1400×1300 and 420×1700, `/join`, `/glossary`, `/page/stakeholders/<any>` on the fixture vault; and `/` on the real vault (`WIKI_DIR` unset). Save under the session scratchpad and look at each with the Read tool. Check: no horizontal scroll on the phone width, nav wraps, tiles stack, QR readable, fonts loaded (Bricolage `a`), maturity bars visible, flags aligned, footer plural.

- [ ] **Step 5: Full suite, commit** `"dashboard: polish pass"`. Then `git log --oneline main..HEAD` should list ten commits after the WIP commit.
