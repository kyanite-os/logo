#!/usr/bin/env python3
"""kyanite-icon.svg — the version for small sizes.

Same silhouette as the full logo, and nothing else: no grain, no
lamellae, no fractures, no translucent planes, no spangles. Below
64 px all of that is just noise.

What remains is the silhouette, the contrast between the three strokes,
and the filled seam — that last one disappears at 16 px and only comes
back from 22 up. The bevel is widened from 3 to 5 so that it still
carries half a pixel at 16 px.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import block as G

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logo")

# Simplified outline: we drop the jogs along the long edges, invisible
# below 64 px and costly in vertices. The chamfers, the oblique top and
# the stepped foot stay: that is the identity of the mark.
OUTLINE = [
    ((G.SL, 17.0),           (7.0, 8.0)),   # top-left corner
    ((G.SR, G.TOP),          (4.5, 4.0)),   # top of the stem, clean cut
    ((G.SR, G.ARM_Y0),       (4.0, 5.0)),   # bottom of the upper notch
    ((G.X_ARM_TOP, G.TOP),   (6.0, 5.0)),
    ((G.ARM_X, G.TOP),       (5.0, 3.5)),   # top-right corner
    ((G.ARM_X, G.Y_ARM_TIP), (3.5, 6.0)),   # upper blade edge
    ((G.SR, G.FORK),         (7.0, 6.0)),   # the fork
    ((G.LEG_X, G.Y_LEG_TIP), (5.0, 3.0)),   # lower blade edge
    ((G.LEG_X, G.BOT),       (3.0, 5.0)),   # bottom-right corner
    ((G.X_LEG_BOT, G.BOT),   (5.0, 4.0)),
    ((G.SR, G.LEG_Y1),       (4.0, 2.0)),   # bottom of the lower notch
    ((G.SR, 85.0),           (2.0, 2.0)),   # the stepped foot
    ((26.0, 85.0),           (2.0, 2.0)),
    ((26.0, G.BOT),          (2.0, 2.5)),
    ((G.SL, G.BOT),          (0.0, 0.0)),   # bottom-left corner: right angle
]
BEVEL_W = 5.0
# The tints come from the theme (see block.py). The seam is FILLED here
# too: a translucent resin, and above all a continuous meniscus along the
# near lip. It is the continuity of that thread, not its colour, that
# makes it read "sealed" rather than "broken". The values are flattened
# for this size — at 16 px, stacking opacities only gives mush — so the
# body value is the one the full logo's resin produces once composited
# over the stone.

# The seam, reduced to its main path: the stem, then the upper arm.
VEIN_STEM = [(17.5, 84.0), (23.0, 69.0), (19.5, 56.0), (25.0, 43.5), (21.5, 29.0), (23.5, 14.0)]
VEIN_ARM = [(25.0, 43.5), (40.0, 38.5), (56.0, 29.5), (70.0, 21.5), (81.0, 17.0)]
W_STEM = [0.0, 1.35, 1.0, 1.4, 0.95, 0.0]
W_ARM = [1.4, 1.25, 1.1, 0.85, 0.0]

SPLIT_STEM = 21.5
SPLIT_ARM = 32.0
SPLIT_LEG = 58.0
D = 13.0   # overhang: everything is clipped back by the outline mask

def band_arm(a, b):
    return [(G.SR, a), (G.SR + 7 * D, a - 4 * D), (G.SR + 7 * D, b - 4 * D), (G.SR, b)]
def band_leg(a, b):
    return [(G.SR, a), (G.SR + 8 * D, a + 5 * D), (G.SR + 8 * D, b + 5 * D), (G.SR, b)]
def band_stem(a, b):
    return [(a, -5), (b, -5), (b, 105), (a, 105)]

def write_svg(theme):
    G.check_ground(theme)
    STONE, RAMP, SEAM = theme["icon_stone"], theme["bevel"], theme["icon_seam"]
    n, pts = G.n_, G.pts
    outer = G.chamfer(OUTLINE)
    edge = G.inset(outer, 1.2)
    assert not G.reversed_edges(outer, edge), "bevel facet flipped over"
    inner = G.inset(edge, BEVEL_W - 1.2)
    assert not G.reversed_edges(edge, inner), "bevel facet flipped over"
    keen = [RAMP[0], RAMP[0], RAMP[1], RAMP[4], RAMP[4]]

    L = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"',
         '     role="img" aria-label="Kyanite">',
         '  <title>Kyanite</title>',
         f'  <desc>A K cut from a block of kyanite. Small-size version,'
         f' for {theme["name"]} backgrounds.</desc>',
         '',
         '  <defs>',
         f'    <clipPath id="clip-block"><polygon points="{pts(outer)}"/></clipPath>',
         f'    <clipPath id="clip-stem"><polygon points="{pts(band_stem(-5, G.SR))}"/></clipPath>',
         f'    <clipPath id="clip-arm"><polygon points="{pts(band_arm(G.ARM_Y0, G.FORK))}"/></clipPath>',
         f'    <clipPath id="clip-leg"><polygon points="{pts(band_leg(G.FORK, G.LEG_Y1))}"/></clipPath>',
         '  </defs>',
         '',
         '  <g clip-path="url(#clip-block)">',
         f'    <polygon points="{pts(outer)}" fill="{STONE["stem_shade"]}"/>',
         '',
         "    <!-- a single light, coming from the top left: the face turned",
         '         towards it is lit, the other is in shadow -->']
    for cid, name, parts in (
        ("clip-stem", "stem", [(band_stem(-5, SPLIT_STEM), "stem_lit"),
                               (band_stem(SPLIT_STEM, G.SR), "stem_shade")]),
        ("clip-arm", "arm", [(band_arm(G.ARM_Y0 - D, SPLIT_ARM), "arm_lit"),
                             (band_arm(SPLIT_ARM, G.FORK), "arm_shade")]),
        ("clip-leg", "leg", [(band_leg(G.FORK, SPLIT_LEG), "leg_lit"),
                             (band_leg(SPLIT_LEG, G.LEG_Y1 + D), "leg_shade")])):
        L.append(f'    <g id="{name}" clip-path="url(#{cid})">')
        for poly, c in parts:
            L.append(f'      <polygon points="{pts(poly)}" fill="{STONE[c]}"/>')
        L.append('    </g>')

    L += ['', '    <!-- the filled seam: stone lip, resin, meniscus -->',
          '    <g id="seam">']
    for vein, w in ((VEIN_STEM, W_STEM), (VEIN_ARM, W_ARM)):
        L.append(f'      <polygon points="{pts(G.ribbon(vein, [x * 1.25 for x in w]))}"'
                 f' fill="{SEAM["stone_lip"]}"/>')
        L.append(f'      <polygon points="{pts(G.ribbon(vein, w))}" fill="{SEAM["body"]}"/>')
        L.append(f'      <polygon points="{pts(G.ribbon(vein, [x * 0.26 for x in w], -1.1))}"'
                 f' fill="{SEAM["meniscus"]}"/>')
    L.append('    </g>')

    L += ['', '    <!-- bevel: a keen edge, then the main facet -->', '    <g id="bevel">']
    for poly, c in G.bevel_ring(outer, edge, keen):
        L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
    for poly, c in G.bevel_ring(edge, inner, RAMP):
        L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
    L += ['    </g>', '  </g>', '</svg>']
    return "\n".join(L) + "\n"

VARIANTS = [("kyanite-icon", G.ON_DARK), ("kyanite-icon-light", G.ON_LIGHT)]
if __name__ == "__main__":
    for slug, theme in VARIANTS:
        p = os.path.join(OUT, slug + ".svg")
        open(p, "w").write(write_svg(theme))
        print(f"wrote {slug:<22} {os.path.getsize(p) / 1024:.1f} KB"
              f"   keen edge {G.check_ground(theme):.2f}:1 on {theme['ground']}")
