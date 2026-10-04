"""Build the official GP METHOD logo files for the bozza (circle approved by the client, 2026-10-05).

Monogram and METHOD come from the brand kit vectors (assets/brand/svg, the same glyphs as the
"Minimal metallo lucido HD" reference): they are reused as-is, never redrawn.
The thin rule and the tagline "SHAPE • STRENGTH • PERFORMANCE" are added under METHOD with the
proportions of Giorgia's reference (rule = 18% of METHOD's width, tagline = 1.35x METHOD's width,
tagline caps = 42% of METHOD's caps), set in Jost Light and converted to outlines.

Usage: <venv-with-fonttools>/bin/python bozza/tools/build-logo.py <Jost[wght].ttf>
"""
import re
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "assets/brand/svg/GP-METHOD_con-cerchio_trasparente-scuro.svg"
OUT = ROOT / "bozza/assets/logo"

# Measured in the brand SVG (1000x1000 box): METHOD spans x 357.4-642.2, caps y 687.7-716.5.
METHOD_W, METHOD_CAP, METHOD_BASE = 284.8, 28.8, 716.5
RULE_W = METHOD_W * 0.18
RULE_Y = METHOD_BASE + METHOD_CAP * 0.95
TAG_CAP = METHOD_CAP * 0.42
TAG_W = METHOD_W * 1.35
TAG_BASE = RULE_Y + METHOD_CAP * 0.74 + TAG_CAP
TAGLINE = "SHAPE   •   STRENGTH   •   PERFORMANCE"

PALETTES = {
    "": {  # polished metal on light grounds
        "gp": [("0", "#9C7F67"), (".22", "#E2D3C1"), (".45", "#A88B72"), (".72", "#4A382A"), ("1", "#1E1712")],
        "method": [("0", "#3A2F27"), ("1", "#1C1611")],
        "line": "#4A3F36",
        "ring": [("0", "#EFE3D4"), (".35", "#C9B8A6"), (".7", "#8A6E58"), ("1", "#5A4535")],
    },
    "-light": {  # champagne metal for dark grounds (preloader, dark panels)
        "gp": [("0", "#B9A189"), (".25", "#FBF3E8"), (".5", "#D9C6B0"), (".8", "#A88B72"), ("1", "#8C7360")],
        "method": [("0", "#F1E7DC"), ("1", "#D5C4B2")],
        "line": "#E2D6C9",
        "ring": [("0", "#FBF3E8"), (".4", "#D9C6B0"), ("1", "#8C7360")],
    },
}


def brand_paths():
    s = re.sub(r"<metadata>.*?</metadata>", "", SRC.read_text(), flags=re.S)
    paths = re.findall(r"<path [^>]+/>", s)
    strip = lambda p: re.sub(r'\sfill="[^"]*"', "", p)
    return strip(paths[0]), strip(paths[1])  # monogram, METHOD


def tagline_path(font_file):
    font = instantiateVariableFont(TTFont(font_file), {"wght": 300})
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    cap = font["OS/2"].sCapHeight or 700
    scale = TAG_CAP / cap
    names = [cmap[ord(c)] for c in TAGLINE]
    natural = sum(gs[n].width for n in names) * scale
    track = (TAG_W - natural) / (len(names) - 1)
    pen = SVGPathPen(gs)
    dots = []
    x = (1000 - TAG_W) / 2
    for i, (ch, n) in enumerate(zip(TAGLINE, names)):
        adv = gs[n].width * scale
        if ch == "•":
            # the reference's separators are solid dots about a third of the cap height
            dots.append((x + adv / 2, TAG_BASE - TAG_CAP / 2))
        else:
            # font units are y-up: flip, scale, move to baseline
            gs[n].draw(TransformPen(pen, (scale, 0, 0, -scale, x, TAG_BASE)))
        x += adv + (track if i < len(names) - 1 else 0)
    r = TAG_CAP * 0.17
    circles = "".join(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}"/>' for cx, cy in dots)
    return pen.getCommands(), circles


def gradient(gid, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{gid}" x1="0" y1="0.1" x2="1" y2="0.9">{s}</linearGradient>'


def main():
    mono, method = brand_paths()
    tag, dots = tagline_path(sys.argv[1])
    OUT.mkdir(parents=True, exist_ok=True)
    for suffix, pal in PALETTES.items():
        g = f"gp{suffix or '-dark'}"
        m = f"me{suffix or '-dark'}"
        r = f"ring{suffix or '-dark'}"
        defs = f"<defs>{gradient(g, pal['gp'])}{gradient(m, pal['method'])}{gradient(r, pal['ring'])}</defs>"
        ring = f'<circle cx="500" cy="500" r="400" fill="none" stroke="url(#{r})" stroke-width="5.5"/>'
        rule = (f'<line x1="{500 - RULE_W / 2:.1f}" y1="{RULE_Y:.1f}" x2="{500 + RULE_W / 2:.1f}" y2="{RULE_Y:.1f}" '
                f'stroke="{pal["line"]}" stroke-width="1.3" stroke-linecap="round"/>')
        body = (f'{ring}<g fill="url(#{g})">{mono}</g><g fill="url(#{m})">{method}</g>{rule}'
                f'<g fill="{pal["line"]}"><path d="{tag}"/>{dots}</g>')
        logo = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="96 96 808 808" role="img" '
                f'aria-label="GP METHOD: Shape, Strength, Performance">{defs}{body}</svg>\n')
        (OUT / f"gp-method-logo{suffix}.svg").write_text(logo)
        mono_svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="312 260 378 386" role="img" '
                    f'aria-label="GP METHOD">{defs.replace(gradient(m, pal["method"]), "").replace(gradient(r, pal["ring"]), "")}'
                    f'<g fill="url(#{g})">{mono}</g></svg>\n')
        (OUT / f"gp-method-monogram{suffix}.svg").write_text(mono_svg)
    print("written:", sorted(p.name for p in OUT.glob("*.svg")))


if __name__ == "__main__":
    main()
