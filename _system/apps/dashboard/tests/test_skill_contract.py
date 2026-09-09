"""The workflows and the installed skills are two halves of one contract.

`_system/workflows/` and `CLAUDE.md` tell the agent to activate skills by name.
Nothing checks that those skills are actually here, and the failure is silent in
the worst way: the agent reaches step 5 of an ingest, finds no `grilling` skill,
and quietly files Issues for questions the human was sitting right there to
answer. Nobody sees a stack trace. The wiki just gets a little worse.

Same shape as test_template_contract.py, one layer out: a name written in one
place, a directory that has to exist in another, and no runtime that complains
when they drift. Skills are vendored into the repo precisely so `git clone` is
the whole install — this test is what keeps that true.

Run from the dashboard dir:
    .venv/bin/python tests/test_skill_contract.py
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
SKILL_ROOTS = [REPO / ".claude" / "skills", REPO / ".agents" / "skills"]
DOCS = sorted((REPO / "_system" / "workflows").glob("*.md")) + [REPO / "CLAUDE.md"]

# "the **grilling** skill", "activate the `grill-requirements` skill" — a name
# in bold or backticks, immediately followed by the word "skill".
_REFERENCE_RE = re.compile(r"(?:\*\*|`)([a-z][a-z0-9-]*)(?:\*\*|`)\s+skill\b")
# a literal path to a skill file, e.g. `.claude/skills/grill-requirements/SKILL.md`
_PATH_RE = re.compile(r"`((?:\.claude|\.agents)/skills/[A-Za-z0-9._/-]*SKILL\.md)`")
_NAME_RE = re.compile(r"^name:\s*(\S+)\s*$", re.MULTILINE)


def _installed() -> dict:
    """Every skill on disk, by the `name:` in its frontmatter and by its
    directory name — an installer is free to disagree about which one wins, and
    a doc may reasonably cite either."""
    found = {}
    for root in SKILL_ROOTS:
        if not root.is_dir():
            continue
        for skill in sorted(root.glob("*/SKILL.md")):
            found[skill.parent.name] = skill
            m = _NAME_RE.search(skill.read_text(encoding="utf-8"))
            if m:
                found[m.group(1)] = skill
    return found


def _docs() -> list:
    present = [d for d in DOCS if d.is_file()]
    assert present, f"no workflow docs found under {REPO}"
    return present


def test_every_skill_the_docs_name_is_installed():
    """The failure this exists for: a workflow orders the agent to activate a
    skill that was never vendored, and the agent silently does without."""
    installed = _installed()
    assert installed, f"no skills found under {[str(r) for r in SKILL_ROOTS]}"
    missing = []
    for doc in _docs():
        for name in _REFERENCE_RE.findall(doc.read_text(encoding="utf-8")):
            if name not in installed:
                missing.append(f"{doc.relative_to(REPO)} -> {name}")
    assert not missing, \
        "docs name skills that are not installed in this repo: " + str(sorted(set(missing)))


def test_the_docs_reference_at_least_the_two_grills():
    """A guard on the regex, not on the repo. If the wording drifts so far that
    nothing matches, the test above starts passing vacuously and stops being
    worth having."""
    referenced = set()
    for doc in _docs():
        referenced |= set(_REFERENCE_RE.findall(doc.read_text(encoding="utf-8")))
    for expected in ("grill-requirements", "grilling"):
        assert expected in referenced, \
            f"no doc names the {expected!r} skill any more — did the wording change? {sorted(referenced)}"


def test_every_skill_path_the_docs_quote_exists():
    """Paths rot differently from names: a skill can be renamed or moved and the
    prose still reads correctly while the path underneath it points nowhere."""
    broken = []
    for doc in _docs():
        for rel in _PATH_RE.findall(doc.read_text(encoding="utf-8")):
            if not (REPO / rel).is_file():
                broken.append(f"{doc.relative_to(REPO)} -> {rel}")
    assert not broken, "docs quote skill paths that do not exist: " + str(sorted(set(broken)))


def test_every_installed_skill_declares_a_name():
    """Frontmatter `name:` is how a skill is addressed; one without it cannot be
    activated by the workflows no matter where it sits."""
    for root in SKILL_ROOTS:
        if not root.is_dir():
            continue
        for skill in sorted(root.glob("*/SKILL.md")):
            text = skill.read_text(encoding="utf-8")
            assert _NAME_RE.search(text), \
                f"{skill.relative_to(REPO)} has no `name:` in its frontmatter"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
        except AssertionError as exc:
            failed += 1
            print(f"FAIL {fn.__name__}: {exc}")
    if failed:
        sys.exit(1)
    print(f"ok — {len(fns)} checks, {len(_installed())} skill names installed")
