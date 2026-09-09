# Log

Append-only. One entry per operation. Keep the prefix exact so the log is
greppable: `grep '^## \[' _system/log.md | tail -5`.

<!-- Format:
## [YYYY-MM-DD] ingest | <source title>
- created: GLO-004, STK-002, UC-007
- updated: _system/index.md, FEAT-001
- issues: ISS-003 (contradiction: SLA target vs CON-002)
-->

## [2026-09-06] bootstrap | eTSU
- system_name kept as "eTSU" (matches the brief's own wording); tagline set to "Combining Art, AI and Requirements"
- ubiquitous language confirmed as English (ADR-0005 unchanged)
- created: GOAL-001 (vision), GLO-001 (Tour), GLO-002 (Show), STK-001 (Gus Renoir)
- updated: _system/wiki.yaml, _system/index.md
- next: `raw/TSU-brief.md.md` is sitting in the inbox — proceed with the normal, grill-gated `ingest.md` pass

## [2026-09-09] ingest | Req4Arc Linz workshop emails (3)
- grill-gated per `ingest.md`; four decisions taken with the human before writing:
  (1) Ulrich's "VISION 1/2/3" are PAM objectives, not visions — filed under GOAL-001;
  (2) the 2029 newspaper supplies a five-year ambition, the VISION blocks the Year-1 targets;
  (3) only stakeholders with a documented interaction get pages, the rest become an Issue;
  (4) `raw/TSU-brief.md.md` stays queued — this pass covers the emails only.
- created: SRC-001, SRC-002, SRC-003
- created: GOAL-002 (global market reach), GOAL-003 (operational excellence), GOAL-004 (authenticated provenance), GOAL-005 (real-time visibility)
- created: STK-002 artist, STK-003 gallery manager, STK-004 buyer, STK-005 shipper, STK-006 insurer, STK-007 customs authority, STK-008 museum, STK-009 restorer, STK-010 legal & accounting, STK-011 development team, STK-012 Creative Genius, STK-013 private owner
- created: GLO-003 Provenance, GLO-004 TSU, GLO-005 eTSU
- updated: GOAL-001 (objective backlinks + competing-vision note), STK-001 (aliases CEO / TSU management), _system/index.md
- issues: ISS-001 (contradiction: two vision statements), ISS-002 (gap: unsourced baselines), ISS-003 (contradiction: Year-1 vs 2029 targets), ISS-004 (**blocker**, risk: back-office tool vs global marketplace), ISS-005 (question: six ungrounded stakeholder entries), ISS-006 (ambiguity: buyer vs art collector), ISS-007 (ambiguity: cleaner vs restorer), ISS-008 (gap: Thomas Marti's email arrived empty), ISS-009 (ambiguity: "real time" untestable, GOAL-005 overlaps GOAL-002/003)
- notes: STK-012 and STK-013 surfaced by grilling Georg's list against the brief — they are in the brief and *missing* from the workshop list; both carry `> [!assumption]` and empty `sources:` until the brief is ingested
- next: `raw/TSU-brief.md.md` still in the inbox; ISS-004 blocks the Context page and the backlog

## [2026-09-09] ingest | Context Diagram (Ulrich Stürzlinger)
- grill-gated; source is a PNG attachment — a 14-node business ecosystem diagram, not a system context diagram
- decisions with the human: (1) capture the diagram **as drawn**, one EIF per box, rather than decomposing it — supersedes ADR-0013 point 1 for this context; (2) the EIF nodes own the context edges, the 7 duplicated stakeholders get `context_role: none` so the projection renders each actor once
- answered: **no new content type needed** — EIF is the external-systems type (ADR-0009/0013); taxonomy stays at thirteen, per ADR-0024's precedent
- created: SRC-004
- created: CTX-001 (eTSU system context)
- created: EIF-001 artists, EIF-002 museums & owners, EIF-003 appraisers & authenticators, EIF-004 customer support & marketing, EIF-005 fraud & security, EIF-006 business growth & content, EIF-007 data & analytics, EIF-008 individual buyers, EIF-009 global online buyers, EIF-010 institutional buyers, EIF-011 gallery operations, EIF-012 logistics & fulfillment, EIF-013 technology & infrastructure, EIF-014 regulatory & compliance
- created: ADR-0026 (capture as drawn; adds `tier:` to the external-interface template)
- updated: _templates/external-interface.md (new `tier:` field), STK-002/004/005/006/008/009/013 (`context_role: none` + EIF twin link), ISS-004 (diagram corroborates Reading B), ISS-006 (widened by ISS-013), _system/index.md
- issues: ISS-010 (**blocker**, ambiguity: CORE OPERATIONS drawn outside the boundary), ISS-011 (gap: all flows inferred from box labels, no arrow labelled), ISS-012 (ambiguity: 4 nodes bundle 2–3 partners each; customs absent entirely), ISS-013 (contradiction: third buyer segmentation), ISS-014 (question: starter ADRs cite issue IDs absent from this vault)
- new facts: TSU has **6 gallery locations** (first source to say so); "Appraisers & Authenticators" and "corporate collections" appear in no earlier source
- next: ISS-010 cannot close before ISS-004; ~half of wiki/external-interfaces/ is provisional until it does
- follow-up (same day): ISS-015 ("a new Picasso" undefined/unmeasurable) and ISS-016 (Moore vision format cited by `_templates/goal.md` with no `_system/anchors/` entry, contra ADR-0004) raised on the human's question; both linked from ISS-001, which cannot be decided while neither candidate vision is legible
- follow-up (same day): context diagram made legible. The projection drew one edge per direction (28 labelled arrows) and used `partner:` — a full sentence — as node labels. Now: one `<-->` line per neighbour with one short label (new `short_title:` on EIF, `label:` per flow), `tier:` clustered into mermaid subgraphs and used to rank nodes left/right of the centre, and a flow table beneath the diagram carrying both directions in full. Fixed two latent bugs in `_clean_label()`: `&` was silently deleted from every diagram label vault-wide, and edge labels ordered in-then-out instead of document order. ADR-0026 amended; regression cover in `tests/test_context_projection.py`. CTX-001's duplicated interface list collapsed into two tables.

## [2026-09-09] ingest | Req4Arc Linz workshop photos (card wall + eTSU context sketch)

Two photographs from the raw inbox, both from the Linz workshop, author unattributed.
Grilled before writing (`grill-requirements`); three decisions taken by Gernot Starke
in the session shaped the result.

**Sources.** `SRC-005` capability card wall (12 handwritten cards, two print sizes,
no drawn grouping). `SRC-006` hand-drawn eTSU context sketch on an Asseco notepad
(6 neighbours: Visitors, Artist, Payment, Invoice, Delivery, Social Media).

**Decision — the cards are held, not promoted.** Twelve names, no definitions, no
owners. Rather than fill `wiki/functional-requirements/` with twelve unfalsifiable
epics, the transcribed list lives in `ISS-017` until a definition pass runs. The
backlog folder stays empty on purpose.

**Decision — the sketch is a competing artefact.** It contradicts the ecosystem
diagram behind `CTX-001` on almost every count and is structurally the better
context diagram, but it was not an agreed refinement. `ISS-018` holds both sides;
`CTX-001` keeps recording the ecosystem diagram alone.

**Created.** `SRC-005`, `SRC-006`, `ISS-017` (12 cards undefined, carries the list),
`ISS-018` (competing context diagrams), `ISS-019` (Visitors undefined),
`ISS-020` (four sketch boxes untyped), `ISS-021` (authentication ambiguous).

**Updated.** `ISS-004` (both photos bear on scope and point opposite ways — the card
wall is pure back-office, the sketch has Visitors and Social Media), `ISS-013`
(two further segmentation cuts: customer/museum processes, and Visitors), `CTX-001`.

## [2026-09-09] decisions | Four open issues closed by Gernot Starke

Taken mid-ingest, applied across the wiki.

- **`ISS-008` → wontfix.** Thomas Marti's empty email is ignored; nobody chases a resend.
- **`ISS-006` → resolved: two roles.** Buyer and art collector are distinct.
  `STK-014-art-collector` created (goals/pains inferred, flagged as assumption);
  the `art collector` alias removed from `STK-004`. The wider segmentation question
  stays open in `ISS-013`.
- **`ISS-007` → resolved: one role, the conservator.** *Cleaner* and *restorator* are
  aliases; *restorer* was a typo for *restorator*, kept as an alias. No janitorial
  stakeholder exists. `STK-009-restorer` retitled and renamed to
  `STK-009-conservator`, all references rewritten; `GLO-006-conservator` added as an
  **agreed** glossary term.
- **`ISS-010` → resolved: a drawing mistake.** TSU's own operations were placed
  outside the boundary in error; the line runs around eTSU the product.
  `EIF-004`, `EIF-006`, `EIF-007` and `EIF-011` deprecated as internal (kept, not
  deleted, so the artefact stays readable); `EIF-013` narrowed to the payment
  provider. Fourteen boundary nodes became ten. `CTX-001` updated throughout;
  `ISS-004` is now the blocker on that page.

**Archived.** `raw/IMG_3585.jpeg` and `raw/IMG_3586.jpeg` → `raw/ingested/`.
