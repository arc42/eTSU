# Requirements Wiki — Starter

You bring the raw material; the AI agent files it.

## The pattern

This vault follows the Karpathy three-layer LLM-wiki pattern. `raw/` holds your
immutable sources — interview notes, transcripts, specs — which you drop in and
never edit. `wiki/` holds the structured, interlinked requirements knowledge
(glossary, stakeholders, use cases, stories, and more) that the AI agent reads
sources into and keeps current. A schema layer — `CLAUDE.md`, `_templates/`,
`_system/anchors/` — defines the content types and conventions both layers share,
and evolves with you over time.

## Quick start

1. Run `./dashboard.sh` to start the live dashboard (Docker) at
   `http://localhost:8080` — a browsable view of the wiki, useful even while it's
   still empty. No Docker on this machine? `./dashboard.sh local` runs it
   directly with Python at `http://localhost:8000`.
2. Open this folder in Obsidian (**Open folder as vault**) to navigate and
   graph-view the wiki directly.
3. Point Claude Code at this same folder — it reads `CLAUDE.md` automatically and
   discovers the bundled skills in `.claude/skills/`.

For a full walkthrough, see [`docs/GETTING-STARTED.md`](docs/GETTING-STARTED.md).
If you're running this as a workshop, see [`docs/WORKSHOP.md`](docs/WORKSHOP.md).

