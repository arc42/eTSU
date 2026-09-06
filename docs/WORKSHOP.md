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

1. **`./reset.sh`** — wipes `wiki/`, the `raw/` inbox, and archived sources;
   restores `_system/index.md`, `_system/log.md` and `_system/wiki.yaml` to
   blank. Use this between separate workshop runs, or to fully restart after
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
