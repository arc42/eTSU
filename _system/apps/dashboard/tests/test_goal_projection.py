"""Goals are projected from the vault, never from a hardcoded ID list — no pytest.

The regression this guards: `load_goals()` used to read a module constant
`GOAL_VALUE_CHAIN = ["GOAL-002".."GOAL-005"]`, inherited from the demo vault it
was extracted from. That capped every vault at four objectives, at exactly those
IDs. A fifth objective — and any epic whose only `goal:` pointed at it — vanished
from `/goals`, the goal tree, the Vision tile, the backlog map and the coverage
matrix, while the req42 tile on the same screen still counted them. No error
anywhere: the page simply rendered fewer goals than the vault holds.

This suite therefore builds a vault with FIVE objectives (GOAL-002..GOAL-006)
plus an epic that contributes only to the fifth, and asserts all of them reach
the rendered HTML. It also pins the two rules that replaced the ID list:
the vision is the page with `stereotype: vision` (not "whatever is GOAL-001"),
and every other goal page is an objective.

Run from the dashboard dir:
    .venv/bin/python tests/test_goal_projection.py
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
(_tmp / "wiki.yaml").write_text("system_name: System X\n", encoding="utf-8")
os.environ["WIKI_DIR"] = str(_wiki)
os.environ["ADR_DIR"] = str(_tmp / "adr")
os.environ["WIKI_CONFIG"] = str(_tmp / "wiki.yaml")
# without a browser heartbeat the watchdog SIGTERMs this process (ADR-0022)
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402

_GOALS = _wiki / "goals"
_FRS = _wiki / "functional-requirements"

# The vision. Note the id is deliberately NOT GOAL-001 in one of the tests
# below; here it is, matching bootstrap.md step 3.
_GOALS.joinpath("GOAL-001-system-x.md").write_text("""---
id: GOAL-001
type: goal
title: System X Runs Itself
status: accepted
created: 2026-09-06
updated: 2026-09-06
sources: []
related: []
tags: [goal]
stereotype: vision
parent: []
beneficiary: []
metric:
baseline:
target:
horizon:
tile_claim: System X, without the paperwork.
---

# System X Runs Itself

## Vision

For **Role B**, who need Entity A handled without paperwork, **System X** is a
**platform** that does the bookkeeping for them.
""", encoding="utf-8")

# FIVE objectives — one more than the retired GOAL_VALUE_CHAIN allowed.
for _n in ("002", "003", "004", "005", "006"):
    _GOALS.joinpath(f"GOAL-{_n}-objective-{_n}.md").write_text(f"""---
id: GOAL-{_n}
type: goal
title: Objective {_n}
status: accepted
created: 2026-09-06
updated: 2026-09-06
sources: []
related: []
tags: [goal]
stereotype: objective
parent:
  - "[[GOAL-001-system-x]]"
beneficiary: []
metric: indicator {_n}
baseline: today
target: better
horizon:
---

# Objective {_n}

## Objective

- **Purpose.** Purpose of objective {_n}.
- **Advantage.** Advantage of objective {_n}.
- **Metric.** Indicator {_n}.
""", encoding="utf-8")

# An epic whose ONLY goal is the fifth objective — the page that used to vanish.
_FRS.joinpath("FR-001-sixth-goal-epic.md").write_text("""---
id: FR-001
type: functional-requirement
title: Sixth Goal Epic
status: accepted
created: 2026-09-06
updated: 2026-09-06
sources: []
related: []
tags: [functional-requirement]
stereotype: epic
parent: []
priority: Must
release: v1
lane: backbone
order: 1
goal:
  - "[[GOAL-006-objective-006]]"
---

# Sixth Goal Epic

An epic that contributes only to GOAL-006.
""", encoding="utf-8")

ALL_OBJECTIVES = ["GOAL-002", "GOAL-003", "GOAL-004", "GOAL-005", "GOAL-006"]


def test_every_objective_page_is_projected():
    with app.app.app_context():
        data = app.load_goals()
    assert data["vision"] is not None, "no vision found"
    assert data["vision"].id == "GOAL-001", data["vision"].id
    ids = [p.id for p in data["objectives"]]
    assert ids == ALL_OBJECTIVES, ids


def test_coverage_reaches_the_fifth_objective():
    with app.app.app_context():
        data = app.load_goals()
    covered = {gid: [p.id for p in frs] for gid, frs in data["coverage"].items()}
    assert set(covered) == set(ALL_OBJECTIVES), sorted(covered)
    assert covered["GOAL-006"] == ["FR-001"], covered
    # an epic that names a goal is not an enabler
    assert [p.id for p in data["enablers"]] == [], data["enablers"]


def test_goals_page_renders_all_objectives_and_the_late_epic():
    body = app.app.test_client().get("/goals").get_data(as_text=True)
    for gid in ALL_OBJECTIVES:
        assert gid in body, f"{gid} missing from /goals"
    assert "FR-001" in body, "the GOAL-006 epic is missing from the coverage matrix"


def test_home_and_backlog_agree_with_the_vault():
    client = app.app.test_client()
    home = client.get("/").get_data(as_text=True)
    for gid in ALL_OBJECTIVES:
        assert gid in home, f"{gid} missing from the home Vision tile"
    backlog = client.get("/req42/backlog").get_data(as_text=True)
    assert "GOAL-006" in backlog, "GOAL-006 missing from the backlog goal map"


def test_the_vision_is_chosen_by_stereotype_not_by_id():
    """A group whose GOAL-001 is an objective must not get it drawn as the
    vision — and it must still appear, as an objective."""
    demoted = _GOALS / "GOAL-001-system-x.md"
    original = demoted.read_text(encoding="utf-8")
    late_vision = _GOALS / "GOAL-009-late-vision.md"
    try:
        demoted.write_text(original.replace("stereotype: vision",
                                            "stereotype: objective"),
                           encoding="utf-8")
        late_vision.write_text(original.replace("GOAL-001", "GOAL-009")
                                       .replace("System X Runs Itself",
                                                "The Late Vision"),
                               encoding="utf-8")
        with app.app.app_context():
            data = app.load_goals()
        assert data["vision"].id == "GOAL-009", data["vision"].id
        ids = [p.id for p in data["objectives"]]
        assert ids == ["GOAL-001"] + ALL_OBJECTIVES, ids
        assert app.app.test_client().get("/goals").status_code == 200
    finally:
        demoted.write_text(original, encoding="utf-8")
        late_vision.unlink(missing_ok=True)


def test_a_vision_without_objectives_gets_the_objectives_empty_state():
    """The state bootstrap.md step 3 leaves behind: a vision captured, no
    objectives yet. /goals used to say "No goals yet" directly underneath the
    rendered vision; the fix reworded it, and nothing covered either state."""
    moved = []
    try:
        for f in sorted(_GOALS.glob("GOAL-00[23456]*.md")):
            moved.append((f, f.read_text(encoding="utf-8")))
            f.unlink()
        body = app.app.test_client().get("/goals").get_data(as_text=True)
        assert "No objectives yet" in body, \
            "a vision with no objectives does not get the objectives empty state"
        assert "No goals yet" not in body, \
            "/goals claims there are no goals while rendering the vision"
        assert "System X Runs Itself" in body, "the vision itself stopped rendering"
    finally:
        for f, text in moved:
            f.write_text(text, encoding="utf-8")


def test_the_goal_type_is_labelled_in_search():
    """FOLDER_LABELS had no entry for goals/, so the Goal type surfaced as the
    lowercase folder name `goals` in search results and facets."""
    assert app.FOLDER_LABELS["goals"] == "Goal", app.FOLDER_LABELS.get("goals")
    body = app.app.test_client().get("/search").get_data(as_text=True)
    assert '<span class="badge kind-badge">Goal</span>' in body, \
        "search results do not label goal pages 'Goal'"
    assert 'data-type="goals"' not in body, \
        "the raw folder name leaked into the search type filter"


def test_a_parenthesised_system_name_survives_into_the_diagrams():
    """`system_name: "Bookshelf (v2)"` used to show in full in the hero but as
    "Bookshelf" in every diagram — two names for one system on one screen."""
    cfg = Path(os.environ["WIKI_CONFIG"])
    original = cfg.read_text(encoding="utf-8")
    try:
        cfg.write_text('system_name: "System X (v2)"\n', encoding="utf-8")
        with app.app.app_context():
            data = app.load_goals()
            tree = app._mermaid_goal_tree(data["vision"], data["objectives"])
        assert "System X (v2)" in tree, tree.splitlines()[:2]
        # square brackets are mermaid node delimiters and must still go
        assert app._clean_label("Acme [Beta]") == "Acme Beta"
        assert app._clean_label("Member's card") == "Member's card"
    finally:
        cfg.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    test_every_objective_page_is_projected()
    test_coverage_reaches_the_fifth_objective()
    test_goals_page_renders_all_objectives_and_the_late_epic()
    test_home_and_backlog_agree_with_the_vault()
    test_the_vision_is_chosen_by_stereotype_not_by_id()
    test_a_vision_without_objectives_gets_the_objectives_empty_state()
    test_the_goal_type_is_labelled_in_search()
    test_a_parenthesised_system_name_survives_into_the_diagrams()
    print(f"OK: all {len(ALL_OBJECTIVES)} objectives projected from the vault")
