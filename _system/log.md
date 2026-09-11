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

## [2026-09-09] ingest | Glossary terms for four external partners

Requested by Gernot Starke: give the external partners names in the ubiquitous
language. Four terms written, all marked **preliminary**.

**Created.** `GLO-007` Appraiser, `GLO-008` Lender, `GLO-009` Logistics partner,
`GLO-010` AML screening. Each carries `tags: [glossary, preliminary]` alongside
`agreed: false`, and a body callout naming what is still open. `preliminary` is a
tag rather than a new frontmatter field or a new `status:` value, because the
status lifecycle is fixed at draft → review → accepted → deprecated and inventing
a field needs an ADR (CLAUDE.md). It is greppable and filterable as a tag.

**Definitions are the agent's, not the group's.** All four are derived from box
labels on the workshop context diagram plus the brief. None was confirmed with
anyone.

**One new finding.** Writing `GLO-007` surfaced that
`EIF-003-appraisers-and-authenticators` fuses two different jobs: an appraiser
says what a piece is **worth**, an authenticator says whether it is **genuine**.
`ISS-012` grew from four bundled nodes to five and now names the appraiser split.
That Issue is also unblocked, since `ISS-010` closed earlier today.

**Updated.** `ISS-012` (fifth bundle, unblocked, links the four terms), reciprocal
`related:` links added on `EIF-002`, `EIF-003`, `EIF-005`, `EIF-012` and on
`STK-005`, `STK-006`, `STK-008`, `STK-009`, `STK-013`.

## [2026-09-09] ingest | TSU brief, glossary only

Requested by Gernot Starke: more glossary entries from the initial story, with
relations. Guessing was authorised but **not needed** — the brief covers all
thirteen terms explicitly, so every definition is sourced rather than invented.
None carries the `preliminary` tag for that reason; all carry `agreed: false`,
since nothing has been confirmed with Gus Renoir's team.

**Created.** `GLO-011` Piece, `GLO-012` Artist, `GLO-013` Buyer, `GLO-014` Museum,
`GLO-015` Gallery, `GLO-016` Home gallery, `GLO-017` Minimum sale price,
`GLO-018` Minimum museum sale price, `GLO-019` Agreed price, `GLO-020` Commission,
`GLO-021` Lending agreement, `GLO-022` Intent to purchase, `GLO-023` The Insult.
Also `SRC-007` (the brief's first provenance record) and `ISS-022`.

**Two naming calls.** *Piece* is canonical with **artwork** as an alias: the brief
says piece throughout and never says artwork, while the workshop card wall says
"Artwork Management". *Tour stop* needed no new page — it was already an alias on
`GLO-002` Show, which is exactly what the brief says it is.

**The brief is only partially ingested.** Thirteen glossary terms were taken; the
tour-assembly sequence, the payment and commission flows, the loss-of-a-sold-piece
rule and several constraints were not. `ISS-022` records what is left and why the
file stays in the `raw/` inbox rather than moving to `raw/ingested/`.

## [2026-09-09] relations | Whole-vault reciprocity repair

`related:` is symmetric by definition (`relations.md`, Tier 2), but the vault had
drifted one-directional in 149 places, so the Obsidian graph and the dashboard
relations panel only ever saw half of each edge.

- **149 back-links added across 51 pages**, `updated:` bumped on each.
- Tier-1 concept-identity gaps closed: `STK-002`⇄`GLO-012`, `STK-004`⇄`GLO-013`,
  `STK-008`⇄`GLO-014`.
- Verified: 0 asymmetric edges and 0 dangling `related:` targets remain;
  `concept-cluster-audit.py` reports every cluster fully linked.
- Candidates and issues raised: none. Every fix was Tier-1 or symmetric Tier-2,
  which the workflow classifies as auto-fix; nothing judgmental was touched.

## [2026-09-09] ingest | Beneficiary stories (Sandra Mayer)

Grilled before writing. Three decisions taken by Gernot Starke in the session.

**Source.** `SRC-008`, supplied as `.rtf` and `.txt`. The two files differ byte for
byte but carry **identical text** (verified by `textutil` conversion and diff), so
the `.txt` is the record and its hash the one used for drift detection; the `.rtf`
hash is noted alongside. Sender is Sandra **Mayer**, not Meyer.

**Decision — these become stories.** Unlike the bare-noun card wall held in
`ISS-017`, these carry a role and a want, so four `FR` pages were written with
`stereotype: story`. **This is the first backlog content in the vault.**

**Decision — benefit clauses stay empty.** None of the four states a "so that".
The lines are left blank on the pages with an assumption callout, and `ISS-023`
covers all four rather than inventing four sentences nobody said.

**Decision — "exhibition" means Show.** Added as an alias on `GLO-002`. Settling
the word exposed a contradiction it had been hiding: Sandra fires close-out at
Show end, while the brief puts both conservation and release-to-buyer at **Tour**
close and states outright that a buyer may not take a piece until the tour is
over. `ISS-024` holds it; the wiki picks no side.

**Created.** `SRC-008`; `FR-001` View piece inventory and status, `FR-002` Settle
finances and legal obligations, `FR-003` Upload piece information, `FR-004` Track
piece status; `ISS-023`, `ISS-024`.

**Updated.** `GLO-002` (exhibition alias, sources, contradiction warning),
`ISS-004` (the two artist stories are the first artist-**facing** surface in the
wiki, a third distinct piece of evidence for Reading B, from a fourth
contributor), `_system/index.md`.

**Two things flagged, not fixed.** `FR-002` is at the wrong altitude and is almost
certainly an epic. All four priorities are the template's `Should` default, so the
backlog is not prioritised even though every item carries a priority.

**Archived.** Both files → `raw/ingested/`.

## [2026-09-09] goals | Two new objectives, and the backlog un-orphaned

Gernot Starke asked for the two proposed goals to be written and for the
orphaned-requirements list on the dashboard backlog page to be cleared.

**Goal coverage was audited against metrics, not prose.** Three of the five
`goal:` links written earlier today did not survive: `FR-001` and `FR-002` both
claimed `GOAL-003`, which measures *tour setup lead time*, and neither operates
before first show opening; `FR-003` claimed `GOAL-002`, which measures digital
revenue share, two removes away from artist data entry. All three were removed,
with the removal recorded on each page.

**Created — goals.** `GOAL-006` Settlement that is correct and on time (metric:
share of payment obligations settled inside their contractual deadline; four
obligations on four clocks, plus The Insult and the lost-piece refund).
`GOAL-007` Artists maintain and follow their own work (metric: share of catalogue
pieces supplied by the artist). **Both are agent-proposed and confirmed by
nobody**, and `GOAL-007` is a scope commitment leaning to Reading B of `ISS-004`.

**Created — epics.** `FR-005` Piece Management, `FR-006` Tour Visibility,
`FR-007` Settlement and Compliance. Orphans went from four to zero; the tile now
reads 3 epics, 4 stories.

**The epics are the agent's grouping.** `FR-005` is the card wall's "Artwork
Management" renamed into the ubiquitous language. `FR-007` absorbs three
undefined cards (payment, contract and insurance claim handling) on the reading
that all three are obligations with deadlines. `FR-006` is on no card at all and
takes its name from `GOAL-005`. `ISS-017` was updated: four of its twelve cards
are absorbed, eight remain held and undefined.

**One thing got worse, deliberately visible.** `FR-002` is epic-sized and now
sits under `FR-007`, which says nearly the same thing one level up. The backlog
carries that scope twice at two altitudes. Recorded in `ISS-023` rather than
resolved, because splitting `FR-002` is the group's call.

**Updated.** `FR-001`–`FR-004` (parents, corrected goals), `GOAL-005` (its
"Served by: none captured yet" line was stale), `ISS-017`, `ISS-023`, index.

## [2026-09-09] backlog | FR-002 split into five settlement stories

Gernot Starke instructed the split. `FR-002` is **retired** (`status: deprecated`,
kept not deleted) and replaced by five stories under
`FR-007-settlement-and-compliance`.

**Created.** `FR-008` Collect the purchase deposit, `FR-009` Collect the purchase
balance, `FR-010` Settle a failed purchase, `FR-011` Pay artist commission,
`FR-012` Settle a loss claim on a sold piece.

**These are the first stories in the wiki with real acceptance criteria.** The
brief states the money rules precisely enough to write Given-When-Then against —
the 24-hour deposit with its Friday/Saturday Monday rule, the 14-day balance with
no weekend extension, The Insult's half-and-half split, commission in two halves
on two clocks, and the three-way unwind when a sold piece is lost on tour. Benefit
clauses are **derived** from the brief's stated consequences rather than quoted,
and each page says so.

**The "legals" half of FR-002 did not survive the split.** All five successors are
money rules. Contracts, tax and AML screening had no rule to write a criterion
against, so no story covers them. Recorded as an open point on `FR-007`, **not
filed as an Issue** — it is a question for the human first (CLAUDE.md).

**Two open money questions surfaced**, both on `FR-012`: whether the second half
of the commission is still owed after a loss, and what happens when a piece is
lost before the buyer has paid in full. Neither is answered by any source.

**Dashboard.** `build_backlog` now excludes `status: deprecated` items, the same
rule already applied to a deprecated external interface. Without it the retired
`FR-002` would still have been counted and drawn under its epic. Backlog now
reads 3 epics, 8 stories, 0 orphans.

**Updated.** `FR-007` (five children, the legals gap), `ISS-023` (FR-002 row
struck, the other three stories unaffected), `ISS-022` (three of its seven
uningested rows now done), `SRC-007`, `GOAL-006`, index.

## [2026-09-09] model | data model projected from the glossary

Wrote the first data model, derived from the glossary rather than from a new
source. Four modelling calls were put to the human and confirmed: Piece is a
sum type (for sale / on loan carry different payloads, so a status flag would
leave half the attributes always null); Museum is an independent entity with
associations to the lender and buyer roles rather than inheriting both; home
gallery is a role on Tour, not a subclass of Gallery; the single `Gallery
Touring` context splits into `Gallery Touring` and `Settlement`.

- Marked 20 of 23 glossary terms `stereotype: entity|value-object` (ADR-0027).
  TSU, eTSU and AML screening are not data and stay unmarked.
- Re-scoped 7 terms into the new `Settlement` bounded context.
- Created DM-001..DM-010, with `relationships:` frontmatter feeding the
  projected class diagram at `/data-model`.
- Raised ISS-025: relationships are sourced, attribute lists are not.

## [2026-09-09] ingest | Req4Arc Linz workshop photos 2 — card decomposition + Example Mapping stories

Grilled first (`grill-requirements`), then a six-question round put to Gernot Starke
via `grilling`. **He answered one of the six**, question 6, with *"we need to protect
both."* Per `ingest.md` step 5 an ingest does not block on an unanswered round, so
the other five were executed on the agent's own recommendations and every page says
so.

**Sources.** `SRC-009` green cards decomposing the "As Gus" inventory story into two
groups and nine operations, plus four loose capability cards. `SRC-010` ten pink
cards in full role-goal-benefit form. Authorship **unconfirmed** — a "Neza Naglic"
name sheet is in shot on `SRC-009` but nobody confirmed it, and one green card is
cut off at the frame edge showing only "Tra…" over "Ma…", recorded as unreadable
rather than guessed at.

**The one settled decision became a goal.** "Protect both" means the business
protects the artwork as well as the money. Every damage rule in the brief protects
money only: refund the buyer, artist keeps their half-commission, TSU absorbs the
rest. `GOAL-008` Every piece comes home intact is the missing half, and
`FR-016 Piece Protection` serves it.

**Created — 17 pages.** Goal: `GOAL-008`. Epics: `FR-013` Artist Management,
`FR-014` Contract Management, `FR-015` Tour Scheduling, `FR-016` Piece Protection.
**The wiki's first features:** `FR-017` Artwork Inventory, `FR-018` Artwork Tracking.
Stories: `FR-019`–`FR-024` from the green operations, `FR-025`–`FR-029` from the
pink cards. Sources `SRC-009`, `SRC-010`.

**`FR-001` retired**, the same fate as `FR-002`. The workshop wrote it verbatim at
the head of a decomposition table and hung nine operations under it, so it was being
used at epic altitude and duplicated `FR-006` above it.

**Two cards changed epic within one day.** *contract handling* moved from
`FR-007` to `FR-014`, because the workshop drew Contract Management as its own
capability; *insurance claim handling* moved to `FR-016` under "protect both".
`ISS-017` records that, and that re-homing two cards within hours is itself evidence
that grouping undefined names is guesswork. Five of twelve cards absorbed, seven
still held.

**`ISS-023` narrowed, not closed.** The pink cards supplied the missing "so that" for
`FR-003` and `FR-004`, and the other two subjects are retired, so **the benefit half
is closed**. Criteria are still missing and the problem grew: the six green
operation stories are bare cards with neither role nor reason.

**Contracts are now covered; tax and AML still are not.** `FR-014` plus
`FR-026 Sign the artist contract` close the contract part of the legals gap left by
the `FR-002` split. `FR-026` has real criteria, taken from the brief's contract
sequence.

**Updated.** `FR-003`, `FR-004`, `FR-011` (benefit clauses merged in), `FR-006`,
`FR-007`, `ISS-017`, `ISS-023`, `GLO-011` (six more words for *piece* found in the
photographs; *item*, *art* and *picture* aliased, *painting* and *print* not, being
media), index.

## [2026-09-10] dashboard | The data model gets its visual half on every entity page

Gernot Starke: *"im still missing my graphical data model. Entities (basic
building blocks of data) is one aspect, visual representation another."*

**Checked before building.** The graphical model already existed and was
working: ADR-0027's projection renders a mermaid class diagram at `/data-model`
from ten `DM-` pages plus twelve marked glossary terms — **22 classes, 27
relationships**, with bounded-context filtering and a nav entry.

**The gap was on the entity pages themselves.** A `DM-` page rendered its
attributes and prose and **no picture at all**. Glossary terms have carried a
1-hop ego graph since ADR-0023 and context pages carry the context diagram;
data-model pages carried neither. So the entity was described in words on its own
page and only ever *shown* on a catalog page listing everything at once.

**The fix was wiring, not new machinery.** `build_data_model_full_diagram()`
already took a `focus` argument that keeps one entity and its direct neighbours —
written for exactly this and never called outside tests. `page_detail` now passes
`focus=stem` for `data-models` pages, and `detail.html` renders it above the body
with a link through to the whole model. One hop only, deliberately: drawing 22
classes on one entity's page would repeat the ADR-0026 readability regression.

**No ADR.** ADR-0027 already decided the projection and named this use of
`focus` ("what makes this readable in a room"). This is that decision being used,
not a new one.

**Tests.** Two added to `test_data_model_diagram.py`: an entity page renders a
class diagram containing itself and its direct neighbours but not the rest of the
vault, and a non-data-model page renders no class diagram. 16 pass in that file;
every test file passes in isolation.

**Verified against the running dashboard**, not just the test client: `/data-model`
serves the full diagram and all five spot-checked entity pages serve their own.

## [2026-09-11] dashboard | The data model diagram made findable from block 05

Gernot Starke: *"I need a button or obvious option to see the complete data model
diagram from the 'supporting models'."*

**Two changes, both following an existing precedent rather than inventing one.**

1. **`/req42/models` now draws the whole class diagram inline.** Block 03 Scope has
   always rendered the live-projected context diagram on its own block page; block
   05 Supporting Models is where the data model belongs, and it showed only a table
   of page titles. It now renders all 22 classes and 27 relationships above that
   table, with a link through to `/data-model` for bounded-context filtering and
   per-entity views.
2. **The home tile gained a second call to action.** "Supporting models" was a
   single whole-tile link to the page list, so the diagram was one click deeper
   than the list and invisible from the overview. It now carries two CTAs —
   *Model pages →* and *Data model diagram →* — the same shape the Glossary tile
   already uses for Table vs. Term network.

**No new ADR.** ADR-0027 decided the projection; ADR-0013 and ADR-0026 established
that a block page renders its own projected diagram. This applies both.

**Tests.** Two added to `test_data_model_diagram.py`: block 05 renders the whole
model unfiltered and links on to `/data-model`, and the home tile offers the
diagram alongside the page list. 18 pass in that file; every test file passes in
isolation.

**Verified against the running dashboard**, not only the test client: `/req42/models`
serves one class diagram with 22 classes and the onward link; the home tile serves
both CTAs.
