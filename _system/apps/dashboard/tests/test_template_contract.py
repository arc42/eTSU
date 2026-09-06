"""`_templates/` and `app.py` are two halves of one contract — no pytest.

Frontmatter keys, `TYPE-NNN` ID prefixes and body-structure markers are shared
between the template the agent writes from and the parser the dashboard reads
with. When they drift, nothing raises: Jinja renders Undefined as "", a regex
that matches nothing returns [], and the page comes up looking merely empty.
Three instances of exactly that were found in this repo:

  * `tile_claim:` was read by app.py and declared by no template, so the Vision
    tile's claim line was permanently blank;
  * `_templates/data-model.md` prescribed `- <name> : <type>` while the parser
    required the name in backticks, so /data-model's Attributes column was `—`
    for every entity while the cards below it showed them;
  * `_templates/activity-model.md` emits `ACT-NNN` while app.py's type maps
    said `AM`, so the relations panel showed the raw code `ACT` as a group
    heading and the `AM` entries were dead code.

This suite diffs the two halves instead of trusting a reader to notice.

Run from the dashboard dir:
    .venv/bin/python tests/test_template_contract.py
"""
import os
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
TEMPLATES = REPO / "_templates"

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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_KEY_RE = re.compile(r"^([a-zA-Z][a-zA-Z0-9_-]*)\s*:", re.MULTILINE)

# `SRC-` records live in raw/sources/, not in the wiki layer, so they carry no
# entry in the wiki type maps (ADR-0006).
NON_WIKI_PREFIXES = {"SRC"}


def _templates() -> list[Path]:
    files = sorted(TEMPLATES.glob("*.md"))
    assert files, f"no templates found under {TEMPLATES}"
    return files


def _frontmatter(path: Path) -> str:
    m = _FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
    assert m, f"{path.name} has no frontmatter block"
    return m.group(1)


def test_every_key_app_reads_is_declared_by_some_template():
    """The `tile_claim` failure class: app.py reads a key no template mentions,
    CLAUDE.md forbids the agent from inventing fields, so the read is dead."""
    declared: set[str] = set()
    for f in _templates():
        declared |= set(_KEY_RE.findall(_frontmatter(f)))
    source = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
    read = set(re.findall(r'\.meta\.get\(\s*"([^"]+)"', source))
    assert read, "found no .meta.get() reads — did app.py move?"
    undeclared = sorted(read - declared)
    assert not undeclared, \
        f"app.py reads frontmatter keys no template declares: {undeclared}"


def test_every_template_id_prefix_is_known_to_the_type_maps():
    """The `ACT` vs `AM` failure class: the prefix the template emits must be
    the prefix the parser maps to a folder and a human label."""
    for f in _templates():
        m = re.search(r"^id:\s*([A-Z]+)-", _frontmatter(f), re.MULTILINE)
        assert m, f"{f.name} declares no `id: TYPE-NNN`"
        prefix = m.group(1)
        if prefix in NON_WIKI_PREFIXES:
            continue
        assert prefix in app._TYPE_FOLDER, \
            f"{f.name} emits {prefix}- but _TYPE_FOLDER has no such key"
        assert prefix in app._TYPE_LABEL, \
            f"{f.name} emits {prefix}- but _TYPE_LABEL has no such key"
        assert prefix in app._REL_TYPE_ORDER, \
            f"{f.name} emits {prefix}- but _REL_TYPE_ORDER omits it"


def test_no_type_map_entry_is_dead():
    """The other half of the same check: a mapped prefix no template emits is a
    key that can never match a page."""
    emitted = set()
    for f in _templates():
        m = re.search(r"^id:\s*([A-Z]+)-", _frontmatter(f), re.MULTILINE)
        emitted.add(m.group(1))
    for name, keys in (("_TYPE_FOLDER", set(app._TYPE_FOLDER)),
                       ("_TYPE_LABEL", set(app._TYPE_LABEL)),
                       ("_REL_TYPE_ORDER", set(app._REL_TYPE_ORDER))):
        dead = sorted(keys - emitted)
        assert not dead, f"{name} maps prefixes no template emits: {dead}"
    codes = {m["code"] for m in app.SUPPORTING_MODEL_TYPES}
    assert codes <= emitted, \
        f"SUPPORTING_MODEL_TYPES uses codes no template emits: {sorted(codes - emitted)}"


def test_data_model_attribute_bullets_are_extractable():
    """`/data-model`'s "Entity types at a glance" reads attribute names off the
    `**Attributes.**` bullets. The template's own bullet shape must match."""
    tpl = (TEMPLATES / "data-model.md").read_text(encoding="utf-8")
    bullet = re.search(r"^- .*<name>.*$", tpl, re.MULTILINE)
    assert bullet, "data-model.md no longer prescribes an attribute bullet"
    line = (bullet.group(0)
            .replace("<name>", "entity_key")
            .replace("<type>", "string")
            .replace("<mandatory?>", "mandatory")
            .replace("<note>", "the key"))
    page = tpl.replace(bullet.group(0), line)
    page = (page.replace("DM-NNN", "DM-001")
                .replace("<Entity / value-object / sum-type name>", "Entity A")
                .replace("{{date}}", "2026-09-06")
                .replace("{{title}}", "Entity A"))
    target = _wiki / "data-models" / "DM-001-entity-a.md"
    target.write_text(page, encoding="utf-8")
    try:
        with app.app.app_context():
            dm = app.load_folder("data-models")[0]
            names = app._extract_dm_attribute_names(dm)
        assert names == ["entity_key"], \
            f"the template's own attribute bullet does not parse: {names}"
    finally:
        target.unlink()


def test_goal_template_body_markers_are_extractable():
    """`## Vision` (vision) and the `- **Purpose.**` / `- **Advantage.**`
    bullets (objective) are parsed out of the goal body for /goals and the
    home tile."""
    tpl = (TEMPLATES / "goal.md").read_text(encoding="utf-8")
    base = (tpl.replace("{{date}}", "2026-09-06")
               .replace("{{title}}", "System X Runs Itself")
               .replace("<Name>", "System X Runs Itself")
               .replace("<target group>", "Role B")
               .replace("<need / problem>", "need Entity A handled")
               .replace("<system>", "System X")
               .replace("<category>", "platform")
               .replace("<key benefit>", "does the bookkeeping")
               .replace("<the outcome sought, not an activity>", "The outcome.")
               .replace("<for whom (see `beneficiary:`), what concrete benefit — \"so what?\">",
                        "Role B saves time.")
               .replace("<the one indicator (see `metric:` / `baseline:` / `target:`)>",
                        "Indicator A."))
    vision = (base.replace("id: GOAL-NNN", "id: GOAL-001")
                  .replace("stereotype: objective", "stereotype: vision")
                  .replace("tile_claim:", "tile_claim: System X, without the paperwork."))
    objective = (base.replace("id: GOAL-NNN", "id: GOAL-002")
                     .replace("title: System X Runs Itself", "title: Objective A"))
    vp = _wiki / "goals" / "GOAL-001-system-x.md"
    op = _wiki / "goals" / "GOAL-002-objective-a.md"
    vp.write_text(vision, encoding="utf-8")
    op.write_text(objective, encoding="utf-8")
    try:
        with app.app.app_context():
            data = app.load_goals()
            titles = app.title_index()
            assert data["vision"] is not None, "the template's vision is not recognised"
            para = app._vision_full_paragraph(data["vision"], titles)
            assert "System X" in para, f"`## Vision` did not parse: {para!r}"
            tile = app.build_vision_tile(data, titles)
            assert tile["claim"].startswith("System X, without"), tile["claim"]
            obj = data["objectives"][0]
            for label in ("Purpose", "Advantage", "Metric"):
                got = app.extract_pam_bullet(obj, label, titles)
                assert got.strip(), f"`- **{label}.**` did not parse from the template"
    finally:
        vp.unlink()
        op.unlink()


if __name__ == "__main__":
    test_every_key_app_reads_is_declared_by_some_template()
    test_every_template_id_prefix_is_known_to_the_type_maps()
    test_no_type_map_entry_is_dead()
    test_data_model_attribute_bullets_are_extractable()
    test_goal_template_body_markers_are_extractable()
    print(f"OK: {len(_templates())} templates match the parser contract")
