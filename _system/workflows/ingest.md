# Workflow: Ingest

Turn one raw source into typed, interlinked wiki knowledge.

## Before you ingest — mandatory: grill first

Every ingest is **gated by a grilling pass.** Before writing any page from a new
source, activate the **grill-requirements** skill (load and follow
`.claude/skills/grill-requirements/SKILL.md`) and stress-test the material against
the existing wiki — sharpen the ubiquitous language, expose contradictions and
gaps, and let decisions crystallise. Only once the grilling has settled the shared
understanding do you proceed to the steps below. Do not skip this gate, even for
sources that look obvious.

**Two grills, and they are not the same one.** `grill-requirements` (this gate)
stress-tests the *material* against the wiki before you write anything.
**`grilling`** (step 5) interviews the *human* to settle the questions that
survive the writing. The first gates starting an ingest; the second gates filing
an Issue.

**Language:** The ubiquitous language is English
([[0005-ubiquitous-language-english|ADR-0005]]). You may grill and ask in any
language, but every page you write below is captured **in English.**

## Steps

1. **Capture provenance.** Confirm the human's source file is in the `raw/` **inbox**
   (top level). Create a **slim** `SRC-NNN` provenance record from `_templates/source.md`
   — only frontmatter plus a one-line summary — in **`raw/sources/`** (ADR-0006). Compute
   a body sha256 for drift detection (`shasum -a 256 <file>`); record it in frontmatter.
   Keep narrative out of the record; that belongs in `_system/log.md` (step 7).
2. **Read & discuss.** Read the source fully. Surface the key takeaways to the
   human *before* writing pages. Agree on emphasis.
3. **Extract by type.** For each piece of requirements knowledge, decide its type
   (glossary / stakeholder / data-model / activity-model / use-case / user-story /
   feature / quality-requirement / constraint). Prefer extending an existing page
   over creating a near-duplicate — check `_system/index.md` first.
4. **Write / update pages.** Use the matching template. Assign the next free
   `TYPE-NNN`. Wikilink every cross-reference. If the page is the *same domain concept*
   as an existing page of another type (same slug/title — e.g. a `DM-` entity for an
   existing `GLO-` term), add the reciprocal `related:` link on **both** pages now
   (Tier 1 of `relations.md`, so the relationship audit stays cleanup). Link the source
   in `sources:` and add the page to the source's `ingested-pages:`. Apply the relevant
   `_system/anchors/` standard (goal frame, story format/quality, priority) and
   cite it; flag conformance gaps as Issues per step 5.
5. **Ask first, then flag.** Every contradiction with existing content, gap,
   ambiguity, untestable quality goal or missing stakeholder is a **question
   before it is an Issue.** Collect them all, then activate the **grilling**
   skill (Skill tool, `grilling`; the human starts the same interview with
   `/grill-me`) and put the whole frontier to the human in one numbered round,
   each question carrying your recommended answer. Look up anything the wiki
   can already answer yourself — finding facts is your job, deciding is theirs.

   Write whatever the human settles straight into the pages. Whatever they
   decline, defer, or cannot answer becomes an `ISS-NNN` linking both sides,
   exactly as before. **The gate is *try*, not *succeed*:** one round the human
   leaves unanswered is enough to fall back to Issues, so an ingest never
   blocks on an open question.

   The skill ships with this repo, in `.agents/skills/grilling/`. If it is not
   among your available skills anyway, **say so plainly** and file the Issues
   without it. A missing skill is a loud fallback, never a silent one.

   Never silently overwrite a conflicting claim, and never pick a side on your
   own. A grilled answer is the human deciding; an ungrilled one is you
   guessing.
6. **Update index.** Add/adjust entries in `_system/index.md` under the right type heading.
   If the session produced an ADR, also add its one-line entry to the
   **Architecture Decisions (ADR)** section (link via filename, displayed as `ADR-NNNN`).
7. **Append to `_system/log.md`.** `## [YYYY-MM-DD] ingest | <source title>` followed by a
   terse list of pages created/updated and issues raised.
8. **Archive the source (ADR-0008).** Move the ingested original from the `raw/` inbox
   to **`raw/ingested/`** and update the `SRC-NNN` `origin:` to its new path. This keeps
   the inbox to *un-ingested* sources only; the file's content (and thus its sha256) is
   unchanged, so drift detection still resolves it via `origin:`. Sources with no file
   (e.g. a verbal interview) skip this.

## Quality bar
A single ingest commonly touches 8–15 pages. If it touched only the source record,
you under-extracted. If you created duplicates, you skipped step 3. If every open
question became an Issue without the human ever being asked, you skipped step 5.
