"""Plain-assert test for build_glossary_graph() — no pytest dependency.

Run from the dashboard dir inside a venv that has the app's requirements:
    python3 -m venv .venv
    .venv/bin/pip install -q -r requirements.txt
    .venv/bin/python tests/test_glossary_graph.py

WIKI_DIR points at tests/fixtures/wiki, a small neutral vault, so the suite is
independent of whatever content this starter is filled with.
"""
import os
import sys
from pathlib import Path

_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "wiki"
os.environ["WIKI_DIR"] = str(_FIXTURE)
os.environ["ADR_DIR"] = str(_FIXTURE.parent / "adr")
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402


def test_build_glossary_graph_shape_and_invariants():
    g = app.build_glossary_graph()
    nodes = [n["data"] for n in g["nodes"]]
    edges = [e["data"] for e in g["edges"]]
    by_id = {n["id"]: n for n in nodes}

    # --- cytoscape integrity: every edge endpoint is a real node ---
    for e in edges:
        assert e["source"] in by_id, e
        assert e["target"] in by_id, e
        assert e["source"] != e["target"], e            # no self-loops

    # --- edges are undirected & deduplicated (one per unordered pair) ---
    pairs = [frozenset((e["source"], e["target"])) for e in edges]
    assert len(pairs) == len(set(pairs)), "duplicate undirected edge"

    # --- node classes ---
    glo = [n for n in nodes if n["type"] == "GLO"]
    assert glo, "no glossary nodes"
    assert all(n["core"] for n in glo), "GLO nodes must be core"
    assert all(not n["core"] for n in nodes if n["type"] != "GLO"), \
        "non-GLO nodes must not be core"

    # every GLO node carries the projected display fields
    for n in glo:
        assert n["state"] in ("agreed", "draft", "deprecated"), n
        assert n["url"] == f"/page/glossary/{n['id']}", n
        assert isinstance(n["degree"], int)

    # default view = GLO-only: core nodes + non-cross edges form a closed graph
    core_ids = {n["id"] for n in glo}
    for e in edges:
        if not e["cross"]:
            assert e["source"] in core_ids and e["target"] in core_ids, e
        else:
            assert "ntype" in e, e
            assert by_id[e["target"]]["type"] == e["ntype"], e

    # degree == number of incident non-cross (GLO-GLO) edges
    deg = {n["id"]: 0 for n in glo}
    for e in edges:
        if not e["cross"]:
            deg[e["source"]] += 1
            deg[e["target"]] += 1
    for n in glo:
        assert n["degree"] == deg[n["id"]], (n["id"], n["degree"], deg[n["id"]])

    # layer_counts == per-type cross-edge tally
    tally = {}
    for e in edges:
        if e["cross"]:
            tally[e["ntype"]] = tally.get(e["ntype"], 0) + 1
    assert g["layer_counts"] == tally, (g["layer_counts"], tally)

    # --- stable facts about the fixture glossary ---
    assert "GLO-004-shelf" in by_id, "Shelf term missing"
    assert by_id["GLO-004-shelf"]["degree"] == 1, \
        "GLO-004-shelf has exactly one glossary-internal edge (to GLO-001-book)"
    # the cross-type layer the buttons are built for; the fixture only wires a
    # GLO -> STK edge (GLO-003-member -> STK-001-librarian), so DM/EIF/GOAL
    # layers are legitimately absent here (unlike the old, richer vault).
    assert "STK" in g["layer_counts"], g["layer_counts"]
    for t in ("DM", "EIF", "GOAL"):
        assert t not in g["layer_counts"], (t, g["layer_counts"])

    # coloured types (own button colour) must NOT carry the grey `rest` flag,
    # else the node[rest] style would override their colour (regression guard).
    named = {"DM", "STK", "EIF", "GOAL"}
    for n in nodes:
        if n["type"] == "GLO":
            assert "rest" not in n, n["id"]
        elif n["type"] in named:
            assert "rest" not in n, f"{n['id']} ({n['type']}) wrongly tagged rest"
        else:
            assert n.get("rest") == 1, f"{n['id']} ({n['type']}) should be rest"

    print(f"OK: {len(glo)} GLO nodes, {len(nodes)-len(glo)} neighbours, "
          f"{len(edges)} edges, layers={g['layer_counts']}")


if __name__ == "__main__":
    test_build_glossary_graph_shape_and_invariants()
    print("all glossary-graph tests passed")
