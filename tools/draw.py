#!/usr/bin/env python3
"""Kyanite — round 4. Variant K (deep mine), enriched.

Two additions:

1. SPANGLES in the vein: small angular shards and diamonds, sown along
   the crack, denser towards the lit lip.

2. TRANSLUCENT PLANES: kyanite is a transparent mineral. We overlay
   broad planes at low opacity, following three cleavage directions that
   match none of the visible faces. Where they cross, the value builds
   up: that is what makes the crystal read as having depth rather than
   as a painted surface.

   The opacity is a plain SVG attribute (fill-opacity), not a filter:
   the rendering stays the same everywhere, system icons included.
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import block as G

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logo")

# ---------------------------------------------------- transparency planes
# (direction, offset, width, which plane, opacity). CLEAR and SHADE name
# the role, not the colour: the theme supplies the value, so the same
# table serves both grounds.
CLEAR, SHADE = "clear", "shade"
PLANES = [
    ((2, 7),  -36,  7, CLEAR, 0.062), ((2, 7),  -26,  4, SHADE, 0.074),
    ((2, 7),  -17,  9, CLEAR, 0.05), ((2, 7),   -6,  5, SHADE, 0.081),
    ((2, 7),    4, 11, CLEAR, 0.043), ((2, 7),   16,  4, SHADE, 0.074),
    ((2, 7),   25,  8, CLEAR, 0.056), ((2, 7),   36,  5, SHADE, 0.074),
    ((9, -3), -33,  9, SHADE, 0.056), ((9, -3), -22,  4, CLEAR, 0.081),
    ((9, -3), -12, 11, CLEAR, 0.037), ((9, -3),   0,  5, SHADE, 0.068),
    ((9, -3),   11,  8, CLEAR, 0.05), ((9, -3),  22,  4, SHADE, 0.074),
    ((9, -3),   33, 10, CLEAR, 0.043),
    ((-3, 8), -28,  8, CLEAR, 0.043), ((-3, 8), -16,  5, SHADE, 0.062),
    ((-3, 8),  -4, 12, SHADE, 0.037), ((-3, 8),  10,  5, CLEAR, 0.074),
    ((-3, 8),  22,  9, SHADE, 0.05), ((-3, 8),  34,  6, CLEAR, 0.062),
]
# two planes laid over everything: the light passing through the mass
PLANES_OVER = [((9, -3), -20, 18, CLEAR, 0.043), ((2, 7), 16, 14, CLEAR, 0.031),
               ((-3, 8), 6, 9, CLEAR, 0.031)]
# a large wedge of light, entering from the top left
WEDGE = ([(-10, -10), (62, -10), (-10, 58)], CLEAR, 0.07)

def plane(d, o, w, rnd, long_=150.0):
    """An internal plane has no straight edge: we break it, otherwise the
    eye reads a band laid on top of the drawing."""
    u = G.unit(d); nn = (-u[1], u[0])
    c = (50 + nn[0] * o, 50 + nn[1] * o)
    def edge(k):
        p0 = (c[0] + nn[0] * k - u[0] * long_, c[1] + nn[1] * k - u[1] * long_)
        p1 = (c[0] + nn[0] * k + u[0] * long_, c[1] + nn[1] * k + u[1] * long_)
        return G.broken_line(p0, p1, 7, max(0.5, w * 0.16), rnd)
    return edge(w / 2) + edge(-w / 2)[::-1]

# -------------------------------------------------------------- spangles
def diamond(cx, cy, r, rot, ap=0.45):
    return [(cx + math.cos(rot + i * math.pi / 2) * (r if i % 2 == 0 else r * ap),
             cy + math.sin(rot + i * math.pi / 2) * (r if i % 2 == 0 else r * ap))
            for i in range(4)]

def spangles(seed, scale, traces, palette):
    """Sown along the crack, denser towards the lit lip."""
    rnd = random.Random(seed)
    out = []
    for P, W, g, d in traces:
        n = len(P)
        for i in range(n):
            if W[i] < 0.3:
                continue
            u = G.unit(G.sub(P[min(i + 1, n - 1)], P[max(i - 1, 0)]))
            nn = (-u[1], u[0])
            for _ in range(rnd.randint(0, 3)):
                off = rnd.uniform(-g[i] * 0.9, d[i] * 1.15)
                along = rnd.uniform(-0.8, 0.8)
                cx = P[i][0] + nn[0] * off + u[0] * along
                cy = P[i][1] + nn[1] * off + u[1] * along
                r = rnd.uniform(0.09, 0.3) * (0.5 + W[i]) * scale
                c = palette[min(4, int(rnd.random() * 5.4))]
                out.append((G.fleck(rnd, cx, cy, r * 1.35) if rnd.random() < 0.45
                            else diamond(cx, cy, r, rnd.random() * math.pi,
                                         rnd.uniform(0.28, 0.72)), c))
    # a few isolated shards caught in the rock, around the seam
    for cx, cy in ((33.0, 25.0), (15.5, 46.0), (34.0, 62.0), (50.0, 36.0), (70.0, 26.0)):
        r = rnd.uniform(0.3, 0.55) * scale
        out.append((diamond(cx, cy, r, rnd.random() * math.pi, 0.4), palette[rnd.randint(2, 3)]))
    return out

# ------------------------------------------------------------------ output
n_, pts, OUTER = G.n_, G.pts, G.OUTER

def build(title, plane_dose, spangle_scale, seed=81177, theme=None, filled=True):
    theme = theme or G.ON_DARK
    G.check_ground(theme)
    ramp, bev = theme["rock"], theme["bevel"]
    resin = theme["resin"] if filled else None
    def op(v): return f"{min(0.85, v * plane_dose):.3f}".rstrip("0").rstrip(".")
    L = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"',
         '     role="img" aria-label="Kyanite">',
         f'  <title>Kyanite — {title}</title>', '',
         '  <defs>',
         f'    <clipPath id="clip-block"><polygon points="{pts(OUTER)}"/></clipPath>',
         f'    <clipPath id="clip-stem"><polygon points="{pts(G.BAND_STEM)}"/></clipPath>',
         f'    <clipPath id="clip-arm"><polygon points="{pts(G.BAND_ARM)}"/></clipPath>',
         f'    <clipPath id="clip-leg"><polygon points="{pts(G.BAND_LEG)}"/></clipPath>',
         '  </defs>', '',
         '  <g clip-path="url(#clip-block)">',
         f'    <polygon points="{pts(OUTER)}" fill="{ramp[4]}"/>', '']
    groups = (
        ("clip-stem", "stem",
         G.blades_stem(ramp, seed + 1) + G.fines_stem(26, ramp, seed + 11)),
        ("clip-arm", "upper arm",
         G.blades_axis(G.ARM_A, G.ARM_D, G.ARM_S, G.ARM_V, ramp, seed + 2)
         + G.fines_axis(G.ARM_Y0 - 4, G.ARM_Y1, G.ARM_S, 24, ramp, seed + 12)),
        ("clip-leg", "lower arm",
         G.blades_axis(G.LEG_A, G.LEG_D, G.LEG_S, G.LEG_V, ramp, seed + 3)
         + G.fines_axis(G.LEG_Y0, G.LEG_Y1 + 4, G.LEG_S, 22, ramp, seed + 13)),
    )
    for cid, name, bl in groups:
        L.append(f'    <!-- {name}: kyanite blades, broad then fine -->')
        L.append(f'    <g clip-path="url(#{cid})">')
        for poly, c in bl:
            L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
        L.append('    </g>')
    L += ['', '    <!-- grain: patches, grains, quartz flecks, mica specks -->', '    <g>']
    for poly, c in G.granite(seed, ramp, theme["mica"], theme["quartz"]):
        L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
    L.append('    </g>')
    L += ['', '    <!-- fractures running across the cleavage -->']
    for ps, w, lit in G.fractures(seed + 5):
        for poly, c in G.fracture(ps, w, lit, theme["fract"]):
            L.append(f'    <polygon points="{pts(poly)}" fill="{c}"/>')
    L += ['', "    <!-- cleavage planes passing through: the depth of the crystal -->", '    <g>']
    rp = random.Random(seed + 31)
    tri, tc, to = WEDGE
    L.append(f'      <polygon points="{pts(tri)}" fill="{theme[tc]}" fill-opacity="{op(to)}"/>')
    for d, o, w, c, a in PLANES:
        L.append(f'      <polygon points="{pts(plane(d, o, w, rp))}" fill="{theme[c]}"'
                 f' fill-opacity="{op(a)}"/>')
    L.append('    </g>')
    if resin is None:
        pieces, traces = G.open_crack(seed + 23, theme["crack"])
        L += ['', "    <!-- the open crack: hollow in shadow, uneven floor, far wall",
              "         lit in stretches, intermittent thread on the near lip,",
              "         missing chips, secondary cracks -->", '    <g>']
        for poly, c in pieces:
            L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
    else:
        pieces, traces = G.resin(seed + 23, resin)
        L += ['', "    <!-- the filled seam: stone lip underneath, translucent",
              "         resin, continuous meniscus on the near lip,",
              "         bubbles caught in the mass -->", '    <g>']
        for poly, c, a in pieces:
            o = f"{a:.2f}".rstrip("0").rstrip(".")
            L.append(f'      <polygon points="{pts(poly)}" fill="{c}" fill-opacity="{o}"/>')
    L.append('    </g>')
    L += ['', '    <!-- spangles: the shards caught in the crack -->', '    <g>']
    for poly, c in spangles(seed + 7, spangle_scale, traces, theme["spangle"]):
        L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
    L.append('    </g>')
    L += ['', '    <!-- two planes laid over everything: the light passing through -->']
    for d, o, w, c, a in PLANES_OVER:
        L.append(f'    <polygon points="{pts(plane(d, o, w, rp))}" fill="{theme[c]}"'
                 f' fill-opacity="{op(a)}"/>')
    L += ['', "    <!-- bevel: a narrow keen edge, then the main facet.",
          '         One facet per edge, a single top-left light. -->']
    edge = G.inset(OUTER, 0.8)
    # the keen edge parts from its facet: darker in shadow, keener in daylight
    keen = [bev[0], bev[0], bev[1], bev[4], bev[4]]
    for poly, c in G.bevel_ring(OUTER, edge, keen):
        L.append(f'    <polygon points="{pts(poly)}" fill="{c}"/>')
    for poly, c in G.bevel_ring(edge, G.inset(edge, G.BEVEL_W - 0.8), bev):
        L.append(f'    <polygon points="{pts(poly)}" fill="{c}"/>')
    L += ['  </g>', '</svg>']
    return "\n".join(L) + "\n"

# Two knobs: the opacity of the planes passing through, and the size of
# the spangles. The same two settings serve both grounds.
PLANE_DOSE, SPANGLE_SCALE = 1.55, 1.30
VARIANTS = [
    ("kyanite-logo", "K", G.ON_DARK),
    ("kyanite-logo-light", "K, for light backgrounds", G.ON_LIGHT),
]
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for slug, title, theme in VARIANTS:
        p = os.path.join(OUT, slug + ".svg")
        open(p, "w").write(build(title, PLANE_DOSE, SPANGLE_SCALE, theme=theme))
        print(f"wrote {slug:<22} {os.path.getsize(p)//1024} KB"
              f"   keen edge {G.check_ground(theme):.2f}:1 on {theme['ground']}")
