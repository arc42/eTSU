# Index

Content catalog, one line per page, grouped by type. The agent updates this on
every ingest (`_system/workflows/ingest.md`, step 6).

## Glossary

- [GLO-001](../wiki/glossary/GLO-001-tour.md) — Tour: a sequence of Shows, contracted and shipped as one unit.
- [GLO-002](../wiki/glossary/GLO-002-show.md) — Show: one stop of a Tour at a single gallery.
- [GLO-003](../wiki/glossary/GLO-003-provenance.md) — Provenance: documented chain of ownership and custody; the evidence behind authenticity.
- [GLO-004](../wiki/glossary/GLO-004-tsu.md) — TSU: the art business — Head Office, galleries and staff.
- [GLO-005](../wiki/glossary/GLO-005-etsu.md) — eTSU: the digital product this wiki specifies; scope unsettled (ISS-004).
- [GLO-006](../wiki/glossary/GLO-006-conservator.md) — Conservator: cleans and conserves borrowed pieces at tour close; *cleaner* / *restorator* are aliases. **agreed**

## Goals

- [GOAL-001](../wiki/goals/GOAL-001-eTSU-vision.md) — Vision: digital tour and gallery management platform for Gus Renoir's business.
- [GOAL-002](../wiki/goals/GOAL-002-global-market-expansion.md) — Objective: global market reach for TSU artists; digital revenue share 15–20% in Year 1.
- [GOAL-003](../wiki/goals/GOAL-003-operational-excellence.md) — Objective: operational excellence in tour setup and settlement; setup lead time 3–4 weeks → ≤ 1 week.
- [GOAL-004](../wiki/goals/GOAL-004-trust-and-authentication.md) — Objective: authenticated provenance as a market differentiator; ≥ 90% verification coverage.
- [GOAL-005](../wiki/goals/GOAL-005-frictionless-global-art-trade.md) — Objective: real-time visibility of every piece on tour; metric not yet quantified (ISS-009).

## Stakeholders

- [STK-001](../wiki/stakeholders/STK-001-gus-renoir.md) — Gus Renoir, business owner / Head Office; also listed as "CEO / TSU management".
- [STK-002](../wiki/stakeholders/STK-002-artist.md) — Artist: creator whose work is shown and sold on a Tour.
- [STK-003](../wiki/stakeholders/STK-003-gallery-manager.md) — Gallery manager: runs one TSU gallery and the Shows hosted there.
- [STK-004](../wiki/stakeholders/STK-004-buyer.md) — Buyer: purchases a piece from a Show; deposit-and-balance payment sequence.
- [STK-005](../wiki/stakeholders/STK-005-shipper.md) — Shipper: one fine-art logistics provider per Tour.
- [STK-006](../wiki/stakeholders/STK-006-insurer.md) — Insurer: one insurer per Tour; insured values fixed in lending agreements.
- [STK-007](../wiki/stakeholders/STK-007-customs-authority.md) — Customs authority: clears pieces across each border; high influence, low interest.
- [STK-008](../wiki/stakeholders/STK-008-museum.md) — Museum: dual role — lends pieces and buys at the minimum museum sale price.
- [STK-009](../wiki/stakeholders/STK-009-conservator.md) — Conservator: conserves borrowed pieces at tour close, per lending agreement.
- [STK-010](../wiki/stakeholders/STK-010-legal-and-accounting.md) — Legal and accounting: contracts, commission settlement, tax and compliance.
- [STK-011](../wiki/stakeholders/STK-011-development-team.md) — Development team: builds eTSU; hidden from the context diagram.
- [STK-012](../wiki/stakeholders/STK-012-creative-genius.md) — Creative Genius: founder; originates every Tour concept.
- [STK-013](../wiki/stakeholders/STK-013-private-owner.md) — Private owner: lends a piece to a Tour under a lending agreement.
- [STK-014](../wiki/stakeholders/STK-014-art-collector.md) — Art collector: recurring private acquirer cultivated across tours; split from STK-004 (ISS-006).

## Context

- [CTX-001](../wiki/context/CTX-001-etsu-system-context.md) — eTSU system context; 10 interfaces after ISS-010 closed. Scope/non-goals blocked on ISS-004; a competing 6-neighbour sketch is held in ISS-018.

## External interfaces

*Captured as drawn per ADR-0026. Four nodes were deprecated on 2026-09-09 when ISS-010 closed — TSU's own operations are inside the boundary — leaving ten.*

- [EIF-001](../wiki/external-interfaces/EIF-001-artists.md) — Artists · supply · submissions in, sales & commission out.
- [EIF-002](../wiki/external-interfaces/EIF-002-museums-and-owners.md) — Museums & Owners · supply · loans in, loan status out. *Fuses two partners.*
- [EIF-003](../wiki/external-interfaces/EIF-003-appraisers-and-authenticators.md) — Appraisers & Authenticators · supply · verification requests out, results in. *New party, no earlier source.*
- ~~[EIF-004](../wiki/external-interfaces/EIF-004-customer-support-and-marketing.md) — Customer Support & Marketing~~ · **deprecated** — internal (ISS-010).
- [EIF-005](../wiki/external-interfaces/EIF-005-fraud-and-security-prevention.md) — Fraud & Security Prevention · support · AML screening.
- ~~[EIF-006](../wiki/external-interfaces/EIF-006-business-growth-and-content.md) — Business Growth & Content~~ · **deprecated** — internal (ISS-010); the photography/3D supplier is left to ISS-012.
- ~~[EIF-007](../wiki/external-interfaces/EIF-007-data-and-analytics.md) — Data & Analytics~~ · **deprecated** — an eTSU capability (ISS-010).
- [EIF-008](../wiki/external-interfaces/EIF-008-individual-buyers.md) — Individual Buyers · demand · retail purchases.
- [EIF-009](../wiki/external-interfaces/EIF-009-global-online-buyers.md) — Global Online Buyers · demand · new markets. *Presumes Reading B of ISS-004.*
- [EIF-010](../wiki/external-interfaces/EIF-010-institutional-buyers.md) — Institutional Buyers · demand · museums, corporate collections.
- ~~[EIF-011](../wiki/external-interfaces/EIF-011-gallery-operations.md) — Gallery Operations~~ · **deprecated** — this is TSU itself (ISS-010); the "6 locations" figure survives on the page.
- [EIF-012](../wiki/external-interfaces/EIF-012-logistics-and-fulfillment.md) — Logistics & Fulfillment · core · shipping, insurance, restoration. *Fuses three partners.*
- [EIF-013](../wiki/external-interfaces/EIF-013-technology-and-infrastructure.md) — Technology & Infrastructure · core · **narrowed** to the payment provider; cloud/CDN/security dropped as internal (ISS-010).
- [EIF-014](../wiki/external-interfaces/EIF-014-regulatory-and-compliance.md) — Regulatory & Compliance · core · tax, AML/KYC, law enforcement. *Customs missing.*

## Data models

## Activity models

## Use cases

## Functional requirements

## Quality requirements

## Constraints

## Issues

- [ISS-001](../wiki/issues/ISS-001-competing-vision-statements.md) — Two competing vision statements: Moore format vs. the "new Picasso" line. *(major, contradiction)*
- [ISS-002](../wiki/issues/ISS-002-unsourced-objective-baselines.md) — Objective baselines and targets asserted with no source. *(major, gap)*
- [ISS-003](../wiki/issues/ISS-003-year-one-vs-2029-target-divergence.md) — Year-1 targets and the 2029 narrative diverge on five metrics. *(minor, contradiction)*
- [ISS-004](../wiki/issues/ISS-004-scope-inflation-marketplace-vs-back-office.md) — Is eTSU a back-office tool or a global consumer marketplace? *(blocker, risk)*
- [ISS-005](../wiki/issues/ISS-005-ungrounded-stakeholder-entries.md) — Six workshop stakeholder entries have no identifiable relationship to eTSU. *(minor, question)*
- [ISS-006](../wiki/issues/ISS-006-buyer-versus-art-collector.md) — Are "buyer" and "art collector" one role or two? **resolved 2026-09-09 — two roles** *(minor, ambiguity)*
- [ISS-007](../wiki/issues/ISS-007-cleaner-versus-restorer.md) — "cleaners / restorer" fuses two unrelated roles. **resolved 2026-09-09 — one role, the conservator** *(minor, ambiguity)*
- [ISS-008](../wiki/issues/ISS-008-thomas-marti-email-arrived-empty.md) — Thomas Marti's eTSU email arrived with an empty body. **wontfix 2026-09-09 — ignored** *(minor, gap)*
- [ISS-009](../wiki/issues/ISS-009-real-time-metric-untestable.md) — GOAL-005's "real time" metric is untestable; overlaps GOAL-002/003. *(major, ambiguity)*
- [ISS-010](../wiki/issues/ISS-010-system-boundary-undefined.md) — The context diagram draws TSU's own operations outside the system boundary. **resolved 2026-09-09 — a drawing mistake; 4 nodes deprecated** *(blocker, ambiguity)*
- [ISS-011](../wiki/issues/ISS-011-context-flows-inferred-not-sourced.md) — Every context flow inferred from box labels; no arrow carries a payload. *(major, gap)*
- [ISS-012](../wiki/issues/ISS-012-bundled-eif-nodes-hide-partners.md) — Four EIF nodes each bundle two or more distinct partners; customs missing. *(major, ambiguity)*
- [ISS-013](../wiki/issues/ISS-013-three-way-buyer-segmentation.md) — A third buyer segmentation appears; supersedes ISS-006. *(major, contradiction)*
- [ISS-014](../wiki/issues/ISS-014-legacy-issue-ids-referenced-by-starter-adrs.md) — Starter ADRs reference issue IDs absent from this vault. *(minor, question)*
- [ISS-015](../wiki/issues/ISS-015-a-new-picasso-is-undefined.md) — "A new Picasso" is undefined and unmeasurable in the candidate vision. *(major, ambiguity)*
- [ISS-016](../wiki/issues/ISS-016-moore-format-cited-without-an-anchor.md) — The Moore vision format is cited by the template but has no semantic anchor. *(minor, gap)*
- [ISS-017](../wiki/issues/ISS-017-twelve-candidate-capabilities-undefined.md) — Twelve capability cards named, none defined; holds the transcribed list. *(major, gap)*
- [ISS-018](../wiki/issues/ISS-018-competing-context-diagrams.md) — Two competing context diagrams: 14-node ecosystem vs. 6-neighbour eTSU sketch. *(blocker, contradiction)*
- [ISS-019](../wiki/issues/ISS-019-visitors-is-an-undefined-actor.md) — "Visitors" is drawn as a primary actor but defined nowhere. *(major, ambiguity)*
- [ISS-020](../wiki/issues/ISS-020-sketch-boxes-untyped.md) — PAYMENT / INVOICE / DELIVERY / SOCIAL MEDIA drawn as boxes but never typed. *(minor, ambiguity)*
- [ISS-021](../wiki/issues/ISS-021-authentication-card-ambiguous.md) — The "authentication" card: artwork authentication or user log-in? *(major, ambiguity)*

## Sources

- [SRC-001](../raw/sources/SRC-001-ulrich-stuerzlinger-goals-and-newspaper.md) — Email: TSU — Goals and Newspaper (Ulrich Stürzlinger), 2026-09-09.
- [SRC-002](../raw/sources/SRC-002-georg-mayrhauser-vision-goals-stakeholders.md) — Email: Vision / Goals / Stakeholders, Req4Arc Workshop Linz (Georg Mayrhauser), 2026-09-09.
- [SRC-003](../raw/sources/SRC-003-thomas-marti-etsu-empty.md) — Email: eTSU (Thomas Marti), 2026-09-09 — empty body, see ISS-008.
- [SRC-004](../raw/sources/SRC-004-ulrich-stuerzlinger-context-diagram.md) — Email: Context Diagram (Ulrich Stürzlinger), 2026-09-09 — 14-node business ecosystem diagram (PNG).
- [SRC-005](../raw/sources/SRC-005-workshop-capability-card-wall.md) — Workshop photo: capability card wall, Req4Arc Linz, 2026-09-09 — 12 handwritten cards, author unattributed.
- [SRC-006](../raw/sources/SRC-006-workshop-etsu-context-sketch.md) — Workshop photo: hand-drawn eTSU context sketch, Req4Arc Linz, 2026-09-09 — 6 neighbours, author unattributed.

## Architecture Decisions (ADR)

- [0000-template](adr/0000-template.md) — ADR-0000, the Nygard template
- [0001-record-architecture-decisions](adr/0001-record-architecture-decisions.md) — ADR-0001, record every structural decision as an ADR in `_system/adr/`, using the Nygard format
- [0002-content-type-taxonomy](adr/0002-content-type-taxonomy.md) — ADR-0002, the typed wiki content types (glossary term, stakeholder, data model, activity model, use case, user story, feature, quality requirement, constraint, issue, plus source), drawing on DDD, arc42, ISO 25010 and ATAM
- [0003-issues-as-meta-type](adr/0003-issues-as-meta-type.md) — ADR-0003, Issue as a first-class content type that cross-cuts all others, raised instead of silently resolving contradictions
- [0004-semantic-anchors](adr/0004-semantic-anchors.md) — ADR-0004, reusable methodological standards (SMART, PAM, user-story-format, INVEST, MoSCoW) kept as semantic anchors in `_system/anchors/`, cited by alias
- [0005-ubiquitous-language-english](adr/0005-ubiquitous-language-english.md) — ADR-0005, the ubiquitous language of this wiki is English
- [0006-provenance-records-location](adr/0006-provenance-records-location.md) — ADR-0006, slim provenance records live in `raw/sources/`, separate from human-curated originals and from the log's narrative
- [0007-req42-as-umbrella-anchor](adr/0007-req42-as-umbrella-anchor.md) — ADR-0007, req42 is the umbrella anchor and methodological reference for the wiki's content types
- [0008-raw-inbox-ingested-archive](adr/0008-raw-inbox-ingested-archive.md) — ADR-0008, `raw/`'s top level is an inbox for new sources; ingested originals move to `raw/ingested/`
- [0009-context-and-external-interface-types](adr/0009-context-and-external-interface-types.md) — ADR-0009, introduces the Context (scope) and External interface content types for system boundary and real external systems
- [0010-stakeholder-aliases-field](adr/0010-stakeholder-aliases-field.md) — ADR-0010, adds an optional `aliases:` field to the stakeholder template for alternate names
- [0011-method-and-reference-layer](adr/0011-method-and-reference-layer.md) — ADR-0011, separates reusable method/reference knowledge from domain knowledge, split between anchors and `docs/`
- [0012-functional-requirement-stereotypes](adr/0012-functional-requirement-stereotypes.md) — ADR-0012, merges feature and user story into one Functional requirement type with stereotype `epic | feature | story`
- [0013-data-flows-as-edges-context-diagram-as-projection](adr/0013-data-flows-as-edges-context-diagram-as-projection.md) — ADR-0013, the context diagram is projected from typed data-flow edges rather than stored directly
- [0014-context-diagram-actor-roles-and-shapes](adr/0014-context-diagram-actor-roles-and-shapes.md) — ADR-0014, the context diagram distinguishes human actors from systems/organizations by shape and collapses duplicate context-level roles
- [0015-backlog-naming-convention](adr/0015-backlog-naming-convention.md) — ADR-0015, backlog naming convention: epics and features are named as nouns, stories and use cases as verb phrases
- [0016-goals-content-type](adr/0016-goals-content-type.md) — ADR-0016, introduces the Goal content type for req42 Block 01 (vision and objectives)
- [0017-functional-requirement-lane-field](adr/0017-functional-requirement-lane-field.md) — ADR-0017, adds a `lane:` field to functional requirements for story-map swimlanes when the backlog spans multiple surfaces
- [0018-projections-from-typed-edges](adr/0018-projections-from-typed-edges.md) — ADR-0018, diagrams and cross-cutting matrices are generated as projections of typed edges rather than hand-maintained
- [0019-data-model-product-and-sum-types](adr/0019-data-model-product-and-sum-types.md) — ADR-0019, data-model stereotypes distinguish product types (all fields present) from sum types (one-of variants)
- [0020-master-data-as-configuration](adr/0020-master-data-as-configuration.md) — ADR-0020, master data is loaded by file import, with runtime CRUD limited to specific owners and no soft-delete
- [0021-file-format-specs-at-boundary-owner](adr/0021-file-format-specs-at-boundary-owner.md) — ADR-0021, a data flow's file-format spec lives with whichever content type owns that boundary, not as a separate content type
- [0022-dashboard-self-shutdown-lifecycle](adr/0022-dashboard-self-shutdown-lifecycle.md) — ADR-0022, the dashboard shuts itself down when its browser tab closes (heartbeat + pagehide beacon) instead of running as a persistent background service
- [0023-glossary-term-network-force-graph](adr/0023-glossary-term-network-force-graph.md) — ADR-0023, the dashboard renders the glossary as an interactive client-side force-directed graph for viewers without Obsidian
- [0024-graphical-brand-requirements](adr/0024-graphical-brand-requirements.md) — ADR-0024, routes graphical/brand requirements to existing content types (Constraint, Functional requirement, Quality requirement, Issue) plus `raw/` for assets, rather than inventing a new type
- [0025-dashboard-req42-home-and-visual-identity](adr/0025-dashboard-req42-home-and-visual-identity.md) — ADR-0025, the dashboard's home page follows req42's reading order with a persistent nav, a flat vendored-font identity, maturity bars, issue flags, a QR join code and provenance chips
- [0026-context-diagram-captured-as-drawn](adr/0026-context-diagram-captured-as-drawn.md) — ADR-0026, the workshop context diagram is captured as drawn (one `EIF` per box, `tier:` field added), superseding ADR-0013's "systems only" admission rule for CTX-001; corrections carried as Issues. *Amended:* the projection draws one labelled line per neighbour with `short_title:`/`label:` short labels and a flow table beneath
