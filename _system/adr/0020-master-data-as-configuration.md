# 20. Master data as configuration: file import, runtime CRUD only for Entity A, no soft-delete

Date: 2026-06-01

## Status

Accepted

## Context

While cutting the stories for [[FR-008-master-data-maintenance]] (grill session 2026-06-01), the
nature of the "master data" was sharpened. The system distinguishes:

- **Configuration** — data that changes rarely or never and is loaded from a file:
  [[GLO-014-entity-a|Entity A]], [[GLO-018-entity-b|Entity B]],
  [[GLO-010-entity-c|Entity C]]/locations and the [[GLO-023-entity-d|Entity D catalog]].
- **Operational data** — data that changes continuously: [[GLO-006-entity-e|Entity E]].

Two questions had to be settled: where the file import lives, and whether entities need a
soft-delete (`active`) flag. The data models (DM-001/003/004/005/006) had each introduced an
`active` soft-delete flag specifically to keep historical references (from downstream
transactional records) intact. The owner decided against that complexity.

## Decision

1. **Configuration is loaded from files.** Each configuration entity has its own file format
   (proposals in `raw/drafts/`: `entity-d-format-proposal.md`,
   `entity-c-format-proposal.md`, `entity-a-format-proposal.md`,
   `entity-b-format-proposal.md`). For the Entity D catalog the inbound channel is
   [[EIF-001-system-x-catalog-feed]] (System X, yearly).
2. **Initial bootstrap at program start is deployment/system administration** → belongs to
   [[FR-006-system-administration]], not FR-008. The yearly Entity D catalog re-import (triggered
   by Backoffice) stays in FR-008.
3. **Only Entity A gets a runtime CRUD path** in FR-008 (an instance may join mid-season).
   Entity B ("never changes") and Entity C/locations are configuration-only.
4. **No soft-delete.** The `active` flag is removed from DM-001/003/004/005/006. Entities are
   **hard-deleted**; deletion does **not** check references. Historical references may break —
   accepted deliberately (old rankings are not business-relevant; a ranking snapshot can be
   generated if ever needed). Tracked as a standing risk in
   [[ISS-016-remove-active-soft-delete]].
5. **Entity E is operational data**, maintained by Backoffice/Role C (`Must`) and by
   end-user self-service (`Should`); Entity A gets no access to master-data maintenance.

## Consequences

- `active` removed from [[DM-001-entity-a]], [[DM-003-entity-c]], [[DM-004-entity-d]] (was already
  only an open point), [[DM-005-entity-e]], [[DM-006-entity-b]]; the "stays referenceable while
  inactive" invariants are replaced by the hard-delete reality.
- Configuration entities carry no lifecycle/active state.
- Risk to [[GOAL-004-traceable-compliant-evaluation]] (audit trail) and
  [[FR-005-result-evaluation]] is accepted and documented in ISS-016, which stays `open`.
- File formats are specified outside the data models; the data model keeps only requirement-level
  facts.
- Reversal would mean reintroducing `active` across five entities and re-deriving the dropped
  invariants — non-trivial, hence this record.
