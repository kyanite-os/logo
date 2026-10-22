#!/usr/bin/env python3
"""kyanite-logotype.svg — the symbol followed by the word.

The word is set in Inter SemiBold and then **converted to outlines**:
the file depends on no installed font. Inter is under the SIL OFL,
which explicitly permits derivative works.

Inter was chosen for its neutrality: a geometric grotesque, technical,
with no character of its own. The symbol carries all the expression;
the word merely names it.
"""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import block as G

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "logo")
FONT = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"

WORD = "Kyanite"
CAP_HEIGHT = 34.0         # cap height: 45% of the symbol's height
TRACKING = -0.4           # overall tracking, slightly tight
KERNING = {"Ky": -2.6, "at": -0.5, "te": -0.3}   # pairs fixed by hand
GAP = 20.0                # white space between the symbol and the word

def glyphs():
    f = TTFont(FONT)
    cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    cap = f["OS/2"].sCapHeight
    k = CAP_HEIGHT / cap
    out, x = [], 0.0
    for i, ch in enumerate(WORD):
        name = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[name].draw(pen)
        d = pen.getCommands()
        if d:
            out.append((x, d))
        x += hmtx[name][0] * k + TRACKING
        if i + 1 < len(WORD):
            x += KERNING.get(WORD[i:i + 2], 0.0)
    return out, x - TRACKING, k

def write_svg(theme, symbol="kyanite-logo.svg"):
    gl, word_width, k = glyphs()
    # The symbol occupies 10..88 out of 10..90 in its own file: we crop it
    # flush so the logotype carries no stray white space.
    x0 = 78.0 + GAP
    baseline = 40.0 + CAP_HEIGHT / 2.0     # the word sits optically centred
    total = x0 + word_width

    logo = open(os.path.join(OUT, symbol)).read()
    body = logo[logo.index("<defs>"):logo.rindex("</svg>")].rstrip()

    L = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total:.1f} 80"',
         f'     width="{total:.1f}" height="80" role="img" aria-label="Kyanite">',
         '  <title>Kyanite</title>',
         '  <desc>The Kyanite symbol followed by the word, in Inter SemiBold outlines.</desc>',
         '', '  <g id="symbol" transform="translate(-10 -10)">',
         '  ' + body.replace("\n", "\n  "), '  </g>', '',
         '  <!-- the word, as outlines: no font required to display it -->',
         f'  <g id="word" fill="{theme["ink"]}">']
    for x, d in gl:
        L.append(f'    <path transform="translate({x0 + x:.2f} {baseline:.1f}) '
                 f'scale({k:.5f} -{k:.5f})" d="{d}"/>')
    L += ['  </g>', '</svg>']
    return "\n".join(L) + "\n", total

VARIANTS = [("kyanite-logotype", "kyanite-logo.svg", G.ON_DARK),
            ("kyanite-logotype-light", "kyanite-logo-light.svg", G.ON_LIGHT)]
if __name__ == "__main__":
    for slug, symbol, theme in VARIANTS:
        svg, w = write_svg(theme, symbol)
        p = os.path.join(OUT, slug + ".svg")
        open(p, "w").write(svg)
        print(f"wrote {slug:<24} {os.path.getsize(p) / 1024:.1f} KB  —  viewBox {w:.1f} x 80")
