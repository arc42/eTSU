"""Requirements-Wiki Dashboard.

A small read-only Flask app that parses the Obsidian-style requirements wiki
(markdown + YAML frontmatter + [[wikilinks]]) live on each request and renders
it as a tiled dashboard. The wiki folder is mounted into the container; nothing
is ever written back.
"""
from __future__ import annotations

import functools
import mimetypes
import os
import re
import signal
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import markdown as md
import yaml
from flask import Flask, abort, g, has_request_context, redirect, render_template

# some slim base images lack a webp entry in their mime.types
mimetypes.add_type("image/webp", ".webp")

app = Flask(__name__)

# Timezone for the "last refreshed" footer; honours the container's TZ env.
DISPLAY_TZ = os.environ.get("TZ", "Europe/Berlin")


@app.context_processor
def inject_refresh_time():
    """Every render carries the moment its data was (re)parsed — pages parse the
    wiki live, so this is effectively the page load / data refresh time."""
    try:
        tz = ZoneInfo(DISPLAY_TZ)
    except (ZoneInfoNotFoundError, ValueError):
        tz = None
    return {"refreshed_at": datetime.now(tz).strftime("%d.%m.%Y, %H:%M:%S %Z").strip()}

# Root of the wiki layer. In Docker this is a read-only bind mount at /wiki;
# for local runs it falls back to the repo's wiki/ folder (4 levels up from
# _system/apps/dashboard/app.py). The fallback is computed lazily so the
# container path is never resolved.
_env_wiki = os.environ.get("WIKI_DIR")
WIKI_DIR = Path(_env_wiki) if _env_wiki else Path(__file__).resolve().parents[3] / "wiki"

# ADRs live in _system/adr/ (outside the wiki layer). Mounted read-only at /adr
# in Docker; falls back to the repo's _system/adr/ for local runs.
_env_adr = os.environ.get("ADR_DIR")
ADR_DIR = Path(_env_adr) if _env_adr else Path(__file__).resolve().parents[3] / "_system" / "adr"

# [[target]] | [[target|alias]] | [[target#heading]] | [[path/target|alias]]
WIKILINK_RE = re.compile(r"\[\[([^\]\|#]+)(?:#[^\]\|]+)?(?:\|([^\]]+))?\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


@dataclass
class Page:
    stem: str                       # filename without .md, e.g. GLO-006-kind
    meta: dict                      # parsed frontmatter
    body: str                       # markdown body (frontmatter stripped)
    folder: str                     # owning wiki subfolder, e.g. glossary

    @property
    def id(self) -> str:
        return self.meta.get("id", self.stem)

    @property
    def title(self) -> str:
        return self.meta.get("title", self.stem)

    @property
    def status(self) -> str:
        return self.meta.get("status", "")

    @property
    def aliases(self) -> list[str]:
        a = self.meta.get("aliases") or []
        return [x for x in a if x]

    def link_targets(self) -> set[str]:
        """Distinct wiki pages this page points to (frontmatter + body),
        excluding self-references and raw/ source provenance links."""
        targets: set[str] = set()
        haystack = yaml.safe_dump(self.meta, allow_unicode=True) + "\n" + self.body
        for m in WIKILINK_RE.finditer(haystack):
            tgt = m.group(1).strip()
            base = tgt.split("/")[-1]              # drop raw/ path prefix
            if tgt.startswith("raw/") or base.startswith("SRC-"):
                continue                            # provenance, not a relation
            if base == self.stem or base == self.id:
                continue                            # self-reference
            targets.add(base)
        return targets


# --- caching ----------------------------------------------------------------
#
# The wiki is parsed live on every request and was, before caching, re-read and
# re-parsed dozens of times per page (every `render_markdown` rebuilt the whole
# link index from disk). Two complementary layers fix that without ever serving
# stale content:
#
#   Tier 1  _parse() is memoized by (path, mtime). A file is re-read only when it
#           changes on disk, so editing a page and refreshing the browser still
#           shows the new text — but repeated reads (within a request and across
#           requests) collapse to a dict lookup. The cache lives for the worker's
#           lifetime; each gunicorn worker warms its own.
#
#   Tier 2  the aggregate builders (load_folder / load_all_pages / title_index /
#           link_index / load_adrs) are memoized for the duration of ONE request
#           via flask.g, so the tree is walked once per request instead of once
#           per markdown block rendered. Outside a request context they run
#           uncached (keeps build_* helpers usable standalone, e.g. for ISS-010).

# (path -> (mtime, parsed Page or None)); folder is deterministic from the path
# (always path.parent.name at every call site), so the path alone is the key.
_PARSE_CACHE: dict[Path, tuple[float, "Page | None"]] = {}


def _request_cached(func):
    """Memoize a builder for the current request (keyed by name + args). The
    cached objects are treated as read-only by every caller, so sharing the same
    reference across calls within a request is safe."""
    @functools.wraps(func)
    def wrapper(*args):
        if not has_request_context():
            return func(*args)
        cache = g.setdefault("_build_cache", {})
        key = (func.__name__, args)
        if key not in cache:
            cache[key] = func(*args)
        return cache[key]
    return wrapper


def _parse(path: Path, folder: str) -> Page | None:
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return None
    cached = _PARSE_CACHE.get(path)
    if cached is not None and cached[0] == mtime:
        return cached[1]
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        page = None
    else:
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            meta = {}
        page = Page(stem=path.stem, meta=meta, body=m.group(2), folder=folder)
    _PARSE_CACHE[path] = (mtime, page)
    return page


@_request_cached
def load_folder(folder: str) -> list[Page]:
    d = WIKI_DIR / folder
    if not d.is_dir():
        return []
    pages = [_parse(p, folder) for p in sorted(d.glob("*.md"))]
    return [p for p in pages if p is not None]


@_request_cached
def load_all_pages() -> list[Page]:
    """Every wiki page across all content-type folders, for global search."""
    out: list[Page] = []
    if WIKI_DIR.is_dir():
        for d in sorted(WIKI_DIR.iterdir()):
            if d.is_dir():
                out.extend(load_folder(d.name))
    return out


@_request_cached
def title_index() -> dict[str, str]:
    """Map every page stem -> human title, for resolving wikilinks to text."""
    idx: dict[str, str] = {}
    if not WIKI_DIR.is_dir():
        return idx
    for p in WIKI_DIR.rglob("*.md"):
        page = _parse(p, p.parent.name)
        if page:
            idx[p.stem] = page.title
    return idx


def _page_url(folder: str, stem: str) -> str:
    """Canonical dashboard URL for a wiki page. FRs have their own rich route;
    everything else uses the generic /page view."""
    if folder == "functional-requirements":
        return f"/functional-requirements/{stem}"
    return f"/page/{folder}/{stem}"


@_request_cached
def link_index() -> dict[str, tuple[str, str]]:
    """Map each page's stem and id -> (folder, stem), so body wikilinks like
    `[[STK-006-…|Backoffice]]` or `[[FR-008]]` resolve to a real target URL.
    Stems/ids are unique; first writer wins on the rare collision."""
    idx: dict[str, tuple[str, str]] = {}
    for p in load_all_pages():
        idx.setdefault(p.stem, (p.folder, p.stem))
        idx.setdefault(p.id, (p.folder, p.stem))
    return idx


# --- rendering helpers -----------------------------------------------------

def render_wikilinks(text: str, titles: dict[str, str],
                     links: dict[str, tuple[str, str]] | None = None) -> str:
    """Replace [[..]] with its alias (or resolved title). When `links` is given
    and the target resolves to a wiki page, emit a real hyperlink; otherwise
    (inline snippets, or an unresolved/raw target) keep the styled-text span."""
    def repl(m: re.Match) -> str:
        target, alias = m.group(1).strip(), m.group(2)
        base = target.split("/")[-1]
        label = alias.strip() if alias else titles.get(base, base)
        if links and not target.startswith("raw/") and not base.startswith("SRC-"):
            dest = links.get(base)
            if dest:
                return f'<a class="wl" href="{_page_url(*dest)}">{label}</a>'
        return f'<span class="wl">{label}</span>'
    return WIKILINK_RE.sub(repl, text)


CALLOUT_RE = re.compile(r"^>\s*\[!(\w+)\]\s*(.*)$", re.MULTILINE)


def render_markdown(body: str, titles: dict[str, str]) -> str:
    # full-text bodies get real hyperlinks; inline-snippet helpers keep spans
    body = render_wikilinks(body, titles, link_index())
    # turn Obsidian callouts `> [!type] title` into a bold label line
    body = CALLOUT_RE.sub(lambda m: f"> **{m.group(2) or m.group(1).title()}**", body)
    return md.markdown(body, extensions=["extra", "sane_lists", "nl2br"])


def extract_labeled(page: Page, label: str, titles: dict[str, str],
                    links: dict[str, tuple[str, str]] | None = None) -> str:
    """Pull the paragraph introduced by a bold lead like **Definition.** or
    **Snapshot.**, collapse whitespace, and render its wikilinks. Pass `links`
    (a link index) to turn resolvable targets into real hyperlinks instead of
    styled-text spans."""
    rx = re.compile(r"\*\*" + re.escape(label) + r"\.\*\*\s*(.+?)(?=\n\s*\n|\n\s*\*\*|$)", re.DOTALL)
    m = rx.search(page.body)
    raw = m.group(1).strip() if m else ""
    raw = re.sub(r"\s+", " ", raw)
    return render_wikilinks(raw, titles, links)


_PAM_BULLET_RE = re.compile(
    r"^[ \t]*-\s+\*\*(?P<label>[A-Za-zÄÖÜäöü]+)\.\*\*\s+"
    r"(?P<body>.+?)(?=\n[ \t]*-\s+\*\*|\n##\s|\n\s*\n|\Z)",
    re.DOTALL | re.MULTILINE,
)


def extract_pam_bullet(page: Page, label: str, titles: dict[str, str],
                       links: dict[str, tuple[str, str]] | None = None) -> str:
    """Pull a bullet-style PAM field (`- **Purpose.** …`) from a goal body.
    Bullets can wrap onto continuation lines; stops at the next sibling bullet,
    a new heading, or a blank line. Pass `links` to emit real hyperlinks."""
    for m in _PAM_BULLET_RE.finditer(page.body):
        if m.group("label").lower() == label.lower():
            raw = re.sub(r"\s+", " ", m.group("body")).strip()
            return render_wikilinks(raw, titles, links)
    return ""


# Status values that count as "closed" for the issues filter.
CLOSED_STATUSES = {"resolved", "wontfix"}


# --- ADRs (Nygard format, no frontmatter) ----------------------------------

ADR_HEADING_RE = re.compile(r"^#\s*(ADR-\d{3,4})\s*:\s*(.+?)\s*$", re.MULTILINE)
ADR_STATUS_RE = re.compile(r"\*\*Status:\*\*\s*(.+?)\s*$", re.MULTILINE)
ADR_DATE_RE = re.compile(r"\*\*Date:\*\*\s*(.+?)\s*$", re.MULTILINE)


def _normalize_adr_status(raw: str) -> str:
    """Collapse 'superseded by ADR-0007' etc. to a single filterable keyword."""
    s = raw.strip().lower()
    for key in ("proposed", "accepted", "superseded", "deprecated", "rejected"):
        if s.startswith(key):
            return key
    return s.split()[0] if s else "unknown"


@_request_cached
def load_adrs() -> list[dict]:
    """Parse _system/adr/*.md (skipping the template) into rendered records."""
    if not ADR_DIR.is_dir():
        return []
    titles = title_index()  # so [[wikilinks]] inside ADRs resolve to readable text
    adrs = []
    for p in sorted(ADR_DIR.glob("*.md")):
        if p.stem.startswith("0000"):
            continue  # the 0000-template.md is not a real decision
        text = p.read_text(encoding="utf-8")
        hm = ADR_HEADING_RE.search(text)
        if not hm or "NNNN" in hm.group(1):
            continue
        adr_id, title = hm.group(1), hm.group(2)
        sm, dm = ADR_STATUS_RE.search(text), ADR_DATE_RE.search(text)
        status_raw = sm.group(1).strip() if sm else ""
        date = dm.group(1).strip() if dm else ""
        if date in ("{{date}}", "YYYY-MM-DD", ""):
            date = "—"
        adrs.append({
            "id": adr_id,
            "num": int(re.sub(r"\D", "", adr_id)),
            "stem": p.stem,
            "title": title,
            "status": _normalize_adr_status(status_raw),
            "status_raw": status_raw,
            "date": date,
            "html": render_markdown(text, titles),
        })
    adrs.sort(key=lambda a: a["num"])
    return adrs


# --- req42 schema (the 12 building blocks) ---------------------------------
#
# The umbrella methodical reference (_system/anchors/req42.md). Each block maps
# to zero or more wiki folders; an "entry" is one page in those folders. Blocks
# 09–11 are deliberately out of scope (project-management concerns). "href" is
# where the block's "Alle ansehen" link points: an existing rich view where one
# exists (glossary/stakeholders/issues), otherwise a generic /req42/<slug> list.

REQ42_BLOCKS = [
    {"num": "01", "title": "Visionen & Ziele", "en": "Business Goals",
     "folders": ["goals"], "scope": "in", "href": "/goals", "slug": None,
     "note": ""},
    {"num": "02", "title": "Stakeholder", "en": "Stakeholders",
     "folders": ["stakeholders"], "scope": "in", "href": "/stakeholders", "slug": None, "note": ""},
    {"num": "03", "title": "Scope & Abgrenzung", "en": "Scope",
     "folders": ["context", "external-interfaces"], "scope": "in",
     "href": "/req42/scope", "slug": "scope", "note": ""},
    {"num": "04", "title": "Product Backlog", "en": "Product Backlog",
     "folders": ["functional-requirements"], "scope": "in",
     "href": "/req42/backlog", "slug": "backlog",
     "note": "Ein Typ, Stereotyp epic|feature|story; Hierarchie via parent: (ADR-0012)."},
    {"num": "05", "title": "Unterstützende Modelle", "en": "Supporting Models",
     "folders": ["use-cases", "activity-models", "data-models"], "scope": "in",
     "href": "/req42/modelle", "slug": "modelle", "note": ""},
    {"num": "06", "title": "Qualitätsanforderungen", "en": "Quality Requirements",
     "folders": ["quality-requirements"], "scope": "in",
     "href": "/req42/qualitaet", "slug": "qualitaet", "note": ""},
    {"num": "07", "title": "Randbedingungen", "en": "Constraints",
     "folders": ["constraints"], "scope": "in",
     "href": "/req42/randbedingungen", "slug": "randbedingungen", "note": ""},
    {"num": "08", "title": "Domänenbegriffe", "en": "Domain Terminology",
     "folders": ["glossary"], "scope": "in", "href": "/glossary", "slug": None, "note": ""},
    {"num": "09", "title": "Betriebsmittel & Personal", "en": "Assets",
     "folders": [], "scope": "out", "href": None, "slug": None,
     "note": "Projekt-Ressourcen — bewusst nicht erfasst."},
    {"num": "10", "title": "Teamstruktur", "en": "Teams",
     "folders": [], "scope": "out", "href": None, "slug": None,
     "note": "Organisations-/Team-Setup — bewusst nicht erfasst."},
    {"num": "11", "title": "Roadmaps", "en": "Roadmaps",
     "folders": [], "scope": "out", "href": None, "slug": None,
     "note": "Release-Planung — bewusst nicht erfasst."},
    {"num": "12", "title": "Risiken & Annahmen", "en": "Risks & Assumptions",
     "folders": ["issues"], "scope": "in", "href": "/issues", "slug": None,
     "note": "Issues (insb. kind: risk) plus [!assumption]-Markierungen."},
]

# Human-readable DE type label per wiki folder, for the "Typ" column.
FOLDER_LABELS = {
    "context": "Kontext",
    "external-interfaces": "Externe Schnittstelle",
    "functional-requirements": "Funktionale Anforderung",
    "use-cases": "Use Case",
    "activity-models": "Aktivitätsmodell",
    "data-models": "Datenmodell",
    "quality-requirements": "Qualitätsanforderung",
    "constraints": "Randbedingung",
    "glossary": "Begriff",
    "stakeholders": "Stakeholder",
    "issues": "Issue",
}

REQ42_BY_SLUG = {b["slug"]: b for b in REQ42_BLOCKS if b["slug"]}


def _block_pages(block: dict) -> list[Page]:
    """All wiki pages feeding one req42 block, sorted by id."""
    pages: list[Page] = []
    for folder in block["folders"]:
        pages.extend(load_folder(folder))
    return sorted(pages, key=lambda p: p.id)


def build_req42_blocks(sample: int = 5) -> list[dict]:
    """Enrich each block with its entry count and a few sample entries —
    shared by the index tile (counts) and the /req42 overview (samples).

    Block 01 (Visionen & Ziele) gets a special `diagram` payload: the Vision
    →Objectives tree replaces the sample list on the /req42 overview, and
    `claim` carries the Vision tagline as a sub-headline."""
    out = []
    for b in REQ42_BLOCKS:
        entries = [
            {"id": p.id, "title": p.title,
             "type": FOLDER_LABELS.get(p.folder, p.folder),
             "status": p.status, "relations": len(p.link_targets())}
            for p in _block_pages(b)
        ]
        block = {**b, "count": len(entries),
                 "entries": entries, "sample": entries[:sample]}
        if b["num"] == "01":
            goals = load_goals()
            block["diagram"] = _mermaid_goal_tree(goals["vision"], goals["objectives"])
            block["claim"] = (str(goals["vision"].meta.get("tile_claim") or "").strip()
                              if goals["vision"] else "")
        if b["num"] == "05":
            # collapse 13+ entity pages into one row per model TYPE
            type_rows = _supporting_model_entries()
            block["sample"] = type_rows
            block["entries"] = type_rows
        out.append(block)
    return out


# --- context diagram (req42 block 03) --------------------------------------
#
# The system context is NOT stored as a diagram (ADR-0013, ISS-010): it is
# projected live from the structured edges — each external interface's `flows`
# and each stakeholder's `provides:`/`receives:` — into a mermaid flowchart.
# Center = the system (blueish box); systems/organizations = light-grey boxes;
# human roles = actor symbol (👤). Stakeholders are merged/hidden/shaped per their
# `context_role`/`nature` fields (ADR-0014). No node links (not needed yet).

_NID_RE = re.compile(r"[^A-Za-z0-9]")


def _diagram_node_id(raw: str) -> str:
    return _NID_RE.sub("", str(raw)) or "N"


def _clean_label(s: object) -> str:
    """Resolve [[a|b]]→b / [[a]]→a, drop a trailing (parenthetical), strip chars
    that would break the mermaid/HTML text so labels are always render-safe."""
    t = str(s or "")
    t = re.sub(r"\[\[[^\]|]+\|([^\]]+)\]\]", r"\1", t)                       # [[a|b]] -> b
    t = re.sub(r"\[\[([^\]]+)\]\]", lambda m: m.group(1).split("/")[-1], t)  # [[a]]   -> a
    t = re.sub(r"\s*\([^)]*\)\s*$", "", t)                                   # trailing (…)
    t = re.sub(r'[<>"&|]', "", t)
    return re.sub(r"\s+", " ", t).strip()


def build_context_diagram(center: str = "AQUARIUS") -> str | None:
    """Project a mermaid context diagram from EIF.flows + STK.provides/receives.

    Returns None when no edges exist yet. Pure and string-only, so the planned
    audit-loop (ISS-010) can reuse it outside the request cycle."""
    core = "CORE"
    nodes: list[tuple[str, str, str]] = []   # (node_id, label, css_class)
    edges: list[str] = []

    def edge(src: str, items, dst: str) -> None:
        labels = [l for l in (_clean_label(i) for i in (items or [])) if l]
        if labels:
            edges.append(f'  {src} -->|"{", ".join(labels)}"| {dst}')

    # real external systems — one node each (ADR-0013), flows grouped per direction
    for p in load_folder("external-interfaces"):
        flows = [f for f in (p.meta.get("flows") or []) if isinstance(f, dict)]
        ins = [f.get("data") for f in flows
               if str(f.get("direction", "")).lower() in ("inbound", "bidirectional")]
        outs = [f.get("data") for f in flows
                if str(f.get("direction", "")).lower() in ("outbound", "bidirectional")]
        if not (ins or outs):
            continue
        nid = _diagram_node_id(p.id)
        nodes.append((nid, _clean_label(p.meta.get("partner") or p.title), "system"))
        edge(nid, ins, core)
        edge(core, outs, nid)

    # user roles — flows live on the stakeholder, not as EIF nodes. ADR-0014:
    # several stakeholders sharing a `context_role` merge into ONE node (union of
    # their flows); `context_role: none` hides the role; `nature: organization`
    # draws a box instead of the person/actor symbol.
    def _union(dst: list, src) -> None:
        for x in (src or []):
            if x not in dst:
                dst.append(x)

    groups: dict[str, dict] = {}   # label -> {prov, recv, cls, order}
    for p in load_folder("stakeholders"):
        prov, recv = p.meta.get("provides") or [], p.meta.get("receives") or []
        if not (prov or recv):
            continue
        raw_role = p.meta.get("context_role")
        if isinstance(raw_role, str) and raw_role.strip().lower() == "none":
            continue
        label = _clean_label(raw_role) if raw_role else _clean_label(p.title)
        is_org = str(p.meta.get("nature", "person")).strip().lower() == "organization"
        g = groups.get(label)
        if g is None:
            g = groups[label] = {"prov": [], "recv": [], "cls": "actor", "order": len(groups)}
        if is_org:
            g["cls"] = "system"          # organizations/systems share the box style
        _union(g["prov"], prov)
        _union(g["recv"], recv)

    for label, g in sorted(groups.items(), key=lambda kv: kv[1]["order"]):
        nid = _diagram_node_id(label)
        nodes.append((nid, label, g["cls"]))
        edge(nid, g["prov"], core)
        edge(core, g["recv"], nid)

    if not edges:
        return None

    lines = ["flowchart LR", f'  {core}["{_clean_label(center)}"]:::core']
    for nid, label, cls in nodes:
        # persons get the actor symbol (stadium + 👤); systems/organizations are boxes
        if cls == "actor":
            lines.append(f'  {nid}(["👤 {label}"]):::actor')
        else:
            lines.append(f'  {nid}["{label}"]:::{cls}')
    lines += edges
    lines += [
        "  classDef core fill:#2f6fb3,stroke:#7fc0ff,stroke-width:2px,color:#ffffff,font-weight:bold;",
        "  classDef system fill:#d7dbe3,stroke:#9aa3b2,color:#15202e;",
        "  classDef actor fill:#f3f6fb,stroke:#aeb8c9,color:#15202e;",
    ]
    return "\n".join(lines)


# --- glossary term network (ADR-0023) --------------------------------------
#
# A force-directed graph of the glossary, projected from the `related:` edges.
# The server emits cytoscape elements ({nodes, edges}); the browser lays them
# out (cytoscape.js). Single source of truth stays the typed edges — only the
# layout is client-side. Default view is GLO-only; cross-type neighbours (1-hop)
# are revealed per type by buttons. Edges are undirected & deduplicated and come
# ONLY from `related:` frontmatter (body wikilinks would add uncurated noise, so
# link_targets() is deliberately NOT used here).

# Stem prefix -> wiki folder, for click-through URLs (/page/<folder>/<stem>).
_TYPE_FOLDER = {
    "GLO": "glossary", "DM": "data-models", "STK": "stakeholders",
    "EIF": "external-interfaces", "GOAL": "goals", "CTX": "context",
    "FR": "functional-requirements", "CON": "constraints", "ISS": "issues",
    "UC": "use-cases", "AM": "activity-models", "QR": "quality-requirements",
}


def _stem_of_link(raw: object) -> str:
    """A `related:` entry like '[[GLO-026-eaqua|EAquA]]' -> 'GLO-026-eaqua'."""
    t = str(raw or "").strip()
    m = re.search(r"\[\[([^\]]+)\]\]", t)
    if m:
        t = m.group(1)
    t = t.split("|")[0].split("#")[0].strip()   # drop alias / anchor
    return t.split("/")[-1].strip()             # drop raw/ path prefix


def _type_of(stem: str) -> str:
    return stem.split("-")[0] if "-" in stem else stem


def build_glossary_graph() -> dict:
    """Project the glossary term network from `related:` edges (ADR-0023).

    Pure and dict-only, so it is testable and reusable outside a request.
    Returns cytoscape elements: {"nodes", "edges", "layer_counts"}. GLO nodes
    carry core=True (shown by default); cross-type neighbours (1-hop) are tagged
    by type for the layer buttons. Edges are undirected and deduplicated and
    sourced only from `related:`."""
    glossary = load_folder("glossary")
    glo_stems = {p.stem for p in glossary}
    by_stem = {p.stem: p for p in load_all_pages()}   # existence + title/folder

    seen_pairs: set[frozenset] = set()
    edges: list[dict] = []
    glo_degree: dict[str, int] = {s: 0 for s in glo_stems}
    neighbour_stems: set[str] = set()

    for p in glossary:                       # src is always a GLO page
        src = p.stem
        for raw in (p.meta.get("related") or []):
            tgt = _stem_of_link(raw)
            if not tgt or tgt == src or tgt not in by_stem:
                continue                     # self / dangling / non-page
            pair = frozenset((src, tgt))
            if pair in seen_pairs:
                continue                     # undirected dedup
            seen_pairs.add(pair)
            cross = tgt not in glo_stems
            edge = {"id": f"e{len(edges)}", "source": src, "target": tgt, "cross": cross}
            if cross:
                edge["ntype"] = _type_of(tgt)
                neighbour_stems.add(tgt)
            else:
                glo_degree[src] += 1
                glo_degree[tgt] += 1
            edges.append(edge)

    nodes: list[dict] = []
    for p in glossary:
        state = ("deprecated" if p.status == "deprecated"
                 else "agreed" if p.meta.get("agreed") is True
                 else "draft")
        nodes.append({
            "id": p.stem, "label": p.title, "type": "GLO", "core": True,
            "url": f"/page/glossary/{p.stem}",
            "degree": glo_degree.get(p.stem, 0),
            "state": state,
            "assumption": "[!assumption]" in p.body,
            "aliases": ", ".join(p.aliases),
        })
    named = {"DM", "STK", "EIF", "GOAL"}   # types with their own colour + button
    for stem in sorted(neighbour_stems):
        pg = by_stem[stem]
        ntype = _type_of(stem)
        node = {
            "id": stem, "label": pg.title, "type": ntype, "core": False,
            "url": f"/page/{_TYPE_FOLDER.get(ntype, pg.folder)}/{stem}",
        }
        if ntype not in named:
            node["rest"] = 1   # CTX/FR/CON/ISS/… → grey, selected via node[rest]
        nodes.append(node)

    layer_counts: dict[str, int] = {}
    for e in edges:
        if e["cross"]:
            layer_counts[e["ntype"]] = layer_counts.get(e["ntype"], 0) + 1

    return {
        "nodes": [{"data": n} for n in nodes],
        "edges": [{"data": e} for e in edges],
        "layer_counts": layer_counts,
    }


# Neighbour types the per-term ego snippet offers as buttons (ADR-0023): GLO shown by
# default, DM/STK/GOAL revealed on demand. A focused 1-hop slice for a glossary detail page.
_EGO_TYPES = {"GLO", "DM", "STK", "GOAL"}


def build_glossary_ego_graph(stem: str) -> dict | None:
    """1-hop ego network of a single glossary term for the detail-page snippet
    (ADR-0023): the focal GLO node + its immediate neighbours of type GLO/DM/STK/GOAL
    and the edges among them. A pure filtered projection of build_glossary_graph();
    returns None if the term has no node (not a glossary page)."""
    full = build_glossary_graph()
    node_by_id = {n["data"]["id"]: n["data"] for n in full["nodes"]}
    if stem not in node_by_id:
        return None

    nbrs: set[str] = set()
    for e in full["edges"]:
        d = e["data"]
        if d["source"] == stem:
            nbrs.add(d["target"])
        elif d["target"] == stem:
            nbrs.add(d["source"])

    ego_ids = {stem} | {n for n in nbrs
                        if node_by_id.get(n, {}).get("type") in _EGO_TYPES}

    nodes = []
    for nid in ego_ids:
        data = dict(node_by_id[nid])
        if nid == stem:
            data["focus"] = True
        nodes.append({"data": data})
    edges = [e for e in full["edges"]
             if e["data"]["source"] in ego_ids and e["data"]["target"] in ego_ids]

    layer_counts: dict[str, int] = {}
    for e in edges:
        d = e["data"]
        if d.get("cross") and d.get("ntype") in _EGO_TYPES:
            layer_counts[d["ntype"]] = layer_counts.get(d["ntype"], 0) + 1

    return {"nodes": nodes, "edges": edges, "layer_counts": layer_counts}


# Group label per stem-type for the detail-page relations panel.
_TYPE_LABEL = {
    "GLO": "Begriffe", "STK": "Stakeholder", "DM": "Datenmodelle", "CTX": "Kontext",
    "EIF": "Externe Schnittstellen", "GOAL": "Ziele", "FR": "Funktionale Anforderungen",
    "UC": "Use Cases", "AM": "Aktivitätsmodelle", "QR": "Qualitätsanforderungen",
    "CON": "Randbedingungen", "ISS": "Issues",
}
_REL_TYPE_ORDER = ["GLO", "STK", "DM", "CTX", "EIF", "GOAL", "FR", "UC", "AM", "QR", "CON", "ISS"]


def build_relations_panel(stem: str) -> dict:
    """Outbound links (this page's `related:` + body wikilinks) and inbound
    backlinks (other pages that reference it), grouped by type, as link dicts.
    A pure projection over the link graph (ADR-0018) — powers the 'Verweist auf'
    / 'Taucht auf in' section on a detail page."""
    titles = title_index()
    pages = load_all_pages()
    by_stem = {p.stem: p for p in pages}

    def info(s: str) -> dict:
        ntype = _type_of(s)
        folder = _TYPE_FOLDER.get(ntype)
        if folder == "functional-requirements":
            url = f"/functional-requirements/{s}"
        elif folder:
            url = f"/page/{folder}/{s}"
        else:
            url = f"/page/{by_stem[s].folder}/{s}"
        return {"id": by_stem[s].id if s in by_stem else s,
                "label": titles.get(s, s), "url": url, "type": ntype}

    me = by_stem.get(stem)
    outbound = sorted(s for s in (me.link_targets() if me else ()) if s in by_stem)
    out_set = set(outbound)
    inbound = sorted(q.stem for q in pages
                     if q.stem != stem and q.stem not in out_set
                     and stem in q.link_targets())

    def grouped(stems: list) -> list:
        buckets: dict[str, list] = {}
        for s in stems:
            i = info(s)
            buckets.setdefault(i["type"], []).append(i)
        ordered = _REL_TYPE_ORDER + [t for t in buckets if t not in _REL_TYPE_ORDER]
        return [{"type": t, "label": _TYPE_LABEL.get(t, t), "links": buckets[t]}
                for t in ordered if t in buckets]

    return {"outbound": grouped(outbound), "inbound": grouped(inbound)}


# --- goals (req42 block 01: vision + objectives) ---------------------------
#
# One content type `goal` with stereotype `vision | objective` (ADR-0016).
# Vision = `GOAL-001`, Objectives = `GOAL-002..` in Wertkette order (Saisonplanung
# → Anmeldung → Planung → Durchführung → Auswertung → Urkunde). The Goal↔Epic
# edge is pinned at the Epic (`goal:` field on each FR, ADR-0018); coverage and
# tile counters are pure projections from those edges.

# Wertkette-Reihenfolge der Objectives (siehe raw/vision-draft.md „Konsens & Spec").
GOAL_WERTKETTE = ["GOAL-002", "GOAL-003", "GOAL-004", "GOAL-005"]


def _goal_id_from_ref(ref: object) -> str:
    """From '[[GOAL-002-foo]]' / 'GOAL-002-foo' / 'GOAL-002', return 'GOAL-002'."""
    s = str(ref or "").strip()
    m = re.match(r"\[\[([^\]\|#]+)", s)
    stem = (m.group(1) if m else s).split("/")[-1].strip()
    parts = stem.split("-", 2)
    if len(parts) >= 2 and parts[0].upper() == "GOAL":
        return f"GOAL-{parts[1]}"
    return stem


def _goal_maturity(p: Page) -> str:
    """PAM until `horizon:` is set, then promotion to SMART (ADR-0016 / anchor)."""
    return "SMART" if str(p.meta.get("horizon") or "").strip() else "PAM"


_VISION_SECTION_RE = re.compile(r"##\s+Vision\b[^\n]*\n+(.+?)(?=\n##\s|\Z)", re.DOTALL)


def _vision_full_paragraph(page: Page, titles: dict[str, str],
                           links: dict[str, tuple[str, str]] | None = None) -> str:
    """First paragraph under `## Vision` in the Vision page; inline markdown
    (`**bold**`, wikilinks) is rendered, no <p> wrapper. Pass `links` to emit
    real hyperlinks for resolvable targets."""
    if not page:
        return ""
    m = _VISION_SECTION_RE.search(page.body)
    if not m:
        return ""
    para = m.group(1).split("\n\n")[0]
    para = re.sub(r"\s+", " ", para).strip()
    para = render_wikilinks(para, titles, links)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", para)


def load_goals() -> dict:
    """Return everything the tile and /goals page need.

    Shape:
      vision     — the GOAL-001 Page (stereotype: vision) or None
      objectives — list of GOAL-002…005 Pages in Wertkette order
      coverage   — { 'GOAL-NNN': [FR-Page, ...] } from FR.goal: backlinks
      enablers   — list of FR-Pages with goal: [] (explicit enablers, ADR-0018)
      frs        — all FR-Pages sorted by id (column order for the matrix)
    """
    by_id: dict[str, Page] = {p.id: p for p in load_folder("goals")}
    vision = by_id.get("GOAL-001")
    objectives = [by_id[gid] for gid in GOAL_WERTKETTE if gid in by_id]

    frs = sorted(load_folder("functional-requirements"), key=lambda p: p.id)
    coverage: dict[str, list[Page]] = {gid: [] for gid in GOAL_WERTKETTE}
    enablers: list[Page] = []
    for fr in frs:
        refs = fr.meta.get("goal") or []
        if not refs:
            enablers.append(fr)
            continue
        for ref in refs:
            gid = _goal_id_from_ref(ref)
            if gid in coverage:
                coverage[gid].append(fr)
    return {"vision": vision, "objectives": objectives,
            "coverage": coverage, "enablers": enablers, "frs": frs}


def build_vision_tile(data: dict, titles: dict[str, str]) -> dict:
    """The home-tile payload for the Vision card (key='vision')."""
    vision = data["vision"]
    objectives = data["objectives"]
    coverage = data["coverage"]
    if not vision:
        return {
            "key": "vision", "label": "Vision", "href": None,
            "count": "—", "unit": "Platzhalter", "icon": "🎯",
            "rows": [], "active": False,
        }
    claim = str(vision.meta.get("tile_claim") or "").strip()
    rows = [{
        "id": o.id,
        "title": o.title,
        "epics": len(coverage.get(o.id, [])),
    } for o in objectives]
    return {
        "key": "vision", "label": "Vision", "href": "/goals",
        "icon": "🎯", "active": True,
        "claim": claim,
        "objective_rows": rows,
    }


# --- product backlog (req42 block 04: Epic→Feature→Story hierarchy) ---------
#
# One content type `functional-requirement` with stereotype epic|feature|story
# (ADR-0012). The hierarchy edge is the `parent:` wikilink field; build_backlog
# is a pure projection over those edges — the single source for both the home
# tile and the /req42/backlog page (cf. load_goals / _mermaid_goal_tree).

def _fr_stem_from_ref(ref: object) -> str:
    """From '[[FR-009-foo]]' / 'FR-009-foo' / a bare stem, return the page stem
    (children are matched to parents by stem)."""
    s = str(ref or "").strip()
    m = re.match(r"\[\[([^\]\|#]+)", s)
    return (m.group(1) if m else s).split("/")[-1].strip()


def _fr_stereotype(p: "Page") -> str:
    return str(p.meta.get("stereotype") or "").strip().lower()


def _fr_sort_key(p: "Page"):
    """Backlog order: numeric `order:` field, then id as a stable tiebreak."""
    try:
        order = int(p.meta.get("order"))
    except (TypeError, ValueError):
        order = 9999
    return (order, p.id)


def _fr_node(p: "Page") -> dict:
    """Slim per-page record shared by tile rows, cards, and the diagram."""
    return {
        "id": p.id, "title": p.title, "stem": p.stem,
        "priority": str(p.meta.get("priority") or "").strip(),
        "status": p.status,
    }


def build_backlog() -> dict:
    """Project the Epic→Feature→Story hierarchy from each FR's `parent:` field.

    Returns:
      epics          — list of epic dicts in `order` then id order; each carries
                       `features` (with nested `stories`), `direct_stories`
                       (stories hung straight off the epic), `n_features`
                       (direct feature children) and `n_stories` (its direct
                       stories plus the stories of its direct features — exactly
                       what the page renders), plus priority/release/status.
      total_epics / total_features / total_stories — aggregate counters.
      orphans        — feature/story pages whose parent does not resolve to a
                       known FR (normally empty; surfaced for visibility).
    """
    pages = load_folder("functional-requirements")
    by_stem = {p.stem: p for p in pages}

    def parent_stem(p: "Page") -> str | None:
        # The backlog is a tree: we take the first parent only. A page with
        # multiple parents is placed under its first; multi-parent graphs are
        # out of scope for this view.
        for ref in (p.meta.get("parent") or []):
            stem = _fr_stem_from_ref(ref)
            if stem:
                return stem
        return None

    children: dict[str, list["Page"]] = {}
    for p in pages:
        ps = parent_stem(p)
        if ps:
            children.setdefault(ps, []).append(p)

    def kids(stem: str, stereo: str) -> list["Page"]:
        return sorted((c for c in children.get(stem, []) if _fr_stereotype(c) == stereo),
                      key=_fr_sort_key)

    epics = sorted((p for p in pages if _fr_stereotype(p) == "epic"), key=_fr_sort_key)
    epic_rows = []
    total_features = total_stories = 0
    for e in epics:
        feats = kids(e.stem, "feature")
        feature_rows = [
            {**_fr_node(f), "stories": [_fr_node(s) for s in kids(f.stem, "story")]}
            for f in feats
        ]
        direct_stories = [_fr_node(s) for s in kids(e.stem, "story")]
        # n_stories counts exactly what the page renders — the epic's direct
        # stories plus the stories of its direct features (the model is two
        # levels: epic→feature→story / epic→story). Computed from the built
        # structure, not by recursion, so a malformed/cyclic parent: edge can
        # never run away and 500 the dashboard.
        n_features = len(feats)
        n_stories = len(direct_stories) + sum(len(f["stories"]) for f in feature_rows)
        total_features += n_features
        total_stories += n_stories
        epic_rows.append({
            **_fr_node(e),
            "release": str(e.meta.get("release") or "").strip(),
            "n_features": n_features,
            "n_stories": n_stories,
            "features": feature_rows,
            "direct_stories": direct_stories,
        })

    orphans = []
    for p in pages:
        st = _fr_stereotype(p)
        if st in ("feature", "story"):
            ps = parent_stem(p)
            if ps is None or ps not in by_stem:
                orphans.append({**_fr_node(p), "stereotype": st})

    return {
        "epics": epic_rows,
        "total_epics": len(epics),
        "total_features": total_features,
        "total_stories": total_stories,
        "orphans": orphans,
    }


def _mermaid_goal_epic_tree(goals: dict, backlog: dict) -> str | None:
    """Compact top-of-backlog map: each Objective links down to the Epics that
    contribute to it (FR `goal:` coverage, ADR-0018). Enabler epics (`goal: []`)
    hang under a shared `Plattform / Enabler` node so they stay visible. Two
    levels only — it must stay readable as the backlog grows, which is exactly
    why the old full Epic→Feature→Story tree was split out to the epic pages.
    Goal nodes jump to their card on /goals; epic nodes open their epic page.
    Returns None when there are no epics."""
    epics = backlog.get("epics") or []
    if not epics:
        return None
    epic_by_id = {e["id"]: e for e in epics}
    objectives = goals.get("objectives") or []
    coverage = goals.get("coverage") or {}
    enablers = goals.get("enablers") or []

    lines = ["graph TD"]
    seen: set[str] = set()

    def epic_edge(parent_nid: str, e: dict) -> None:
        # An epic may contribute to several goals (a DAG): declare its node with
        # label + click once, then reference it by id on every further edge.
        nid = _diagram_node_id(e["id"])
        if e["id"] in seen:
            lines.append(f'  {parent_nid} --> {nid}')
            return
        label = _clean_label(e["title"])
        lines.append(f'  {parent_nid} --> {nid}["{e["id"]}<br/>{label}"]:::epic')
        lines.append(f'  click {nid} "/functional-requirements/{e["stem"]}"')
        seen.add(e["id"])

    for o in objectives:
        gid = _diagram_node_id(o.id)
        glabel = _clean_label(_short_title(o))
        lines.append(f'  {gid}["{o.id}<br/>{glabel}"]:::goal')
        lines.append(f'  click {gid} "/goals#{o.id}"')
        for fr in coverage.get(o.id, []):
            e = epic_by_id.get(fr.id)
            if e:  # only epics belong on this map (features/stories carry no goal:)
                epic_edge(gid, e)

    enabler_epics = [epic_by_id[fr.id] for fr in enablers if fr.id in epic_by_id]
    if enabler_epics:
        lines.append('  ENABLER["Plattform / Enabler"]:::enabler')
        for e in enabler_epics:
            epic_edge("ENABLER", e)

    lines += [
        "  classDef goal fill:#2f6fb3,stroke:#7fc0ff,color:#ffffff,stroke-width:2px,font-weight:bold;",
        "  classDef enabler fill:#3a3f4b,stroke:#7a8497,color:#ffffff,font-weight:bold;",
        "  classDef epic fill:#d7dbe3,stroke:#9aa3b2,color:#15202e;",
    ]
    return "\n".join(lines)


def _mermaid_fr_subtree(node: dict | None) -> str | None:
    """One FR's own breakdown as a focused mermaid, drawn on its FR page so the
    backlog overview can stay compact. Handles both an epic root (→ its Features
    → their Stories, plus stories hung straight off the epic) and a feature root
    (→ its Stories). Descendant nodes click through to their own FR page.
    Returns None when the node is a leaf (a story, or an un-broken-down FR)."""
    if not node:
        return None
    feats = node.get("features") or []
    own_stories = node.get("stories") or []          # set when the root is a feature
    direct = node.get("direct_stories") or []        # epic's stories without a feature
    if not feats and not own_stories and not direct:
        return None
    rid = _diagram_node_id(node["id"])
    lines = ["graph TD", f'  {rid}["{node["id"]}<br/>{_clean_label(node["title"])}"]:::root']

    def child(parent_nid: str, rec: dict, css: str) -> str:
        nid = _diagram_node_id(rec["id"])
        label = _clean_label(rec["title"])
        lines.append(f'  {parent_nid} --> {nid}["{rec["id"]}<br/>{label}"]:::{css}')
        lines.append(f'  click {nid} "/functional-requirements/{rec["stem"]}"')
        return nid

    for f in feats:
        fid = child(rid, f, "feature")
        for s in f.get("stories") or []:
            child(fid, s, "story")
    for s in own_stories:
        child(rid, s, "story")
    for s in direct:
        child(rid, s, "story")

    lines += [
        "  classDef root fill:#2f6fb3,stroke:#7fc0ff,color:#ffffff,stroke-width:2px,font-weight:bold;",
        "  classDef feature fill:#d7dbe3,stroke:#9aa3b2,color:#15202e;",
        "  classDef story fill:#f3f6fb,stroke:#c4ccd9,color:#15202e;",
    ]
    return "\n".join(lines)


def _backlog_node(backlog: dict, stem: str) -> tuple[dict | None, str | None]:
    """Locate the built hierarchy node for a stem within build_backlog()'s tree.
    Returns (node, kind) with kind ∈ {epic, feature, story}; (None, None) if the
    stem is not an FR in the backlog (e.g. an orphan or unknown page)."""
    for e in backlog["epics"]:
        if e["stem"] == stem:
            return e, "epic"
        for f in e["features"]:
            if f["stem"] == stem:
                return f, "feature"
            for s in f["stories"]:
                if s["stem"] == stem:
                    return s, "story"
        for s in e["direct_stories"]:
            if s["stem"] == stem:
                return s, "story"
    return None, None


def _fr_ancestors(stem: str) -> list[dict]:
    """The parent chain for an FR (root epic first), walked over the first-parent
    `parent:` edge. Powers the FR-page breadcrumb. Cycle-guarded."""
    pages = {p.stem: p for p in load_folder("functional-requirements")}
    out: list[dict] = []
    cur, seen = pages.get(stem), {stem}
    while cur:
        ps = None
        for ref in (cur.meta.get("parent") or []):
            ps = _fr_stem_from_ref(ref)
            if ps:
                break
        if not ps or ps in seen:
            break
        seen.add(ps)
        parent = pages.get(ps)
        if not parent:
            break
        out.append({"id": parent.id, "title": parent.title, "stem": parent.stem})
        cur = parent
    return list(reversed(out))


# --- global search ---------------------------------------------------------

def build_search_records() -> list[dict]:
    """A flat, lower-cased index over every wiki page plus the ADRs. Each record
    links to that unit's own detail page and carries both the full searchable
    text (for the /search page) and a slim title/id key (for the tile preview).
    Small enough to filter client-side today; the same shape feeds lunr.js later."""
    records = []
    for p in load_all_pages():
        kind = FOLDER_LABELS.get(p.folder, p.folder)
        text = " ".join(filter(None, [p.id, p.title, " ".join(p.aliases), p.body]))
        records.append({
            "id": p.id,
            "type": kind,
            "title": p.title,
            "status": p.status,
            "url": (f"/functional-requirements/{p.stem}"
                    if p.folder == "functional-requirements"
                    else f"/page/{p.folder}/{p.stem}"),
            "text": re.sub(r"\s+", " ", text).strip().lower(),
            "key": " ".join([p.id, p.title, " ".join(p.aliases), kind]).strip().lower(),
        })
    for a in load_adrs():
        plain = re.sub(r"<[^>]+>", " ", a["html"])  # strip tags from rendered body
        records.append({
            "id": a["id"],
            "type": "ADR",
            "title": a["title"],
            "status": a["status"],
            "url": f"/page/adr/{a['stem']}",
            "text": re.sub(r"\s+", " ", f'{a["id"]} {a["title"]} {plain}').strip().lower(),
            "key": f'{a["id"]} {a["title"]} adr'.lower(),
        })
    return records


# --- views -----------------------------------------------------------------

@app.route("/")
def index():
    titles = title_index()
    glossary = load_folder("glossary")
    issues = load_folder("issues")
    stakeholders = load_folder("stakeholders")
    adrs = load_adrs()

    def by_relations(pages):
        return sorted(
            ({"title": p.title, "id": p.id, "relations": len(p.link_targets())} for p in pages),
            key=lambda r: (-r["relations"], r["id"]),
        )

    open_issues = [i for i in issues if i.status not in CLOSED_STATUSES]

    req42_blocks = build_req42_blocks()
    req42_rows = [
        {"num": b["num"], "title": b["title"], "count": b["count"], "scope": b["scope"]}
        for b in req42_blocks
    ]
    req42_total = sum(b["count"] for b in req42_blocks if b["scope"] == "in")
    req42_in_scope = sum(1 for b in req42_blocks if b["scope"] == "in")

    # Slim index embedded in the page so the search tile can preview matches
    # as the user types (title/id/type only — full-text search lives on /search).
    search_slim = [
        {"id": r["id"], "type": r["type"], "title": r["title"], "url": r["url"], "key": r["key"]}
        for r in build_search_records()
    ]

    vision_tile = build_vision_tile(load_goals(), titles)
    backlog = build_backlog()
    backlog_tile = {
        "key": "backlog", "label": "Product Backlog", "href": "/req42/backlog",
        "count": backlog["total_epics"], "unit": "Epics", "icon": "🗂️",
        "sub": f'{backlog["total_features"]} Features · {backlog["total_stories"]} Stories',
        "active": True,
        "epic_rows": [
            {"id": e["id"], "title": e["title"],
             "n_features": e["n_features"], "n_stories": e["n_stories"]}
            for e in backlog["epics"]
        ],
    }

    # Row 1: Vision, req42, Suche.  Row 2: Product Backlog, Glossar, Stakeholder.
    # Row 3+: ADRs, Issues, Datenmodell.
    tiles = [
        vision_tile,
        {
            "key": "req42", "label": "req42", "href": "/req42",
            "count": req42_total, "unit": "Einträge", "logo": "req42-logo-white.png",
            "rows": req42_rows, "active": True,
            "sub": f"{req42_in_scope} von 12 Blöcken",
        },
        {
            "key": "search", "label": "Suche", "href": "/search", "icon": "🔎",
            "rows": [], "active": True, "search": True,
        },
        backlog_tile,
        {
            "key": "glossary", "label": "Glossar",
            "count": len(glossary), "unit": "Begriffe", "icon": "📖",
            "rows": by_relations(glossary), "active": True,
            "links": [
                {"label": "Tabelle", "href": "/glossary"},
                {"label": "Begriffsnetz", "href": "/graph/glossary"},
            ],
        },
        {
            "key": "stakeholders", "label": "Stakeholder", "href": "/stakeholders",
            "count": len(stakeholders), "unit": "Personas", "icon": "👥",
            "rows": by_relations(stakeholders), "active": True,
        },
        {
            "key": "adrs", "label": "ADRs", "href": "/adrs",
            "count": len(adrs), "unit": "Entscheidungen", "icon": "🏛️",
            "rows": [{"id": a["id"], "title": a["title"], "status": a["status"]} for a in adrs],
            "active": True,
        },
        {
            "key": "issues", "label": "Issues", "href": "/issues",
            "count": len(issues), "unit": "Issues", "icon": "⚠️",
            "rows": [], "active": True,
            "sub": f"{len(open_issues)} offen",
        },
        {
            "key": "data-model", "label": "Datenmodell", "href": "/data-model",
            "icon": "🧩", "active": True,
            "diagram": build_data_model_kind_diagram(),
            "claim": f"{len(load_folder('data-models'))} Entitäten · Kernknoten: Kind",
        },
    ]
    needs_mermaid = any(t.get("diagram") for t in tiles)
    return render_template("index.html", tiles=tiles, search_slim=search_slim,
                           needs_mermaid=needs_mermaid)


@app.route("/glossary")
def glossary_view():
    titles = title_index()
    links = link_index()       # so definition wikilinks render as real hyperlinks
    pages = load_folder("glossary")
    rows = []
    for p in pages:
        rows.append({
            "id": p.id,
            "stem": p.stem,
            "title": p.title,
            "aliases": p.aliases,
            "definition": extract_labeled(p, "Definition", titles, links),
            "relations": len(p.link_targets()),
            "status": p.status,
            "created": str(p.meta.get("created", "")),
            "updated": str(p.meta.get("updated", "")),
            "assumption": "[!assumption]" in p.body,
        })
    # Default order is alphabetical by term; other orders are applied client-side.
    rows.sort(key=lambda r: r["title"].lower())
    return render_template("glossary.html", rows=rows, total=len(rows))


@app.route("/graph/glossary")
def glossary_graph_view():
    """Force-directed glossary term network (ADR-0023). The graph data is a
    deterministic server projection; cytoscape.js lays it out client-side."""
    graph = build_glossary_graph()
    counts = graph["layer_counts"]
    NAMED = [("DM", "Datenmodell"), ("STK", "Stakeholder"),
             ("EIF", "Schnittstelle"), ("GOAL", "Ziele")]
    named_keys = {k for k, _ in NAMED}
    named_layers = [{"key": k, "label": l, "count": counts[k]}
                    for k, l in NAMED if counts.get(k)]
    rest_keys = [k for k in counts if k not in named_keys]
    rest = {"types": rest_keys, "count": sum(counts[k] for k in rest_keys)}
    n_glo = sum(1 for n in graph["nodes"] if n["data"].get("type") == "GLO")
    return render_template("graph.html", graph=graph, n_glo=n_glo,
                           named_layers=named_layers, rest=rest)


@app.route("/issues")
def issues_view():
    titles = title_index()
    pages = sorted(load_folder("issues"), key=lambda x: x.id)
    items = []
    for p in pages:
        items.append({
            "id": p.id,
            "title": p.title,
            "status": p.status,
            "is_open": p.status not in CLOSED_STATUSES,
            "severity": p.meta.get("severity", ""),
            "kind": p.meta.get("kind", ""),
            "html": render_markdown(p.body, titles),
        })
    open_count = sum(1 for i in items if i["is_open"])
    return render_template(
        "issues.html", items=items, total=len(items),
        open_count=open_count, closed_count=len(items) - open_count,
    )


@app.route("/stakeholders")
def stakeholders_view():
    titles = title_index()
    links = link_index()       # snapshot wikilinks become real hyperlinks
    by_stem = {q.stem: q for q in load_all_pages()}   # resolve related GLO/DM targets
    pages = sorted(load_folder("stakeholders"), key=lambda x: x.id)
    _REL_MAX = 6               # cap chips per row; rest is one click away on the detail page
    rows = []
    for p in pages:
        # related glossary terms & data models the stakeholder points at — quick links
        # to "additional info" (the snapshot's inline links + `related:`), GLO before DM.
        rel = []
        for s in sorted(set(p.link_targets())):
            q = by_stem.get(s)
            if q and _type_of(s) in ("GLO", "DM"):
                rel.append({"id": q.id, "label": q.title, "type": _type_of(s),
                            "url": f"/page/{q.folder}/{s}"})
        rel.sort(key=lambda r: (r["type"] != "GLO", r["id"]))   # GLO first, then by id
        rows.append({
            "id": p.id,
            "stem": p.stem,
            "title": p.title,
            "role": p.meta.get("role", ""),
            "snapshot": extract_labeled(p, "Snapshot", titles, links),
            "influence": p.meta.get("influence", ""),
            "interest": p.meta.get("interest", ""),
            "rel_links": rel[:_REL_MAX],
            "rel_more": max(0, len(rel) - _REL_MAX),
            "status": p.status,
        })
    return render_template("stakeholders.html", rows=rows, total=len(rows))


@app.route("/adrs")
def adrs_view():
    items = load_adrs()
    # Fixed state buckets for the filter bar; anything that is not accepted /
    # rejected / deprecated (proposed, superseded, unknown, …) falls under "other".
    primary = ["accepted", "rejected", "deprecated"]
    labels = {"accepted": "Accepted", "rejected": "Rejected",
              "deprecated": "Deprecated", "other": "Andere"}
    tally = {k: 0 for k in primary}
    other = 0
    for a in items:
        if a["status"] in tally:
            tally[a["status"]] += 1
        else:
            other += 1
    buckets = [{"key": k, "label": labels[k], "count": tally[k]} for k in primary]
    buckets.append({"key": "other", "label": labels["other"], "count": other})
    return render_template("adrs.html", items=items, total=len(items), buckets=buckets)


@app.route("/page/<folder>/<stem>")
def page_detail(folder, stem):
    """Detail page for a single content unit (any wiki page, or an ADR when
    folder == 'adr'). Search results link here."""
    titles = title_index()
    if folder == "adr":
        for a in load_adrs():
            if a["stem"] == stem:
                # drop the body's leading "# ADR-…" heading; the page header shows it
                body_html = re.sub(r"<h1>.*?</h1>", "", a["html"], count=1, flags=re.DOTALL)
                return render_template(
                    "detail.html", kind="ADR", id=a["id"], title=a["title"],
                    status=a["status"], created="", updated=a["date"],
                    tags=[], body_html=body_html, crumb="ADRs", crumb_href="/adrs",
                    context_diagram=None, needs_mermaid="language-mermaid" in body_html,
                )
        abort(404)

    # FRs have their own rich page (full text + hierarchy breakdown) under the
    # functional-requirements/ path; send any /page link there so the whole
    # hierarchy stays on one route.
    if folder == "functional-requirements":
        return redirect(f"/functional-requirements/{stem}", code=302)

    path = WIKI_DIR / folder / f"{stem}.md"
    page = _parse(path, folder) if path.is_file() else None
    if not page:
        abort(404)
    kind = FOLDER_LABELS.get(folder, folder)
    # drop the leading "# Title" heading from the body — shown in the page header
    body = re.sub(r"^\s*#\s+.*(?:\n|$)", "", page.body, count=1)
    body_html = render_markdown(body, titles)
    # context pages carry the system-context diagram, projected live (ADR-0013)
    context_diagram = build_context_diagram() if folder == "context" else None
    # glossary pages carry a focused ego-graph snippet above the definition (ADR-0023)
    ego_graph = build_glossary_ego_graph(stem) if folder == "glossary" else None
    ego_layers = None
    if ego_graph:
        c = ego_graph["layer_counts"]
        ego_layers = [{"key": k, "label": l} for k, l in
                      (("DM", "Datenmodell"), ("STK", "Stakeholder"), ("GOAL", "Ziele"))
                      if c.get(k)]
        for L in ego_layers:
            L["count"] = c[L["key"]]
    return render_template(
        "detail.html", kind=kind, id=page.id, title=page.title,
        status=page.status, created=str(page.meta.get("created", "")),
        updated=str(page.meta.get("updated", "")), tags=page.meta.get("tags") or [],
        body_html=body_html, crumb="Suche", crumb_href="/search",
        context_diagram=context_diagram, relations=build_relations_panel(stem),
        ego_graph=ego_graph, ego_layers=ego_layers,
        needs_mermaid=bool(context_diagram) or "language-mermaid" in body_html,
    )


@app.route("/search")
def search_view():
    """Global search across all wiki content + ADRs. Results render once and are
    filtered incrementally client-side; type facets allow browsing by content type."""
    records = build_search_records()
    tally: dict[str, int] = {}
    for r in records:
        tally[r["type"]] = tally.get(r["type"], 0) + 1
    facets = sorted(tally.items(), key=lambda kv: (-kv[1], kv[0]))
    return render_template("search.html", records=records, total=len(records), facets=facets)


def _short_title(p: Page) -> str:
    """Concise label for diagram nodes / tile rows. `short_title:` frontmatter
    field wins; falls back to the full title. Defined per goal so the same label
    is used everywhere a compact form is needed."""
    return str(p.meta.get("short_title") or p.title).strip()


def _mermaid_goal_tree(vision: Page, objectives: list[Page]) -> str | None:
    """Project the Vision→Objectives tree from `parent:` edges (ADR-0018 style).
    Top-down, short-name nodes; clicking a goal jumps to its anchor below.
    Default `useMaxWidth: true` so the SVG fits the container at typical
    desktop widths (≥1000 px) without horizontal scrolling."""
    if not vision or not objectives:
        return None
    lines = ["graph TD", '  V["Vision Aquarius"]:::vision']
    for o in objectives:
        nid = _diagram_node_id(o.id)
        label = _clean_label(_short_title(o))
        lines.append(f'  V --> {nid}["{o.id}<br/>{label}"]:::goal')
        # absolute target so the same diagram works on /goals (in-page anchor)
        # and on /req42 (cross-page navigation to the matching goal card)
        lines.append(f'  click {nid} "/goals#{o.id}"')
    lines += [
        "  classDef vision fill:#2f6fb3,stroke:#7fc0ff,color:#ffffff,stroke-width:2px,font-weight:bold;",
        "  classDef goal fill:#d7dbe3,stroke:#9aa3b2,color:#15202e;",
    ]
    return "\n".join(lines)


# --- data model projection (req42 block 05: Unterstützende Modelle) -------
#
# Test-stage: edges are listed here as constants and projected to mermaid
# classDiagram. Once the relationship syntax inside each DM body (`- field :
# n:1 → [[DM-…]], optional` …) is stable enough to parse reliably, replace
# DM_EDGES with a live extractor from wiki/data-models/.
#
# Source of truth (until then): wiki/data-models/DM-001..DM-013.md.

DM_ENTITIES = [
    "Verein", "Saison", "Schwimmbad", "Figur", "Kind", "Sportverband",
    "Wettkampf", "Anmeldung", "Station", "Gruppe", "Durchgang", "Start", "Wertung",
]

# (source, target, kind, label)
# kind ∈ {"n:1", "n:1-opt", "m:n"} — n:1-opt is the same as n:1 but with the
# target side "0..1" instead of "1" (target reference is optional on the source).
DM_EDGES = [
    ("Kind", "Verein", "n:1-opt", "verein"),
    ("Kind", "Sportverband", "n:1-opt", "verband"),
    ("Wettkampf", "Saison", "n:1", "saison"),
    ("Wettkampf", "Schwimmbad", "n:1", "schwimmbad"),
    ("Wettkampf", "Figur", "m:n", "figuren"),
    ("Anmeldung", "Kind", "n:1", "kind"),
    ("Anmeldung", "Wettkampf", "n:1", "wettkampf"),
    ("Anmeldung", "Figur", "m:n", "figuren"),
    ("Anmeldung", "Gruppe", "n:1-opt", "gruppe"),
    ("Station", "Wettkampf", "n:1", "wettkampf"),
    ("Gruppe", "Wettkampf", "n:1", "wettkampf"),
    ("Durchgang", "Gruppe", "n:1", "gruppe"),
    ("Durchgang", "Station", "n:1", "station"),
    ("Durchgang", "Figur", "n:1", "figur"),
    ("Start", "Anmeldung", "n:1", "anmeldung"),
    ("Start", "Durchgang", "n:1", "durchgang"),
    ("Wertung", "Start", "n:1", "start"),
]


def _mermaid_dm_edge(src: str, tgt: str, kind: str, label: str) -> str:
    if kind == "m:n":
        return f'  {src} "1..n" -- "1..n" {tgt} : {label}'
    if kind == "n:1-opt":
        return f'  {src} "0..n" --> "0..1" {tgt} : {label}'
    return f'  {src} "0..n" --> "1" {tgt} : {label}'


def build_data_model_full_diagram() -> str:
    """Project the full DM class diagram (all entities + relationships)
    from DM_ENTITIES / DM_EDGES into a mermaid classDiagram string."""
    lines = ["classDiagram"]
    for name in DM_ENTITIES:
        lines.append(f"  class {name}")
    lines.append("")
    for src, tgt, kind, label in DM_EDGES:
        lines.append(_mermaid_dm_edge(src, tgt, kind, label))
    return "\n".join(lines)


def build_data_model_kind_diagram() -> str:
    """Kind-centric mini diagram for the index tile: Kind plus its three
    immediate neighbours (Verein, Sportverband, Anmeldung). Stays small
    enough to fit a tile without scrolling."""
    lines = [
        "classDiagram",
        "  direction LR",
        "  class Verein",
        "  class Sportverband",
        "  class Kind",
        "  class Anmeldung",
        '  Kind "0..n" --> "0..1" Verein',
        '  Kind "0..n" --> "0..1" Sportverband',
        '  Anmeldung "0..n" --> "1" Kind',
    ]
    return "\n".join(lines)


# Section/callout extractors for the /data-model catalog: each DM page is
# rendered as bold-led sections (**Purpose.**, **Attributes.**, **Relationships.**,
# **Invariants / rules.** …) plus 0..n `> [!note] X` callouts (Open points,
# Bewusst weggelassen). Order from the file is preserved so the on-page detail
# reads the same as the markdown source.

_DM_SECTION_RE = re.compile(
    r"^\*\*(?P<label>[^*\n]+?)\.\*\*\s*\n?(?P<body>.*?)"
    r"(?=^\*\*[^*\n]+?\.\*\*|^>\s*\[!|^##\s|\Z)",
    re.DOTALL | re.MULTILINE,
)

_DM_NOTE_RE = re.compile(
    r"^>\s*\[!note\]\s*(?P<title>[^\n]+)\n(?P<body>(?:^>.*\n?)+)",
    re.MULTILINE,
)

_DM_ATTRIBUTES_BLOCK_RE = re.compile(
    r"\*\*Attributes\.\*\*\s*\n(?P<body>.+?)"
    r"(?=^\*\*[A-Za-zÄÖÜäöü][^*\n]+?\.\*\*|^>\s*\[!|^##\s|\Z)",
    re.DOTALL | re.MULTILINE,
)
_DM_ATTR_BULLET_RE = re.compile(
    r"^\s*-\s+`(?P<name>[a-zA-Z][a-zA-Z0-9_]*)`", re.MULTILINE,
)


def _extract_dm_attribute_names(page: Page) -> list[str]:
    """Just the attribute *names* from the `**Attributes.**` bullet list — used
    for the compact summary table at the top of /data-model; the per-entity
    cards below carry types, modality, and prose."""
    m = _DM_ATTRIBUTES_BLOCK_RE.search(page.body)
    if not m:
        return []
    return _DM_ATTR_BULLET_RE.findall(m.group("body"))


def _extract_dm_sections(page: Page, titles: dict[str, str]) -> list[tuple[str, str]]:
    """`(label, rendered-html)` pairs for every `**Label.**` section in a DM body,
    in source order. Bullets / inline code are preserved by routing the section
    body back through `render_markdown`."""
    out = []
    for m in _DM_SECTION_RE.finditer(page.body):
        label = m.group("label").strip()
        body = m.group("body").rstrip()
        out.append((label, render_markdown(body, titles)))
    return out


def _extract_dm_notes(page: Page, titles: dict[str, str]) -> list[dict]:
    """`> [!note] Title` callouts as `{title, html}` records. Quote markers
    (`> `) are stripped before the body is re-rendered as markdown."""
    out = []
    for m in _DM_NOTE_RE.finditer(page.body):
        title = m.group("title").strip()
        body_lines = m.group("body").splitlines()
        cleaned = "\n".join(re.sub(r"^>\s?", "", line) for line in body_lines).strip()
        out.append({"title": title, "html": render_markdown(cleaned, titles)})
    return out


def data_model_entities() -> list[dict]:
    """One record per data-model page with its sections + notes ready to render —
    the per-entity catalog rendered below the projection diagram on /data-model."""
    titles = title_index()
    pages = sorted(load_folder("data-models"), key=lambda p: p.id)
    out = []
    for p in pages:
        out.append({
            "id": p.id,
            "stem": p.stem,
            "title": p.title,
            "stereotype": str(p.meta.get("stereotype") or "").strip(),
            "source_of_truth": str(p.meta.get("source-of-truth") or "").strip(),
            "attributes": _extract_dm_attribute_names(p),
            "sections": _extract_dm_sections(p, titles),
            "notes": _extract_dm_notes(p, titles),
        })
    return out


# Block 05 collapses the underlying entity pages (data-models/, use-cases/,
# activity-models/) into one row per *model type*. Each row links to its own
# overview page; types with no content yet are skipped from the listing.
SUPPORTING_MODEL_TYPES = [
    {"folder": "data-models", "label": "Datenmodell", "code": "DM", "href": "/data-model"},
    {"folder": "use-cases", "label": "Use Cases", "code": "UC", "href": None},
    {"folder": "activity-models", "label": "Aktivitätsmodelle", "code": "AM", "href": None},
]


def _supporting_model_entries() -> list[dict]:
    """One row per *populated* supporting-model type, for block 05's sample
    list. Empty types are skipped (they re-appear once their first page is
    written)."""
    out = []
    for m in SUPPORTING_MODEL_TYPES:
        n = len(load_folder(m["folder"]))
        if n == 0:
            continue
        out.append({
            "id": m["code"],
            "title": m["label"],
            "type": f"{n} Einträge",
            "status": "",
            "relations": n,
            "href": m["href"],
        })
    return out


def _epic_label(fr_id: str) -> str:
    """FR-001 → Epic-01 — display alias for the coverage-matrix column header.
    The underlying id stays FR-NNN (linking, frontmatter, search); this is
    purely cosmetic for the matrix."""
    m = re.match(r"FR-?0*(\d+)", fr_id)
    return f"Epic-{int(m.group(1)):02d}" if m else fr_id


@app.route("/goals")
def goals_view():
    """req42 Block 01 — Vision + Teilziele. Three sections top-down:
    Mermaid tree, full-text cards (vision then objectives), Goal-Coverage-Matrix.
    Goal↔Epic edges are read from each FR's `goal:` field (ADR-0018)."""
    titles = title_index()
    links = link_index()       # vision/objective prose wikilinks become real links
    data = load_goals()
    vision, objectives = data["vision"], data["objectives"]
    if not vision:
        abort(404)

    def _wikilink_list(items) -> list[str]:
        """Render a frontmatter list of '[[X]]' refs as human-readable labels."""
        out = []
        for x in (items or []):
            s = str(x).strip()
            m = re.match(r"\[\[([^\]\|]+)(?:\|([^\]]+))?\]\]", s)
            if not m:
                continue
            target, alias = m.group(1).strip(), m.group(2)
            base = target.split("/")[-1]
            out.append(alias.strip() if alias else titles.get(base, base))
        return out

    vision_narrative = _vision_full_paragraph(vision, titles, links)
    vision_card = {
        "id": vision.id,
        "title": vision.title,
        "stereotype": "Vision",
        "maturity": None,
        "beneficiary": _wikilink_list(vision.meta.get("beneficiary")),
        # Vision card shows just the Moore-style narrative paragraph — the
        # Teilziele list and Wirkung block from the wiki page are projected
        # below as separate objective cards and the coverage matrix.
        "html": f"<p>{vision_narrative}</p>" if vision_narrative else "",
    }

    coverage = data["coverage"]
    def _inline(s) -> str:
        """Frontmatter strings may contain `[[wikilinks]]` — render them as
        real hyperlinks when the target resolves."""
        return render_wikilinks(str(s or "").strip(), titles, links)

    objective_cards = []
    for o in objectives:
        objective_cards.append({
            "id": o.id,
            "title": o.title,
            "stereotype": "Ziel",
            "purpose": extract_pam_bullet(o, "Purpose", titles, links),
            "advantage": extract_pam_bullet(o, "Advantage", titles, links),
            "metric": _inline(o.meta.get("metric")),
            "target": _inline(o.meta.get("target")),
            "baseline": _inline(o.meta.get("baseline")),
            "beneficiary": _wikilink_list(o.meta.get("beneficiary")),
            "epics": [{"id": fr.id, "title": fr.title, "stem": fr.stem}
                      for fr in coverage.get(o.id, [])],
        })

    # matrix: rows = objectives in Wertkette order; columns = FR-001..N + enablers
    enabler_ids = {fr.id for fr in data["enablers"]}
    fr_cols = [{"id": fr.id, "title": fr.title, "epic": _epic_label(fr.id),
                "stem": fr.stem, "enabler": fr.id in enabler_ids}
               for fr in data["frs"]]
    matrix_rows = []
    for o in objectives:
        covered_ids = {fr.id for fr in coverage.get(o.id, [])}
        matrix_rows.append({
            "id": o.id, "title": o.title,
            "cells": [(col["id"] in covered_ids) for col in fr_cols],
        })

    diagram = _mermaid_goal_tree(vision, objectives)
    return render_template(
        "goals.html",
        diagram=diagram,
        vision=vision_card,
        objectives=objective_cards,
        fr_cols=fr_cols,
        matrix_rows=matrix_rows,
        needs_mermaid=bool(diagram),
    )


@app.route("/data-model")
def data_model_view():
    """req42 block 05 — Datenmodell: full class diagram of all DM entities
    (projected from DM_EDGES; hardcoded test-stage) plus the per-entity
    catalog below — every section + callout block from every DM page so the
    full data-model documentation lives on one page."""
    diagram = build_data_model_full_diagram()
    entities = data_model_entities()
    return render_template("data_model.html", diagram=diagram,
                           entities=entities, needs_mermaid=True)


@app.route("/req42")
def req42_view():
    """The req42 schema overview: every building block as a section, each with
    its first few entries and a link to the full list. Block 01 carries the
    Vision→Objectives diagram instead of a sample list (see build_req42_blocks)."""
    blocks = build_req42_blocks(sample=5)
    needs_mermaid = any(b.get("diagram") for b in blocks)
    return render_template("req42.html", blocks=blocks, needs_mermaid=needs_mermaid)


@app.route("/req42/backlog")
def backlog_view():
    """req42 block 04 — Product Backlog as the Epic→Feature→Story hierarchy.
    A dedicated rich view for the `backlog` slug (the other /req42/<slug> blocks
    use the generic list). Flask matches this static rule ahead of the dynamic
    /req42/<slug>. Doubles as the home `backlog` tile's click-target."""
    backlog = build_backlog()
    diagram = _mermaid_goal_epic_tree(load_goals(), backlog)
    block = REQ42_BY_SLUG.get("backlog")
    return render_template(
        "backlog.html", backlog=backlog, diagram=diagram,
        block=block, needs_mermaid=bool(diagram),
    )


@app.route("/functional-requirements/<stem>")
def fr_view(stem):
    """Rich detail page for one functional requirement of any stereotype
    (epic/feature/story), mirroring the wiki/functional-requirements/ folder.
    Shows the FR's full text plus — for non-leaf FRs — its own Feature→Story
    breakdown (mermaid + cards). Every FR node in the backlog diagrams clicks
    here, so the whole hierarchy lives under one sprechenden path with a
    'Product Backlog' breadcrumb (instead of the generic /page 'Suche' crumb).
    404 if `stem` is not an FR page."""
    path = WIKI_DIR / "functional-requirements" / f"{stem}.md"
    page = _parse(path, "functional-requirements") if path.is_file() else None
    if not page:
        abort(404)
    titles = title_index()
    body = re.sub(r"^\s*#\s+.*(?:\n|$)", "", page.body, count=1)  # drop leading "# Title"
    body_html = render_markdown(body, titles)

    backlog = build_backlog()
    node, kind = _backlog_node(backlog, stem)
    fr = {
        "id": page.id, "title": page.title, "stem": stem,
        "stereotype": kind or _fr_stereotype(page) or "story",
        "priority": str(page.meta.get("priority") or "").strip(),
        "release": str(page.meta.get("release") or "").strip(),
        "status": page.status,
        "features": (node or {}).get("features") or [],
        "direct_stories": (node or {}).get("direct_stories") or [],
        "stories": (node or {}).get("stories") or [],
    }
    fr["n_features"] = len(fr["features"])
    fr["n_stories"] = (node or {}).get("n_stories")
    if fr["n_stories"] is None:  # feature/story carry no precomputed count
        fr["n_stories"] = len(fr["stories"])

    diagram = _mermaid_fr_subtree(node)
    return render_template(
        "fr.html", fr=fr, body_html=body_html, diagram=diagram,
        ancestors=_fr_ancestors(stem),
        needs_mermaid=bool(diagram) or "language-mermaid" in body_html,
    )


@app.route("/req42/<slug>")
def req42_block_view(slug):
    """All entries of one req42 block, for blocks without their own rich view."""
    block = REQ42_BY_SLUG.get(slug)
    if not block:
        abort(404)
    rows = [
        {"id": p.id, "type": FOLDER_LABELS.get(p.folder, p.folder),
         "title": p.title, "status": p.status, "relations": len(p.link_targets())}
        for p in _block_pages(block)
    ]
    # the Scope block (03) shows the same live-projected system-context diagram
    context_diagram = build_context_diagram() if slug == "scope" else None
    return render_template(
        "req42_block.html", block=block, rows=rows, total=len(rows),
        context_diagram=context_diagram, needs_mermaid=bool(context_diagram),
    )


# ---------------------------------------------------------------------------
# Server-Lebenszyklus: Selbstabschaltung, sobald kein Browser mehr zusieht.
# KEIN Stop-Knopf — „Tab/Fenster schließen" ist das Beenden.
#
# Jede offene Seite schickt einen leichten Heartbeat (`POST /ping`) alle paar
# Sekunden. Solange Pings ankommen, läuft der Server; bleiben sie aus, fährt der
# Watchdog nach einer Schonfrist herunter — ein geschlossenes Browserfenster
# hinterlässt so keinen verwaisten Container. Zusätzlich meldet die Seite per
# pagehide-Beacon `POST /leaving`, dass sie verschwindet: ist es nur Navigation,
# hebt der /ping der Folgeseite das Signal sofort auf; ist der Tab wirklich zu,
# stoppt der Server schon nach `_LEAVE_GRACE` (~5 s) statt erst nach der
# Heartbeat-Schonfrist. So genügt das Schließen des Tabs zum Beenden.
#
# Bewusst KEINE dauerhaft offene Verbindung (eine frühere Iteration nutzte einen
# SSE-/events-Stream): die belegte je Tab einen Worker-Thread für ihre gesamte
# Lebensdauer, und beim Klicken durch Unterseiten stauten sich diese, bis der
# Threadpool erschöpft war und sogar /stop nicht mehr bedient wurde. Ein /ping
# ist dagegen ein Sofort-Request, der keinen Thread hält — das Problem entfällt
# damit ganz. Die Schonfrist ist großzügig, damit ein im Hintergrund gedrosselter
# Tab (Browser drosseln Timer auf ~1×/min) am Leben bleibt; nur ein wirklich
# geschlossener Tab pingt gar nicht mehr. Ein einziger Worker hält den Zustand
# prozess-kohärent (Dockerfile: --workers 1). Siehe ADR-0022.
# ---------------------------------------------------------------------------


def _grace(env_name: str, default: float) -> float:
    """Schonfrist in Sekunden, per Env überschreibbar (für Tests/Tuning)."""
    try:
        return float(os.environ.get(env_name, default))
    except (TypeError, ValueError):
        return default


# Ohne Heartbeat länger als dies → herunterfahren. Größer als das Browser-
# Hintergrund-Throttling (~60 s), damit ein nur versteckter Tab nicht fälschlich
# abschaltet; nur ein wirklich geschlossener Tab pingt gar nicht mehr.
_HEARTBEAT_GRACE = _grace("DASH_HEARTBEAT_GRACE", 90.0)
# Schonfrist beim Start, bis der erste Heartbeat kommt (langsamer erster Build/
# erstes Rendern). Kommt nie einer, fährt der Server danach herunter, statt als
# Waise weiterzulaufen.
_STARTUP_GRACE = _grace("DASH_STARTUP_GRACE", 90.0)
# Kurze Frist nach einem „Tab verlässt"-Signal (`/leaving`, per pagehide-Beacon),
# bevor heruntergefahren wird. Beim Navigieren verbindet die nächste Seite sofort
# wieder (`/ping` hebt das Signal auf); bleibt sie aus (Tab geschlossen), stoppt
# der Server nach dieser Frist — viel schneller als die Heartbeat-Schonfrist.
_LEAVE_GRACE = _grace("DASH_LEAVE_GRACE", 5.0)

_lifecycle_lock = threading.Lock()
_last_seen = None        # monotone Zeit des letzten /ping; None = noch keiner
_leave_at = None         # monotone Zeit eines „Tab verlässt"-Signals; None = keins
_shutting_down = False
_watchdog_started = False


def _shutdown(reason):
    """Server sauber beenden. Unter gunicorn wird der Master (unser Parent)
    per SIGTERM beendet, sodass alle Worker aussteigen und PID 1 des Containers
    zurückkehrt — mit `restart: no` bleibt der Container dann unten. Unter dem
    Dev-Server beenden wir nur uns selbst (NICHT den Parent — das ist die Shell)
    per SIGTERM: ein aus einem Hintergrund-Thread an den eigenen Prozess
    gesendetes SIGINT verschluckt der Werkzeug-Dev-Server (Werkzeug 3.x), SIGTERM
    greift dagegen über die Default-Signal-Aktion zuverlässig."""
    global _shutting_down
    with _lifecycle_lock:
        if _shutting_down:
            return
        _shutting_down = True
    app.logger.info("dashboard shutdown: %s", reason)

    def _terminate():
        time.sleep(0.4)  # HTTP-Antwort / Beacon erst flushen lassen
        if app.config.get("DEV_SERVER"):
            os.kill(os.getpid(), signal.SIGTERM)
            return
        try:
            os.kill(os.getppid(), signal.SIGTERM)  # gunicorn-Master
        except (ProcessLookupError, PermissionError):
            pass
        os.kill(os.getpid(), signal.SIGTERM)

    threading.Thread(target=_terminate, daemon=True).start()


def _watchdog():
    started = time.monotonic()
    while True:
        time.sleep(1.0)
        with _lifecycle_lock:
            if _shutting_down:
                return
            last = _last_seen
            leave = _leave_at
        now = time.monotonic()
        # Tab hat sich verabschiedet und keine neue Seite hat seither gepingt:
        # nach kurzer Frist herunterfahren (schnelles Stop bei Tab-Schließen).
        if leave is not None and (last is None or last <= leave) and now - leave > _LEAVE_GRACE:
            _shutdown("Tab geschlossen (kein Reconnect nach pagehide)")
            return
        if last is None:
            # Es hat noch nie jemand gepingt → Start-Schonfrist.
            if now - started > _STARTUP_GRACE:
                _shutdown("kein Browser-Heartbeat innerhalb der Start-Schonfrist")
                return
        elif now - last > _HEARTBEAT_GRACE:
            _shutdown("kein Browser-Heartbeat mehr (Tab geschlossen)")
            return


def _ensure_watchdog():
    global _watchdog_started
    with _lifecycle_lock:
        if _watchdog_started:
            return
        _watchdog_started = True
    threading.Thread(target=_watchdog, daemon=True).start()


@app.route("/ping", methods=["POST"])
def heartbeat_ping():
    """Leichtes Lebenszeichen jeder offenen Seite. Aktualisiert den `last seen`-
    Zeitstempel, hebt ein offenes „Tab verlässt"-Signal auf (eine lebende Seite
    pingt → kein Abschied) und kehrt sofort zurück — hält keinen Thread."""
    global _last_seen, _leave_at
    _ensure_watchdog()
    with _lifecycle_lock:
        _last_seen = time.monotonic()
        _leave_at = None
    return ("", 204)


@app.route("/leaving", methods=["POST"])
def heartbeat_leaving():
    """Beacon beim Verlassen der Seite (pagehide: Tab geschlossen ODER navigiert).
    Setzt eine kurze Abschaltfrist; navigiert der Nutzer nur, hebt der sofortige
    `/ping` der Folgeseite das Signal wieder auf, bevor die Frist abläuft."""
    global _leave_at
    _ensure_watchdog()
    with _lifecycle_lock:
        _leave_at = time.monotonic()
    return ("", 204)


# Watchdog beim Import starten (im gunicorn-Worker bzw. Dev-Prozess), damit die
# Start-Schonfrist auch greift, falls nie ein /ping eintrifft.
_ensure_watchdog()


if __name__ == "__main__":
    app.config["DEV_SERVER"] = True
    app.run(host="0.0.0.0", port=8000, threaded=True)
