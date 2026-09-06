# Workshop Guide — Facilitator Script

This is written for **one facilitator driving a single shared vault on a
projector.** Participants do not clone this repo, do not install anything, and
do not run their own instance. They watch, they talk, they read the projected
screen — the facilitator's laptop is the only machine doing work. If you're
looking for individual setup instructions instead, see
[`docs/GETTING-STARTED.md`](GETTING-STARTED.md); this file is about running
the room, not about installing the tool.

## Pre-flight checklist (do this before the room fills up)

- [ ] **Docker is running**, or you've decided in advance to use
      `./dashboard.sh local` instead (see "If Docker won't start" below).
- [ ] **Claude Code is open in this folder and authenticated.** Confirm it
      responds to a trivial prompt before the group arrives.
- [ ] **`./dashboard.sh` opens clean** at `http://localhost:8080` and shows the
      empty-vault state (no leftover content from a previous run — if in
      doubt, run `./reset.sh --force` now).
- [ ] **Projector legibility.** Zoom the terminal and the browser to a size
      readable from the back row. Check both the chat window and the
      dashboard/Obsidian view at actual projected size, not just on your
      laptop screen.
- [ ] Have `raw/examples/interview-notes-example.md` ready as a fallback in
      case nobody has live material ready when you reach the ingest step.

## Suggested agenda (a 90-minute session)

| Time | Activity | Workflow |
|------|----------|----------|
| 0:00–0:10 | Welcome, explain the three layers (`raw/` → `wiki/` → schema), explain that the group drives content, the AI does the filing. | — |
| 0:10–0:25 | **Bootstrap.** Name the system live, write the vision, seed the first contested terms and one stakeholder. | `bootstrap.md` |
| 0:25–0:50 | **First ingest.** Bring in a real source if the group has one; otherwise copy `raw/examples/interview-notes-example.md` into `raw/` and ingest that. | `ingest.md` (grill-gated) |
| 0:50–1:00 | **Grill.** Pick one fuzzy requirement that came out of the ingest and run the grilling skill on it live, narrating the questions as they land. | grill-requirements skill |
| 1:00–1:15 | **Audit.** Run a health check over what exists so far; treat every finding as a talking point, not a defect. | `audit.md` |
| 1:15–1:25 | **Report.** Ask for a stakeholder matrix or an open-issues report — whichever the room seems to want closure on. | `report.md` |
| 1:25–1:30 | Wrap-up: show `_system/index.md` as the "what we built today" summary. | — |

Adjust freely — the value is in the group arguing about the domain, not in
hitting every row. If the room is engaged in the ingest step, let it run long
and cut the audit/report steps short rather than the reverse.

## What to narrate while the agent works

The group cannot see the reasoning happening inside the agent unless you say
it out loud. While a workflow runs:

- **During bootstrap** — read the vision sentence aloud as it's written; ask
  the room if it's still true once it's on screen.
- **During ingest** — narrate the grill gate explicitly: "it's going to
  stress-test this before writing anything, that's deliberate." When it
  proposes a glossary term or stakeholder, pause and ask the room to confirm
  or correct it before moving on — this is the moment participants feel
  ownership of the content.
- **When it raises an Issue** — call this out as a feature, not a failure:
  "it just found a contradiction instead of guessing which one of you is
  right." This is usually the most convincing five seconds of the whole
  session.
- **During audit/report** — treat the output as a checklist to react to live,
  not a wall of text to read verbatim.

## Recovery moves

Things will go sideways at least once. Know these three moves cold:

1. **`./reset.sh`** — wipes `wiki/` and everything a session added to `raw/`
   (the inbox, `raw/sources/`, `raw/ingested/` and any files dropped into
   `raw/assets/`), whatever the file extension; restores `_system/index.md`,
   `_system/log.md` and `_system/wiki.yaml` to their shipped state — index and
   log empty, `system_name` back to `eTSU`. The files the repo itself ships
   (the eTSU brand artwork in `raw/assets/`, `raw/examples/`) stay.
   Use this between separate workshop runs, or to fully restart after
   a session that went off the rails. Run `./reset.sh --force` if you're
   confident and want to skip the prompt (e.g. scripted resets between
   back-to-back sessions).
2. **`git checkout -- <path>`** — for a *partial* undo (one bad page, not the
   whole vault). Since the vault is a git repo, anything the agent wrote that
   you don't want to keep can be reverted file by file without a full reset.
   Good for "that one glossary term is wrong" without losing everything else
   from the session.
3. **`raw/examples/interview-notes-example.md`** — the safety net if live
   material isn't ready when you reach the ingest step. Copy it into `raw/`
   and ingest it instead; it's built with deliberate rough edges (two people
   using different words for the same thing, an unquantified quality wish, a
   contradiction, an unnamed stakeholder) so the group sees the agent surface
   real findings even from a canned source.

## If Docker won't start

Workshop laptops vary. If Docker is unavailable or misbehaving on the
facilitator machine, run `./dashboard.sh local` instead — it starts the same
Flask app directly in a local Python virtual environment, no Docker required.
Decide which mode you're using *before* the room fills up; switching mid-session
costs time you don't have. Both modes serve the same dashboard at
`http://localhost:8080` (Docker) or `http://localhost:8000` (`local`).

## Rehearsal log

A record of full "naked runs" — the whole workshop rehearsed end to end against
a throwaway clone. Add an entry each time the run is repeated.

### [2026-09-06] naked run

**Mode:** Docker (`./dashboard.sh`). The `local` fallback was **not** exercised
in this run — rehearse it separately before relying on it in the room.

**What worked.**

- Cold start from a fresh `git clone` needed nothing but Docker: build to
  serving in about 7 seconds, all 15 page routes HTTP 200 against a vault with
  zero pages, every one showing its deliberate empty state. Unknown pages
  (`/page/<folder>/<stem>`, `/functional-requirements/<stem>`) return 404, not
  500.
- Bootstrap: naming the system in `_system/wiki.yaml` re-branded the hero on
  the next refresh with no restart, exactly as the workflow promises. The
  glossary, stakeholder and req42 block counts moved as pages were written.
- Ingest of `raw/examples/interview-notes-example.md` produced 18 pages and
  updated 5 more. All four findings planted in that source were surfaced by the
  grill pass and filed as Issues rather than resolved: the two vocabularies for
  one concept, the unquantified "it should be fast", the reservation-loss
  contradiction, and the unnamed weekend colleague.
- **No template/parser drift.** Detail pages were rendered for all ten created
  content types and inspected section by section: every `**Definition.**`,
  `**Snapshot.**`, `**Purpose.**`, `**Attributes.**`, `**Relationships.**` and
  ATAM sub-bullet carried its content. Nothing came back blank.
- The term network rendered 10 nodes and 11 edges, including cross-type edges to
  data models, issues, stakeholders and constraints. The context diagram
  projected itself from stakeholder `provides:`/`receives:` with no context page
  written at all.
- `./reset.sh --force` returned `git status --short` to empty: 24 files created
  or modified, all gone, `raw/examples/` untouched. The dashboard served the
  naked state again immediately afterwards.

**Defects found and fixed.** Six, all committed separately:

1. Compose derived its project name from the `dashboard` directory, so starting
   this dashboard destroyed the container of any other vault at the same path.
   Pinned to `name: tsu-demo`.
2. ADR-0001 to ADR-0004 still carried the literal `{{date}}` placeholder, which
   `/adrs` renders verbatim.
3. `"Platzhalter"` — untranslated German — appeared on the **empty-vault home
   page**, the very first screen of the workshop. Four German source comments
   went with it.
4. `app.py` read a `tile_claim` field from the vision page that no template
   declared, so the Vision tile's claim line and the req42 block-01 sub-headline
   were permanently blank. Declared in `_templates/goal.md`; bootstrap step 3
   now fills it.
5. `/goals` printed "No goals yet" directly underneath the rendered goal — the
   empty state guards the *objectives* loop but was labelled "goals".
6. The Goal type showed as lowercase `goals` in search results; `FOLDER_LABELS`
   had no entry for that folder.

**Worth knowing for the day.**

- The dashboard's self-shutdown (ADR-0022) is real and quick: in this run the
  server stopped 17 seconds after start once the browser tab went away. If you
  close the projector tab to switch apps, the dashboard is gone — reopen with
  `./dashboard.sh`. Nothing is lost; it re-reads the vault on start.
- `reset.sh` deletes everything under `raw/` that is not committed to git —
  every extension, `raw/assets/` included. Do not park anything there you want
  to keep between runs; commit it, or keep it outside the vault.
