#!/usr/bin/env python3
"""Concept-cluster audit — deterministic implementation of relations.md Tiers 1-2.

A single domain concept (e.g. "Kind") legitimately appears across several content
types as different lenses: a glossary term (what the word means), a data-model entity
(what we store), a stakeholder (what the actor wants). That is *projection*, not
redundancy — the right handling is to LINK the lenses, never to merge them.

This script finds those multi-lens clusters by grouping pages on normalized
`title` + `aliases`, then reports two things:

  1. RECIPROCAL-LINK GAPS (Tier 1/2, ~certain → auto-fixable): cluster members that
     do not reciprocally reference each other in `related:` / body wikilinks.
  2. DEFINITION LEADS per cluster (for the human drift review): the lead sentence of
     each lens side by side, so a reviewer can spot definitional drift — conflicting
     canonical meanings across lenses. Drift is a *content* contradiction → raise an
     ISS-NNN (audit.md), never auto-resolve.

Run from the repo root:  python3 _system/scripts/concept-cluster-audit.py
"""
import os
import re
import glob
from collections import defaultdict

WIKI = "wiki"
LEAD_LABELS = ["Definition", "Purpose", "Snapshot", "Identity"]
ID_RE = re.compile(r"\[\[([A-Z]{2,4}-\d{3})")


def parse(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", txt, re.S)
    if not m:
        return None
    fm, body = m.group(1), m.group(2)

    def field(name):
        mm = re.search(rf"^{name}:\s*(.*)$", fm, re.M)
        return mm.group(1).strip().strip('"').strip("'") if mm else ""

    idv = field("id")
    if not idv:
        return None
    aliases = []
    am = re.search(r"^aliases:\s*(\[.*\])\s*$", fm, re.M)
    if am:
        aliases = [a.strip().strip('"').strip("'")
                   for a in am.group(1).strip("[]").split(",") if a.strip()]
    leads = []
    for label in LEAD_LABELS:
        mm = re.search(rf"\*\*{label}\.\*\*\s*(.*?)(?:\n\n|\Z)", body, re.S)
        if mm:
            lead = re.sub(r"\s+", " ", mm.group(1)).strip()[:240]
            leads.append(f"{label}: {lead}")
    role = field("role")
    if role:
        leads.append(f"role(fm): {role[:240]}")
    return dict(
        path=path, id=idv, type=field("type"),
        title=field("title"), aliases=aliases,
        folder=os.path.basename(os.path.dirname(path)),
        refs=set(ID_RE.findall(fm)) | set(ID_RE.findall(body)),
        leads=leads,
    )


def norm(s):
    return s.lower().strip()


def main():
    pages = [p for p in (parse(f) for f in glob.glob(f"{WIKI}/**/*.md", recursive=True)) if p]
    title_index = defaultdict(list)
    for p in pages:
        title_index[norm(p["title"])].append(p)

    # cluster by title, bridged by aliases that equal another page's title
    clusters = {}
    for key, members in title_index.items():
        bag = list(members)
        for p in members:
            for a in p["aliases"]:
                for q in title_index.get(norm(a), []):
                    if q not in bag:
                        bag.append(q)
        clusters[key] = bag

    multi, seen = [], set()
    for key, members in clusters.items():
        ids = tuple(sorted(m["id"] for m in members))
        if ids in seen:
            continue
        seen.add(ids)
        if len({m["folder"] for m in members}) > 1 and len(members) > 1:
            multi.append((members[0]["title"], members))

    multi.sort(key=lambda x: -len(x[1]))
    print(f"=== {len(multi)} MULTI-LENS CONCEPTS (same title across >1 type) ===\n")

    gaps = []
    for title, members in multi:
        idset = {m["id"] for m in members}
        print(f"● '{title}'  ({len(members)} pages / {len({m['folder'] for m in members})} types)")
        for m in members:
            missing = (idset - {m["id"]}) - m["refs"]
            tag = "ok" if not missing else f"MISSING-> {','.join(sorted(missing))}"
            if missing:
                gaps.append((m["id"], sorted(missing)))
            print(f"    {m['id']:<10} [{m['folder']:<20}] links: {tag}")
        for m in members:
            for l in m["leads"][:2]:
                print(f"      ~ {m['id']}: {l}")
        print()

    print("=== TIER-1/2 RECIPROCAL-LINK GAPS (auto-fix candidates) ===")
    if not gaps:
        print("  none — every cluster is fully reciprocally linked.")
    for src, missing in gaps:
        print(f"  add {','.join('[['+x+']]' for x in missing)} to {src} related:")
    print("\n(Definition leads above are for human drift review — conflicting canonical")
    print(" meanings across lenses are a content contradiction → raise ISS-NNN, never auto-merge.)")


if __name__ == "__main__":
    main()
