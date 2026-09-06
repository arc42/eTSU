"""Plain-assert test for build_relations_panel() — no pytest dependency.

    .venv/bin/python tests/test_relations_panel.py

WIKI_DIR points at tests/fixtures/wiki, a small neutral vault, so the suite is
independent of whatever content this starter is filled with. Powers the
detail-page 'Links to' / 'Linked from' section.
"""
import os
import sys
from pathlib import Path

_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "wiki"
os.environ["WIKI_DIR"] = str(_FIXTURE)
os.environ["ADR_DIR"] = str(_FIXTURE.parent / "adr")
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app  # noqa: E402


def _flat(groups):
    return [it for g in groups for it in g["links"]]


def test_relations_panel_outbound_inbound_and_dedup():
    with app.app.test_request_context("/"):
        rel = app.build_relations_panel("STK-001-librarian")

    out = _flat(rel["outbound"])
    inb = _flat(rel["inbound"])
    out_ids = {i["id"] for i in out}
    inb_ids = {i["id"] for i in inb}

    # a link never appears in both buckets (inbound excludes outbound)
    assert not (out_ids & inb_ids), out_ids & inb_ids
    # never links to itself
    assert "STK-001" not in out_ids and "STK-001" not in inb_ids

    # outbound carries the glossary terms this stakeholder relates to
    assert "GLO-003" in out_ids, "glossary term Member missing from outbound"
    assert "GLO-002" in out_ids, "glossary term Loan missing from outbound"
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

    print(f"OK: STK-001 → {len(out)} outbound, {len(inb)} inbound links")


if __name__ == "__main__":
    test_relations_panel_outbound_inbound_and_dedup()
    print("all relations-panel tests passed")
