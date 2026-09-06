# Getting Started — Capturing Requirements

A practical guide for a product owner who wants to start turning raw material —
interview notes, transcripts, specs, tickets — into a structured, living
requirements wiki. You curate and ask; the AI does the filing.

## The idea in one paragraph

You drop sources into a folder. You tell the AI to "ingest" them. It reads each
one and builds interlinked pages — glossary terms, stakeholders, use cases, user
stories, features, quality requirements, constraints — and flags every open
question as an **Issue**. Nothing is re-derived from scratch later: the knowledge
is compiled once and kept current as you add more. You browse it in Obsidian.

## One-time setup (~5 minutes)

1. **Clone or download this repo.** You get one folder — the repo root — that is
   *both* your knowledge base and the AI's workspace.
2. **Open it in Obsidian** (Open folder as vault → pick the repo root). No
   plugins to install — you navigate with the built-in file list and **graph view**.
   The hidden `.claude/` folder won't show up in Obsidian.
3. **Point your AI agent at the same folder.** Launched there, Claude Code reads
   `CLAUDE.md` automatically and discovers both skills in `.claude/skills/`.

That's it. You won't hand-write wiki pages, and you won't configure anything — the
AI creates and maintains every page itself.

## Your daily loop

### 1. Capture a source
Save anything worth keeping into the `raw/` folder: a meeting transcript, a
stakeholder email, a draft spec, a screenshot. (The Obsidian **Web Clipper**
extension saves web pages straight there.) These files are never edited — they're
your source of truth.

### 2. Ingest it
Tell the agent: **"Ingest the new file in raw/."**
It will read the source, talk through the key takeaways with you, then write or
update pages across the wiki — typically 8–15 of them — and raise Issues for
anything unclear. Watch it happen live in Obsidian's file list and graph view.

### 3. Review what it built
Open `_system/index.md` for the catalog, or use the **graph view** to see how everything
connects. Follow the links. If something's off, just tell the agent. Prefer a browser
to Obsidian? Run `./dashboard.sh` for a live, read-only view of the same wiki —
handy for a quick check or for showing someone else without installing anything.

### 4. Check what's still unknown
Ask **"Report open issues."** The AI reads the `wiki/issues/` folder and gives you
the current list of open questions, contradictions, and gaps — always up to date,
since it's generated fresh each time. This is your "what do we still need to nail
down?" view. **The AI never silently resolves an ambiguity — it asks you.** (You can
also just browse the `wiki/issues/` folder directly.)

### 5. When you're unsure, get grilled
Before committing to a feature or when a requirement feels fuzzy, say
**"Grill me on this."** The AI runs a focused interview — one question at a time,
each with its recommended answer — challenging your wording against the agreed
vocabulary, poking at edge cases, and pushing every goal toward a measurable form
and every "must-have" toward an honest priority. As answers firm up, it writes them
straight into the wiki and flags leftover questions as Issues. It's the fastest way
to turn a half-formed idea into clean, captured requirements.

### 6. Periodically, tidy up
Say **"Audit the wiki."** It checks for contradictions, stale claims, orphaned
pages, broken links, untestable quality requirements, and goals or stories that
don't meet the quality bar — and queues anything needing your judgment as an Issue.

### 7. Report when you need a view
Ask for what you need, e.g.:
- *"Report open issues by severity."*
- *"Show requirements coverage"* (which features lack stories/use-cases).
- *"Give me the stakeholder matrix."*
- *"Trace this stakeholder's goals down to the user stories."*

## What gets captured (the content types)

| Type | What it holds |
|------|---------------|
| **Glossary** | The shared vocabulary — one agreed meaning per term. |
| **Stakeholder** | A simplified persona: goals, concerns, influence/interest. |
| **Data model** | Entities, attributes, relationships. |
| **Activity model** | A process: trigger → steps → outcome. |
| **Use case** | An actor's goal with main and alternate flows. |
| **Functional requirement** | A backlog item, stereotyped **epic / feature / story**, in an Epic→Feature→Story hierarchy (story format + acceptance criteria for stories). |
| **Quality requirement** | A measurable target (performance, security, …). |
| **Constraint** | A fixed limit on the solution. |
| **Issue** | An open question, contradiction, or gap — tracked until resolved. |

## A few good habits

- **Ingest one source at a time** when starting out, and stay in the loop — you'll
  learn what the AI emphasizes and can steer it.
- **Don't pre-organize your sources.** Drop them in raw; let the AI do the filing.
- **Treat Issues as your to-do list.** When the open-issues board is empty, your
  requirements are as settled as your current sources allow.
- **It's just a git repo of markdown.** Commit often; you get full history and can
  branch for free.

## Where things live

```
.                        ← repo root = the vault; open this in both Obsidian and your AI agent
├── wiki/               ← the AI-maintained requirements (one folder per type)
├── raw/                ← you drop sources here (AI never edits these)
│   └── examples/       ← optional worked examples to seed a workshop
├── _templates/         ← page structures the AI follows when filing
├── _system/            ← workflows, ADRs, anchors, index.md & log.md (bookkeeping)
│   └── wiki.yaml       ← project identity (system name, tagline) read by the dashboard
├── docs/               ← this guide and other human documentation
├── .claude/skills/     ← the two AI skills (hidden in Obsidian)
├── CLAUDE.md           ← the AI's schema/rules (read first if curious)
├── README.md           ← repo overview
├── dashboard.sh        ← starts the live, browsable dashboard (Docker)
└── reset.sh            ← DESTRUCTIVE: deletes every page in wiki/ and every source in
                        raw/, then restores index.md, log.md and wiki.yaml to their
                        shipped state. See "Starting over" below.
```

Most of these are de-emphasized in Obsidian (see "Keeping the vault clean" below), so
day to day you mostly see `wiki/` and `raw/`.

You only ever *touch* `raw/`. Everything in `wiki/` is the AI's job.

## Keeping the vault clean

The repo ships with an Obsidian setting (in `.obsidian/app.json`) that **excludes**
the machinery — `_system/`, `_templates/`, `docs/`, `CLAUDE.md`, `README.md` — from
graph view, search, quick-switcher, and link autocomplete. So when you browse or
graph, you see requirements content, not bookkeeping. The `.claude/` skills folder is
hidden automatically (dot-folder).

These files still appear, greyed, in the left file-tree pane — Obsidian can't fully
hide them there without a plugin, and the repo deliberately uses none. If you want a
spotless tree, the community plugin *File Hider* will do it; otherwise the `_` prefix
keeps the machinery sorted together and out of your way.

To adjust what's excluded: Settings → Files and links → Excluded files.

## Starting over

`./reset.sh` returns the vault to the naked state it shipped in. It is
**irreversible and it deletes content**:

- every page in `wiki/`,
- every source in `raw/` — the inbox, `raw/sources/`, `raw/ingested/` and any
  participant files under `raw/assets/` (`raw/examples/` and the repo's own
  committed assets survive),
- and it restores `_system/index.md`, `_system/log.md` and `_system/wiki.yaml`
  to their shipped state — index and log empty, `system_name` back to `eTSU`.

None of that is in git yet unless you committed it, so there is nothing to
recover afterwards. It asks for confirmation first; `./reset.sh --force` skips
the prompt. Use it between separate engagements, not as an undo.

For a *partial* undo — one bad page rather than the whole vault — use
`git checkout -- <path>` instead.
