"""The context diagram is a projection, and it has to stay readable — no pytest.

The regression this guards: `build_context_diagram()` drew ONE EDGE PER
DIRECTION and labelled every node with `partner:`, which is a full sentence by
design ("Museums and private owners who lend artwork"). With the fourteen
interfaces of CTX-001 that produced 28 labelled arrows carrying whole clauses
around a single box — the diagram rendered, and nobody could read it.

The rules that replaced it (ADR-0026):
  * a neighbour with flows in BOTH directions draws ONE `<-->` line, not two;
  * the line carries ONE short label, deduplicated, in the order the flows are
    written — the per-direction detail moves to build_context_flows();
  * node labels prefer `short_title`, then `title`, and only fall back to
    `partner`;
  * `tier:` groups nodes into subgraphs, and decides which side of the centre a
    neighbour is ranked on, so mermaid stops scattering them;
  * a `status: deprecated` interface is one the boundary decision moved inside
    the system (ISS-010) — it keeps its page and its flows, but it is no longer
    a neighbour and is drawn nowhere.

Run from the dashboard dir:
    .venv/bin/python tests/test_context_projection.py
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
os.environ["DASH_STARTUP_GRACE"] = "3600"
os.environ["DASH_HEARTBEAT_GRACE"] = "3600"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # import app.py

import app  # noqa: E402

_EIF = _wiki / "external-interfaces"


def _eif(num, title, tier, flows, short_title=None, partner=None, status="draft"):
    front = [
        "---", f"id: EIF-{num}", "type: external-interface", f"title: {title}",
        f"status: {status}", "created: 2026-09-09", "updated: 2026-09-09",
        "sources: []", "related: []", "tags: [external-interface]",
        f"partner: {partner or title}", f"tier: {tier}",
    ]
    if short_title:
        front.append(f"short_title: {short_title}")
    front.append("flows:")
    front += [f"  - {{ {f} }}" for f in flows]
    front += ["---", "", f"# {title}", ""]
    _EIF.joinpath(f"EIF-{num}-{title.lower().replace(' ', '-')}.md").write_text(
        "\n".join(front), encoding="utf-8")


# bidirectional, supply side, both flows labelled
_eif("001", "Artists", "supply", [
    "data: artwork submissions and tour participation, direction: inbound, label: artwork",
    "data: sale notifications and commission statements, direction: outbound, label: sales",
], short_title="Artists", partner="Artists — individual creators who submit work")
# bidirectional, demand side, SAME label on both flows -> must dedupe to one word
_eif("002", "Buyers", "demand", [
    "data: purchase intent and payment, direction: inbound, label: orders",
    "data: confirmations, direction: outbound, label: orders",
], short_title="Buyers")
# one-way only, and no short_title -> falls back to `title`, never to `partner`
_eif("003", "Regulator", "core-operations", [
    "data: tax filings, direction: outbound, label: filings",
], partner="Tax authorities, AML/KYC providers and law enforcement")
# no `label:` anywhere -> falls back to `data`, clipped so it cannot bloat again
_eif("004", "Analytics", "support", [
    "data: an extremely long payload description that would wreck the layout, direction: inbound",
])
# deprecated: the boundary decision moved this one INSIDE the system (ISS-010),
# so it is no longer a neighbour. Flows and all, it must not be drawn — and the
# edge/node counts asserted above stay at four because of it.
_eif("005", "Payments", "core-operations", [
    "data: card authorisations, direction: outbound, label: payments",
    "data: settlement reports, direction: inbound, label: settlement",
], short_title="Payments", status="deprecated")


def _diagram():
    d = app.build_context_diagram()
    assert d, "no diagram projected — is another test module holding WIKI_DIR?"
    return d


def _edges(d=None):
    d = d or _diagram()
    return [l.strip() for l in d.splitlines()
            if ("-->" in l or "<-->" in l) and "classDef" not in l]


def test_one_line_per_neighbour_not_one_per_direction():
    e = _edges()
    assert len(e) == 4, f"expected 4 edges for 4 neighbours, got {len(e)}: {e}"
    assert sum(1 for x in e if "<-->" in x) == 2, \
        f"the two bidirectional neighbours must draw one <--> each: {e}"


def test_edge_labels_are_short_deduplicated_and_in_document_order():
    e = _edges()
    assert any('<-->|"artwork \u00b7 sales"|' in x for x in e), \
        f"EIF-001 label should read 'artwork \u00b7 sales' in flow order: {e}"
    assert any('<-->|"orders"|' in x for x in e), \
        f"EIF-002's repeated label must collapse to one 'orders': {e}"
    assert not any("orders \u00b7 orders" in x for x in e), "duplicate label not deduplicated"


def test_node_label_prefers_short_title_then_title_never_partner():
    d = _diagram()
    assert '["Artists"]' in d, "short_title should label the node"
    assert '["Regulator"]' in d, "with no short_title the node falls back to `title`"
    assert "Tax authorities, AML/KYC" not in d, \
        "`partner:` is a sentence and must never reach a node label"
    assert "individual creators who submit work" not in d, "`partner:` leaked into the diagram"


def test_unlabelled_flow_clips_its_data_fallback():
    long_edge = [x for x in _edges() if "EIF004" in x]
    assert long_edge, "the unlabelled interface still needs an edge"
    assert "\u2026" in long_edge[0] and len(long_edge[0]) < 90, \
        f"an unlabelled flow must clip its data fallback: {long_edge}"


def test_tiers_become_subgraphs_and_rank_nodes_around_the_centre():
    d = _diagram()
    for band in ("Supply", "Support", "Demand", "Core operations"):
        assert f'["{band}"]' in d, f"missing subgraph for tier {band}"
    e = _edges(d)
    assert any(x.startswith("EIF001 <-->") for x in e), \
        "supply is ranked BEFORE the centre so it lays out on the left"
    assert any(x.startswith("CORE <-->") and "EIF002" in x for x in e), \
        "demand is ranked AFTER the centre so it lays out on the right"


def test_the_table_carries_the_detail_the_diagram_dropped():
    flows = app.build_context_flows()
    by_id = {g["id"]: g for g in flows}
    assert len(flows) == 4, \
        f"every live interface with flows needs a table group, got {len(flows)}"
    assert len(by_id["EIF-001"]["rows"]) == 2, "both directions must be listed for EIF-001"
    assert [r["direction"] for r in by_id["EIF-001"]["rows"]] == ["in", "out"], \
        "table lists inbound then outbound"
    assert by_id["EIF-001"]["rows"][0]["data"] == "artwork submissions and tour participation", \
        "the table carries the FULL data description the edge label dropped"
    assert by_id["EIF-001"]["partner"].startswith("Artists"), \
        "the table keeps the full partner name the node label dropped"
    assert by_id["EIF-003"]["tier"] == "Core operations", "tier is shown in words"
    assert by_id["EIF-001"]["rows"][0]["format"] is None, \
        "absent format must be None, not the word 'unknown'"


def test_a_deprecated_neighbour_is_not_drawn():
    """ISS-010: `status: deprecated` on an interface means the boundary moved
    and it is now internal. It keeps its flows on the page — that history is
    worth having — so the diagram has to filter on status, not on emptiness."""
    d = _diagram()
    assert "Payments" not in d, \
        f"a deprecated interface must not appear as a node:\n{d}"
    assert not any("payments" in x or "settlement" in x for x in _edges(d)), \
        f"a deprecated interface must draw no edge: {_edges(d)}"


def test_a_deprecated_neighbour_has_no_flow_table_group():
    """The table beneath the diagram is the same projection in prose; leaving
    the row in would contradict the picture it explains."""
    ids = [g["id"] for g in app.build_context_flows()]
    assert "EIF-005" not in ids, ids
    assert "EIF-001" in ids, f"the live interfaces must still be listed: {ids}"


def test_an_ampersand_is_never_silently_deleted():
    # "Museums & owners" used to render as "Museums owners" in every diagram
    assert app._clean_label("Fraud & Security") == "Fraud and Security", \
        f"'&' must become 'and', got {app._clean_label('Fraud & Security')!r}"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
        except AssertionError as exc:
            failed += 1
            print(f"FAIL {fn.__name__}: {exc}")
    if failed:
        sys.exit(1)
    print(f"ok — {len(fns)} checks, {len(_edges())} edges for 4 neighbours")
