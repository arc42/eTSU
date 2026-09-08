"""Design-system contract for style.css and the templates. No pytest."""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CSS = (HERE / "static" / "style.css").read_text(encoding="utf-8")
FONTS = HERE / "static" / "vendor" / "fonts"
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿\U0001F000-\U0001F2FF]")


def test_fonts_are_vendored():
    for name in ("BricolageGrotesque-var.woff2", "JetBrainsMono-400.woff2", "JetBrainsMono-600.woff2"):
        f = FONTS / name
        assert f.is_file() and f.stat().st_size > 10_000, name
    assert CSS.count("@font-face") == 3
    assert "fonts.googleapis.com" not in CSS


def test_no_gradients_or_glow():
    assert "linear-gradient" not in CSS and "radial-gradient" not in CSS
    assert "--glow" not in CSS


def test_no_emoji_in_ui():
    for p in list((HERE / "templates").glob("*.html")) + [HERE / "app.py"]:
        txt = p.read_text(encoding="utf-8")
        m = EMOJI.search(txt)
        assert not m, f"emoji {m.group()!r} in {p.name}"


def _block(selector):
    i = CSS.index(selector + " {")
    return CSS[i:CSS.index("}", i)]


# Classes a template sets that style.css deliberately does not define. Each is
# a behavioural hook, not a visual one — if you add to this list, say why.
HOOKLESS_OK = {
    # queried by base.html's JS to swap the unit and the toggle's own wording
    "presence-unit", "theme-toggle-label",
    # graph.html's layout switcher: `#graph-layout .lay-btn` in JS; the visual
    # styling comes from .layer-btn, which sits on the same buttons
    "lay-btn",
    # not a class attribute at all — it appears inside a JS comment in
    # _mermaid.html describing the markup markdown emits for a ```mermaid fence
    "language-mermaid",
}

_JINJA_STMT = re.compile(r"\{%.*?%\}", re.S)     # control flow: contributes no text
_JINJA_EXPR = re.compile(r"\{\{.*?\}\}", re.S)   # a value: makes its token unknowable
_CLASS_ATTR = re.compile(r'class="([^"]*)"')
_SELECTOR_CLASS = re.compile(r"\.(-?[A-Za-z_][\w-]*)")


def _css_class_selectors():
    """Every class name that appears in a selector in style.css (comments and
    at-rule preludes stripped, so a URL or a prose `.` never counts)."""
    body = re.sub(r"/\*.*?\*/", " ", CSS, flags=re.S)
    names = set()
    for sel in re.findall(r"(?:^|[}{;])([^{}]*)\{", body):
        if sel.strip().startswith("@"):
            sel = re.sub(r"@[\w-]+[^{]*", " ", sel)
        names |= set(_SELECTOR_CLASS.findall(sel))
    return names


def test_every_template_class_has_a_rule_or_a_reason():
    """A class in the markup with no rule behind it is either a leftover from a
    deleted design or a typo for a class that does exist. Jinja-composed names
    (`tile-{{ t.key }}`) are unknowable statically and are skipped."""
    css_classes = _css_class_selectors()
    orphans = {}
    for tpl in sorted((HERE / "templates").glob("*.html")):
        txt = tpl.read_text(encoding="utf-8")
        for attr in _CLASS_ATTR.findall(txt):
            attr = _JINJA_EXPR.sub("\x00", _JINJA_STMT.sub(" ", attr))
            for name in attr.split():
                if "\x00" in name or name in css_classes or name in HOOKLESS_OK:
                    continue
                orphans.setdefault(name, set()).add(tpl.name)
    assert not orphans, "class with no CSS rule and no documented hook: " + ", ".join(
        f"{k} ({', '.join(sorted(v))})" for k, v in sorted(orphans.items()))


def test_every_token_exists_in_both_themes():
    dark = set(re.findall(r"--[\w-]+(?=\s*:)", _block(":root")))
    light = set(re.findall(r"--[\w-]+(?=\s*:)", _block(':root[data-theme="light"]')))
    structural = {t for t in dark if not t.startswith(("--font", "--radius", "--space", "--step"))}
    assert structural <= light, f"missing in light theme: {sorted(structural - light)}"
    assert light <= dark, f"only in light theme: {sorted(light - dark)}"


if __name__ == "__main__":
    test_fonts_are_vendored()
    test_no_gradients_or_glow()
    test_no_emoji_in_ui()
    test_every_token_exists_in_both_themes()
    test_every_template_class_has_a_rule_or_a_reason()
    print("OK: design tokens")
