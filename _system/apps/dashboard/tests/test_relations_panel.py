"""Plain-assert test for build_relations_panel() — no pytest dependency.

    .venv/bin/python tests/test_relations_panel.py

WIKI_DIR unset → app.py falls back to the repo's wiki/, so the real link graph
is the oracle. Powers the detail-page 'Verweist auf' / 'Taucht auf in' section.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app  # noqa: E402


def _flat(groups):
    return [it for g in groups for it in g["links"]]


def test_relations_panel_outbound_inbound_and_dedup():
    with app.app.test_request_context("/"):
        rel = app.build_relations_panel("STK-009-offizieller")

    out = _flat(rel["outbound"])
    inb = _flat(rel["inbound"])
    out_ids = {i["id"] for i in out}
    inb_ids = {i["id"] for i in inb}

    # a link never appears in both buckets (inbound excludes outbound)
    assert not (out_ids & inb_ids), out_ids & inb_ids
    # never links to itself
    assert "STK-009" not in out_ids and "STK-009" not in inb_ids

    # outbound carries the glossary term + the concrete role stakeholders
    assert "GLO-007" in out_ids, "glossary term Offizieller missing from outbound"
    assert {"STK-002", "STK-003"} <= out_ids, "Kampf-/Punktrichter missing"
    # inbound surfaces where the role is used (functional requirements)
    assert any(i.startswith("FR-") for i in inb_ids), "no FR backlinks"

    # every link has a usable URL and a label
    for it in out + inb:
        assert it["url"].startswith(("/page/", "/functional-requirements/")), it
        assert it["label"], it
    # FR links route to the rich FR page, not the generic detail route
    for it in out + inb:
        if it["type"] == "FR":
            assert it["url"].startswith("/functional-requirements/"), it

    # groups are typed and ordered (GLO before ISS per _REL_TYPE_ORDER)
    types = [g["type"] for g in rel["outbound"]]
    assert types == sorted(types, key=app._REL_TYPE_ORDER.index), types

    print(f"OK: STK-009 → {len(out)} outbound, {len(inb)} inbound links")


if __name__ == "__main__":
    test_relations_panel_outbound_inbound_and_dedup()
    print("all relations-panel tests passed")
