# Filtered graph views (Obsidian workspaces)

The Obsidian graph only stores **one** configuration globally
(`.obsidian/graph.json`). **Groups** only colour nodes in — they don't remove
any. To **narrow** the graph down to specific nodes, use the search field in
the **Filters** section of the graph settings (above).

To reuse several such filters, we save them as named **workspaces** (core
plugin "Workspaces"). A workspace saves the entire layout, including the
graph filter. The saved layouts live in `.obsidian/workspaces.json`.

## Existing graph workspaces

| Workspace | Filter (`search`) | Shows |
|---|---|---|
| **Graph: Glossary + Goals** | `["type":"glossary"] OR ["type":"goal"]` | GLO and GOAL nodes (green / gold) |
| **Graph: Epics + FRs** | `["type":"functional-requirement"]` | all FRs, coloured by stereotype epic/feature/story |
| **Graph: Term (everything about it)** | `GLO-006-entity-e` | that term + every page that links to it |
| **Graph: Data Models** | `["type":"data-model"]` | all DM nodes |

## Loading

1. `Cmd+P` → **Workspaces: Load workspace** (or the ribbon icon) → pick one of
   the four.
2. Back to the normal layout: load/save a regular workspace.

> If `workspaces.json` was written externally (e.g. by an agent) while
> Obsidian is running, Obsidian first needs to re-read the file:
> `Cmd+P` → **Reload app without saving**. **Don't save a workspace before
> that**, or Obsidian will overwrite the new file with the old saved state.

## Filter syntax (cheat sheet)

The filter field uses the same search syntax as the global search.

- `path:wiki/glossary` — a single folder only
- `["type":"goal"]` — by frontmatter **property** (robust even if files move)
- `["status":"accepted"]` — by status
- `tag:#data-model` — by tag (with `#`)
- `A OR B` — union (**`OR` must be capitalized**; `or` is a regular word)
- `-["status":"deprecated"]` — exclusion
- `GLO-006-entity-e` — the node itself **plus** every page whose text
  contains this wikilink (relies on the convention "every reference is a real
  link")

## Creating a new graph workspace

1. Open the graph, enter the desired expression into the **Filters** field,
   optionally set colours under **Groups**.
2. `Cmd+P` → **Workspaces: Save workspace as…** → give it a descriptive name
   (convention here: prefix `Graph: …`).

> Note: a workspace saves the **entire** layout, not just the graph. The four
> graph workspaces above inherit the side panels from the standard layout.
> Loading one therefore also rearranges the pane layout.
