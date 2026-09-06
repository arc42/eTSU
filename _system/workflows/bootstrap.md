# Workflow: Bootstrap

Turn a naked vault into a working one in the first 30 minutes of a workshop.
Run this once, at the very start, before there is any real source to ingest.

## Not grill-gated

`ingest.md`'s grill gate applies to **ingesting sources** — it stress-tests new
material against a wiki that already has some shared vocabulary to push against.
A cold-start vault has none yet. Gating the very first page behind a grilling
pass would stall the workshop before it began, so bootstrap **skips the gate**.
Grilling resumes as normal from the first real `ingest.md` run onward.

## Steps

1. **Name the system.** Ask the group for a working name and a one-line tagline,
   then write both into `_system/wiki.yaml` (`system_name:`, `tagline:`). The
   dashboard reads this file live — the group sees the re-brand on its next
   refresh, no restart needed.
2. **Confirm the ubiquitous language.** Ask whether the group will work in
   English. If they want to capture requirements in their own domain language
   instead, write an ADR that supersedes
   [[0005-ubiquitous-language-english|ADR-0005]] and say so explicitly in
   `_system/index.md`'s ADR section. Otherwise proceed — English stays default.
3. **Capture the vision as `GOAL-001`.** Use `_templates/goal.md` with
   `stereotype: vision`, following the Geoffrey Moore frame: *for [target group]
   who [need], [system] is a [category] that [key benefit]*. This is the one
   goal page with no `parent:`; every objective captured later points at it.
4. **Capture the first glossary terms.** Ask the group: "what's a word you've
   already disagreed about?" Write a `GLO-NNN` page per term from
   `_templates/glossary-term.md`, even if `agreed: false` for now — a contested
   definition captured is worth more than a polished one deferred.
5. **Capture the first stakeholder.** At least one `STK-NNN` from
   `_templates/stakeholder.md` — whoever is in the room, or whoever they most
   often argue on behalf of.
6. **Update the bookkeeping.** Add every page created above to
   `_system/index.md` under its type heading, and append one entry to
   `_system/log.md`: `## [YYYY-MM-DD] bootstrap | <system name>` listing the
   pages created.
7. **Hand off to `ingest.md`.** Once the vault has a name, a vision, a handful
   of terms, and a stakeholder, bootstrap is done. Point the group at their
   first real source — a live interview, a dropped-in document, or, if nothing
   is ready yet, `raw/examples/interview-notes-example.md` — and proceed with
   the normal, grill-gated ingest workflow.

## Quality bar
Bootstrap is complete when `_system/wiki.yaml` is filled in, `GOAL-001` exists
and reads as a vision (not yet as a SMART objective — that comes later),
at least one glossary term and one stakeholder exist, and `_system/index.md` /
`_system/log.md` reflect all of it. If any of those five are still empty, the
group is not ready to ingest.
