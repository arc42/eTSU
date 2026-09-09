"""The data-model class diagram — a projection, like every other diagram here.

Two carriers feed it, and the split is the decision worth guarding (ADR-0027):

  * a `DM-` page is the carrier of record. It holds identity, attributes and a
    `relationships:` list in frontmatter, which is where the edges come from —
    body prose is for humans, frontmatter is for the projection, exactly as
    `flows:` works for the context diagram (ADR-0026).
  * a glossary term marked `stereotype: entity` (or `value-object`) appears as a
    STUB class: named, empty, annotated `<<term>>`. It costs one line during a
    workshop and makes an unmodelled entity visible as work outstanding instead
    of invisible.

A DM page supersedes the stub for the same concept, so nothing is ever drawn
twice — that is the rule this suite mostly exists to hold.

Run from the dashboard dir:
    .venv/bin/python tests/test_data_model_diagram.py
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

_DM = _wiki / "data-models"
_GLO = _wiki / "glossary"


def _dm(num, title, context, attributes=(), relationships=(), related=(),
        stereotype="entity", parent=()):
    front = [
        "---", f"id: DM-{num}", "type: data-model", f"title: {title}",
        "status: draft", "created: 2026-09-09", "updated: 2026-09-09",
        "sources: []", f"related: [{', '.join(related)}]", "tags: [data-model]",
        f"stereotype: {stereotype}", f"parent: [{', '.join(parent)}]",
        f"bounded-context: {context}", "source-of-truth: System X",
        "relationships:",
    ]
    front += [f"  - {{ {r} }}" for r in relationships]
    front += ["---", "", f"# {title}", "", "**Attributes.**"]
    front += [f"- `{a}` : text — a field" for a in attributes]
    front += [""]
    _DM.joinpath(f"DM-{num}-{title.lower().replace(' ', '-')}.md").write_text(
        "\n".join(front), encoding="utf-8")


def _glo(num, title, context, stereotype=None):
    front = [
        "---", f"id: GLO-{num}", "type: glossary-term", f"title: {title}",
        "status: accepted", "created: 2026-09-09", "updated: 2026-09-09",
        "sources: []", "related: []", "tags: [glossary]", "aliases: []",
        f"bounded-context: {context}", "agreed: true",
    ]
    if stereotype:
        front.append(f"stereotype: {stereotype}")
    front += ["---", "", f"# {title}", "", "**Definition.** A thing.", ""]
    _GLO.joinpath(f"GLO-{num}-{title.lower().replace(' ', '-')}.md").write_text(
        "\n".join(front), encoding="utf-8")


# Catalog context: Artwork owns Lots, and inherits from Asset.
_dm("001", "Artwork", "Catalog", attributes=["id", "title"], relationships=[
    "verb: contains, target: \"[[DM-002-lot]]\", cardinality: 1..*, kind: composition",
    "verb: is a, target: \"[[DM-004-asset]]\", kind: inheritance",
    "verb: dangles, target: \"[[DM-999-nowhere]]\", kind: association",
], related=['"[[GLO-002-artwork]]"'])
_dm("002", "Lot", "Catalog", attributes=["id", "lot-number"])
_dm("004", "Asset", "Catalog", attributes=["id"])
# a second bounded context, so the filter has something to exclude
_dm("003", "Payment", "Billing", attributes=["amount"])
# a sum-type variant: `parent:` alone must draw the inheritance (ADR-0019)
_dm("005", "Sold Artwork", "Catalog", stereotype="entity",
    parent=['"[[DM-001-artwork]]"'])

# marked, and NOT modelled anywhere -> a stub class
_glo("001", "Provenance", "Catalog", stereotype="entity")
# marked, but DM-001 claims it via related: -> must NOT double as a stub
_glo("002", "Artwork", "Catalog", stereotype="entity")
# not marked at all -> not in the data model
_glo("003", "Tour", "Catalog")


def _diagram(**kw):
    d = app.build_data_model_full_diagram(**kw)
    assert d, f"no diagram projected for {kw or 'the whole model'}"
    return d


def test_a_dm_page_becomes_a_class_with_its_attributes():
    d = _diagram()
    assert "classDiagram" in d, d
    assert "class Artwork" in d, d
    assert "+id" in d and "+title" in d, d


def test_a_multi_word_entity_keeps_its_word_boundaries():
    """"Sold Artwork" must read as SoldArtwork, not Soldartwork. Both are legal
    mermaid; only one is legible on a projector."""
    assert "class SoldArtwork" in _diagram(), _diagram()


def test_a_hyphenated_attribute_name_survives():
    """`lot-number` is an ordinary field name. Dropping it was silent — the
    attribute just stopped existing in the box and in the table."""
    assert "+lot-number" in _diagram(), _diagram()


def test_a_marked_glossary_term_becomes_an_empty_stub_class():
    d = _diagram()
    assert "class Provenance" in d, d
    assert "<<term>>" in d, "a stub must be annotated so the room can see it is unmodelled"


def test_an_unmarked_glossary_term_stays_out_of_the_model():
    """The glossary is not the data model. Only a marked term is promoted."""
    assert "Tour" not in _diagram()


def test_a_dm_page_supersedes_the_term_it_claims():
    """GLO-002 Artwork is marked, but DM-001 links it — one class, not two."""
    d = _diagram()
    assert d.count("class Artwork") == 1, d
    artwork = [l for l in d.splitlines() if "class Artwork" in l][0]
    assert "<<term>>" not in artwork, "the modelled entity must not render as a stub"


def test_relationships_carry_verb_cardinality_and_kind():
    """`cardinality:` is the multiplicity at the TARGET end, and only there —
    inventing a source multiplicity from it puts a meaningless "0" on the
    owning side of any `0..*`."""
    d = _diagram()
    assert any('Artwork *-- "1..*" Lot : contains' in l for l in d.splitlines()), d


def test_a_parent_link_draws_inheritance_without_repeating_it():
    """A variant names its sum type in `parent:` and nowhere else. Making the
    author restate that as a relationship entry would be one fact in two
    places, and the two would drift."""
    assert any("Artwork <|-- SoldArtwork" in l for l in _diagram().splitlines()), _diagram()


def test_inheritance_points_from_the_base_class():
    """`A is-a B` draws `B <|-- A`, which is the direction mermaid expects."""
    assert any("Asset <|-- Artwork" in l for l in _diagram().splitlines())


def test_a_relationship_to_a_missing_page_is_dropped():
    assert "DM-999" not in _diagram() and "nowhere" not in _diagram().lower()


def test_the_bounded_context_filter_narrows_the_diagram():
    d = _diagram(context="Billing")
    assert "class Payment" in d, d
    assert "Artwork" not in d, "another context's entities must not leak in"


def test_focus_keeps_one_entity_and_its_direct_neighbours():
    d = _diagram(focus="DM-001-artwork")
    assert "class Artwork" in d and "class Lot" in d and "class Asset" in d, d
    assert "Payment" not in d, "focus is one hop, not the whole vault"


def test_a_filter_that_matches_nothing_projects_nothing():
    """The view guards on entities, not on the diagram, so None is a valid
    answer and must stay one (see build_data_model_full_diagram's contract)."""
    assert app.build_data_model_full_diagram(context="No Such Context") is None


def test_the_contexts_are_listed_for_the_filter_ui():
    assert app.data_model_contexts() == ["Billing", "Catalog"], app.data_model_contexts()


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
    print(f"ok — {len(fns)} checks")
