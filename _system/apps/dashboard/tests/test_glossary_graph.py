"""Plain-assert test for build_glossary_graph() — no pytest dependency.

Run from the dashboard dir inside a venv that has the app's requirements:
    python3 -m venv .venv
    .venv/bin/pip install -q -r requirements.txt
    .venv/bin/python tests/test_glossary_graph.py

WIKI_DIR is left unset so app.py falls back to the repo's wiki/ folder,
making today's real glossary the test oracle (ADR-0023).
"""
import sys
from pathlib import Path

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

    # --- stable facts about today's real glossary (ADR-0023 grilling) ---
    assert "GLO-027-familie" in by_id, "Familie term missing"
    assert by_id["GLO-027-familie"]["degree"] == 0, \
        "GLO-027 is the known orphan (no glossary-internal edges)"
    # the cross-type layers the buttons are built for
    for t in ("DM", "STK", "EIF", "GOAL"):
        assert t in g["layer_counts"], (t, g["layer_counts"])

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
