# 20. Master data as configuration: file import, runtime CRUD only for clubs, no soft-delete

Date: 2026-06-01

## Status

Accepted

## Context

While cutting the stories for [[FR-008-stammdatenpflege]] (grill session 2026-06-01), the
nature of the "Stammdaten" was sharpened. Aquarius distinguishes:

- **Configuration** — data that changes rarely or never and is loaded from a file:
  [[GLO-014-verein|Vereine]], [[GLO-018-sportverband|Sportverbände]],
  [[GLO-010-schwimmbad|Schwimmbäder]]/Orte and the [[GLO-023-figurenkatalog|Figurenkatalog]].
- **Operational data** — data that changes continuously: [[GLO-006-kind|Kinder]].

Two questions had to be settled: where the file import lives, and whether entities need a
soft-delete (`aktiv`) flag. The data models (DM-001/003/004/005/006) had each introduced an
`aktiv` soft-delete flag specifically to keep historical Wettkampf/Anmeldung/Start references
intact. The owner decided against that complexity.

## Decision

1. **Configuration is loaded from files.** Each configuration entity has its own file format
   (proposals in `raw/drafts/`: `figurenkatalog-format-vorschlag.md`,
   `schwimmbad-orte-format-vorschlag.md`, `verein-format-vorschlag.md`,
   `sportverband-format-vorschlag.md`). For the Figurenkatalog the inbound channel is
   [[EIF-001-drsl-figurenkatalog]] (EAquA, yearly).
2. **Initial bootstrap at program start is deployment/system administration** → belongs to
   [[FR-006-systemadministration]], not FR-008. The yearly Figurenkatalog re-import (triggered
   by Backoffice) stays in FR-008.
3. **Only Vereine get a runtime CRUD path** in FR-008 (a club may join mid-season).
   Sportverbände ("never change") and Schwimmbäder/Orte are configuration-only.
4. **No soft-delete.** The `aktiv` flag is removed from DM-001/003/004/005/006. Entities are
   **hard-deleted**; deletion does **not** check references. Historical references may break —
   accepted deliberately (old rankings are not business-relevant; a ranking snapshot can be
   generated if ever needed). Tracked as a standing risk in
   [[ISS-016-aktiv-soft-delete-entfernen]].
5. **Kinder are operational data**, maintained by Backoffice/Präsident (`Must`) and by family
   self-service (`Should`); Vereine get no access to Stammdatenpflege.

## Consequences

- `aktiv` removed from [[DM-001-verein]], [[DM-003-schwimmbad]], [[DM-004-figur]] (was already
  only an open point), [[DM-005-kind]], [[DM-006-sportverband]]; the "stays referenceable while
  inactive" invariants are replaced by the hard-delete reality.
- Configuration entities carry no lifecycle/active state.
- Risk to [[GOAL-004-nachvollziehbare-regelkonforme-bewertung]] (audit trail) and
  [[FR-005-ergebnisauswertung]] is accepted and documented in ISS-016, which stays `open`.
- File formats are specified outside the data models; the data model keeps only requirement-level
  facts.
- Reversal would mean reintroducing `aktiv` across five entities and re-deriving the dropped
  invariants — non-trivial, hence this record.
