"""Light/dark theme contract — no pytest dependency.

The theme is pure CSS custom properties: :root carries the dark palette and
:root[data-theme="light"] overrides it. That design has exactly one failure
mode, and it is silent — add a token to one block and forget the other, and
the missing side falls back to the dark value. A navy pane on a white page or
pale mint label text on white renders without an error anywhere; nothing but
a human looking at the page would catch it.

This test locks the two blocks to the same key set, and pins the three moving
parts the palette cannot cover on its own: the pre-paint stamp in <head>, the
footer control, and mermaid's re-render hook (mermaid bakes its colours into
the SVG at render time, so it does not follow a variable swap).

Run from the dashboard dir:
    .venv/bin/python tests/test_theme.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = (ROOT / "static" / "style.css").read_text(encoding="utf-8")
BASE = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
MERMAID = (ROOT / "templates" / "_mermaid.html").read_text(encoding="utf-8")

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)


def tokens(selector):
    """The custom-property names declared in one palette block."""
    m = re.search(re.escape(selector) + r"\s*\{(.*?)\n\}", CSS, re.S)
    assert m, f"palette block not found: {selector}"
    return set(re.findall(r"^\s*(--[a-z0-9-]+)\s*:", m.group(1), re.M))


dark = tokens(":root")
light = tokens(':root[data-theme="light"]')

# --radius is geometry, not colour, and is deliberately declared once.
GEOMETRY = {"--radius"}

missing_in_light = dark - light - GEOMETRY
check(not missing_in_light,
      f"declared in :root but not in the light palette (they will keep their "
      f"dark value on a light page): {sorted(missing_in_light)}")

extra_in_light = light - dark
check(not extra_in_light,
      f"declared only in the light palette, so the dark theme has no value "
      f"for them: {sorted(extra_in_light)}")

check(len(dark) > 25, f"expected a full token palette, found {len(dark)} in :root")

# Structural colours must go through a token. Translucent accent washes are the
# deliberate exception -- they tint whatever surface they sit on, so they read
# correctly against both grounds (see the palette comment in style.css), and
# rgba() is therefore not scanned here. Opaque hex is.
after_palette = CSS.split(':root[data-theme="light"]', 1)[-1]
after_palette = after_palette.split("\n}", 1)[-1]
HEX = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b")
# The saturated graph/legend swatches are shared by both themes on purpose:
# mid-tone fills stay legible on either ground. Anything else is a bug.
allowed = re.compile(r"\.(layer-|lg-|tile-adrs|bz-)")
VAR = re.compile(r"var\([^)]*\)")   # drops var(--x) and its hex fallback alike
leaked = [
    ln.strip() for ln in after_palette.splitlines()
    if HEX.search(VAR.sub("", ln)) and not allowed.search(ln)
]
check(not leaked, "opaque hex colour outside the palette blocks: " + "; ".join(leaked[:3]))

# The stamp must run in <head>, before the stylesheet, or a light-theme reload
# flashes the dark palette.
head = BASE.split("</head>", 1)[0]
check("etsu-theme" in head, "the theme stamp is not in <head>")
check(head.index("localStorage.getItem") < head.index("style.css"),
      "the theme stamp must precede the stylesheet link, or the page flashes")

check('id="theme-toggle"' in BASE, "the footer theme control is missing")
if 'id="theme-toggle"' in BASE:
    check(BASE.index('id="theme-toggle"') < BASE.index("</footer>"),
          "the theme control must live inside the footer")
check("ETSU_RERENDER_MERMAID" in BASE, "the switch never re-renders mermaid")
check("ETSU_RERENDER_MERMAID" in MERMAID, "_mermaid.html publishes no re-render hook")
check("mermaidSrc" in MERMAID,
      "mermaid's source is not retained, so a re-render has nothing to render")

if failures:
    for f in failures:
        print(f"FAIL: {f}")
    sys.exit(1)
print(f"OK: theme contract ({len(dark)} tokens mirrored across both palettes)")
