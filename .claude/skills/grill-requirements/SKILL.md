---
name: grill-requirements
description: >
  A grilling session that stress-tests a requirements plan, draft, or idea against
  the existing requirements wiki — sharpening the ubiquitous language, exposing
  contradictions and gaps, and updating wiki pages, Issues, and ADRs inline as
  decisions crystallise. Claude MUST invoke this skill on its own before writing any
  wiki page from a new or changed source — every ingest is grill-gated (CLAUDE.md,
  `_system/workflows/ingest.md`) — and SHOULD invoke it whenever requirements are being
  captured, refined, or pressure-tested. Also use when the user asks to pressure-test
  thinking ("grill me on this feature", "stress-test these requirements", "challenge my
  plan against what we know") or when ingesting a source (interview, transcript, spec,
  ticket) into the wiki. Adapted from mattpocock/skills grill-with-docs for
  requirements engineering.
---

**When to invoke.** This skill is the ingest gate, not just a user command. Before any
new or changed source becomes wiki pages, run it first to stress-test the material —
invoke it **on your own initiative, without waiting to be asked** — and also whenever a
requirement is being captured, refined, or challenged (CLAUDE.md,
`_system/workflows/ingest.md`). The user can still trigger it explicitly; you no longer
need them to.

Interview the user relentlessly about every aspect of this plan until you reach a
shared, precise understanding. Walk down each branch of the decision tree, resolving
dependencies between decisions one by one. For each question, provide your
recommended answer.

Ask the questions **one at a time**, waiting for feedback on each before continuing.

If a question can be answered by exploring the wiki or the `raw/` sources, explore
them instead of asking.

**Language ([[0005-ubiquitous-language-english|ADR-0005]]):** The ubiquitous
language is English. You may grill and ask in **any language** — whatever flows
best with the human — but anything you write into the wiki (terms, requirements,
Issues, ADRs) is captured **in English.**

## Orient first

Find the vault root (`CLAUDE.md`, `raw/`, `wiki/`, `_templates/`, `_system/`). Read
`CLAUDE.md` for the schema, skim `_system/index.md` for what already exists, and note the
`_system/anchors/` standards in play (SMART, PAM, user-story-format, INVEST, MoSCoW).
The wiki is your source of truth the way a codebase is for the original skill.

Create or update pages lazily — only when a decision has actually crystallised.

## During the session

### Challenge against the glossary
When the user uses a term that conflicts with `wiki/glossary/`, call it out
immediately. "Your glossary defines *cancellation* as X, but you seem to mean Y —
which is it?" If a needed term has no glossary entry yet, propose one.

### Sharpen fuzzy language
When the user is vague or overloaded, propose a precise canonical term. "You say
*account* — do you mean the [[STK-...]] Customer or the User? Those are different."
Drive toward the ubiquitous language.

### Probe with concrete scenarios
Stress-test relationships and flows with specific, edge-case scenarios that force
precision about boundaries — exactly the cases a use case's alternate flows or a
data model's invariants must cover.

### Apply the anchors as a precision lens
- Goals: push for [[PAM]] (purpose/advantage/metric) or full [[SMART]]. "What's the
  metric that tells us this worked?"
- Stories: test against [[user-story-format]] and [[INVEST]] — real role? genuine
  benefit? testable? small enough?
- Quality requirements: demand a quantified measure — no measure means untestable.
- Priorities: challenge every `Must` against [[MoSCoW]]. "Does the release truly
  fail without this, or is it a Should?"

### Cross-reference against the wiki
When the user states how something works, check whether existing pages or `raw/`
sources agree. On contradiction, surface it and raise an `ISS-NNN` linking both
sides — do not pick a winner. "UC-007 says partial cancellation is allowed, but you
just said all-or-nothing — which is right?"

### Update the wiki inline
When a term, requirement, or decision resolves, capture it right then in the proper
typed page (per its template and anchors) — don't batch. Append the session's
touches to `_system/log.md`. Keep pages free of implementation detail; record only what is
meaningful at the requirements level.

### Offer an ADR sparingly
Only offer an `_system/adr/` record when all three hold:
1. **Hard to reverse** — changing course later is costly.
2. **Surprising without context** — a future reader will ask "why this way?"
3. **A real trade-off** — genuine alternatives existed and one was chosen for reasons.

If any is missing, skip it. Structural decisions about the wiki itself are also ADRs.
When you do write one, list it in the **Architecture Decisions (ADR)** section of
`_system/index.md` (one line, link via filename, displayed as `ADR-NNNN`).
