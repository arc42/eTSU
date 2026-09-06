# 21. File-format specifications live at the boundary owner of the data flow

Date: 2026-06-01

## Status

Accepted

Amended 2026-06-04: every format spec carries a fictive inline example (Decision 5).

## Context

[[0020-master-data-as-configuration|ADR-0020]] established that configuration entities
([[GLO-014-verein|Vereine]], [[GLO-018-sportverband|Sportverbände]],
[[GLO-010-schwimmbad|Schwimmbäder]]/Orte, [[GLO-023-figurenkatalog|Figurenkatalog]]) are
loaded from files, and that the file formats are specified *outside* the data models — the
data model keeps only requirement-level facts. That left an open question: **where exactly**
does a file-format specification (column layout, delimiter, encoding, decimal separator,
versioning) live in the wiki?

Three candidates were on the table:

- **A new content type** „File format" — rejected: a format spec is not an independent
  requirement unit, it is an attribute of a *data flow*. A new type would fragment the schema
  and duplicate provenance.
- **On the data model** (DM-001/003/004/006) — rejected: a data model describes entities,
  attributes and relationships, not the wire format of one particular inbound channel. The
  same entity can arrive through several channels.
- **At the boundary where the data crosses the system edge** (Weg A) — chosen.

The format proposals already drafted in `raw/drafts/` (`figurenkatalog-format-vorschlag.md`,
`schwimmbad-orte-format-vorschlag.md`, `verein-format-vorschlag.md`,
`sportverband-format-vorschlag.md`) all describe *imports* — i.e. flows that cross the system
boundary. That is the natural home.

## Decision

1. **A file-format specification lives at the boundary owner of its data flow** — the wiki
   node that owns the edge across which the data enters or leaves the system. No new content
   type is introduced.
2. **External feeds** — recurring data crossing an edge to/from an external *system* — carry
   their format on the [[wiki/external-interfaces|External Interface]] node, inside the
   relevant `flows:` entry. The Figurenkatalog import (EAquA, yearly) is specified on
   [[EIF-001-drsl-figurenkatalog]].
3. **Internal configuration imports** — bootstrapping files loaded at program start, with no
   external partner system — are specified on the [[FR-006-systemadministration]]
   bootstrapping requirement (the boundary owner is the admin/deployment action, not an EIF).
   The three CSV formats Schwimmbad/Orte, Verein and Sportverband live there.
4. **Data models only reference.** DM-001/003/004/006 link to the boundary node that owns the
   format; they never restate column layouts or delimiters.
5. **Every format spec carries a fictive example** *(added 2026-06-04)* — a fenced
   ` ```csv ` block of 5–8 rows inside the spec section on the boundary-owner page,
   exercising the edge cases the validation rules name (encoding/umlauts, optional
   columns such as Schwimmbad `telefon`/`email` "und/oder"). The example is part of the
   spec: no separate example files, no asset folder, no new rubric — a "supporting
   models" home was considered and rejected (it would re-scatter what this ADR
   consolidated; an example is spec content, not a model). Development copies the block
   as a test fixture.

## Consequences

- The format-spec question is answered without growing the content-type taxonomy
  ([[0002-content-type-taxonomy|ADR-0002]] stays intact).
- There is exactly one home per format, co-located with the trigger/direction/partner facts
  it belongs to — provenance and the format spec sit together.
- A given entity reachable through multiple channels can carry one format per channel, each on
  its own boundary node, without contradiction.
- Follow-up work (separate to-dos): create the FR-006 config-import story/stories and anchor
  the Schwimmbad/Orte format there; bring `verein-format-vorschlag.md` and
  `sportverband-format-vorschlag.md` onto CSV, grill, and ingest them likewise; DM-001/003/006
  become reference-only.
- Reversal would mean relocating every format block and reintroducing a rejected content type —
  hence this record.
