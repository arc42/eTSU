"""Plain-assert test for build_glossary_ego_graph() — no pytest dependency.

The per-term ego snippet on a glossary detail page (ADR-0023): a 1-hop slice of
build_glossary_graph() around one focal term. Run like the sibling test:
    .venv/bin/python tests/test_glossary_ego_graph.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402


def test_ego_is_a_valid_1hop_slice():
    full = app.build_glossary_graph()
    full_ids = {n["data"]["id"] for n in full["nodes"]}

    # focal-term neighbours straight from the full edge set, for the oracle below
    def full_neighbours(stem):
        out = set()
        for e in full["edges"]:
            d = e["data"]
            if d["source"] == stem:
                out.add(d["target"])
            elif d["target"] == stem:
                out.add(d["source"])
        return out

    type_of = {n["data"]["id"]: n["data"]["type"] for n in full["nodes"]}

    checked = 0
    for stem in sorted(full_ids):
        if type_of[stem] != "GLO":
            continue
        ego = app.build_glossary_ego_graph(stem)
        assert ego is not None, stem
        ids = {n["data"]["id"] for n in ego["nodes"]}

        # focal node present, flagged, and the only one flagged
        assert stem in ids, stem
        focus = [n["data"]["id"] for n in ego["nodes"] if n["data"].get("focus")]
        assert focus == [stem], (stem, focus)

        # node set == focal + neighbours of type GLO/DM/STK/GOAL (1-hop, type-filtered)
        expected = {stem} | {n for n in full_neighbours(stem)
                             if type_of.get(n) in app._EGO_TYPES}
        assert ids == expected, (stem, ids ^ expected)
        assert all(type_of[i] in app._EGO_TYPES for i in ids), stem

        # induced subgraph: every edge stays inside the ego, no dangling endpoints
        for e in ego["edges"]:
            d = e["data"]
            assert d["source"] in ids and d["target"] in ids, (stem, d)

        # layer_counts == DM/STK/GOAL cross edges actually present in the slice
        tally = {}
        for e in ego["edges"]:
            d = e["data"]
            if d.get("cross") and d.get("ntype") in app._EGO_TYPES:
                tally[d["ntype"]] = tally.get(d["ntype"], 0) + 1
        assert ego["layer_counts"] == tally, (stem, ego["layer_counts"], tally)
        checked += 1

    assert checked, "no GLO terms found"

    # a non-glossary / unknown stem yields no snippet
    assert app.build_glossary_ego_graph("does-not-exist") is None

    # GLO-027 Familie: 0 glossary-internal edges, but its cross relations still surface
    fam = app.build_glossary_ego_graph("GLO-027-familie")
    assert fam is not None
    assert not any(e["data"].get("cross") is False for e in fam["edges"]), \
        "Familie has no GLO-GLO edge"
    assert fam["layer_counts"], "Familie's STK/GOAL relations should give buttons"

    print(f"OK: ego graphs valid for {checked} GLO terms; "
          f"Familie layers={fam['layer_counts']}")


if __name__ == "__main__":
    test_ego_is_a_valid_1hop_slice()
    print("all glossary-ego-graph tests passed")
