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
    print("OK: design tokens")
