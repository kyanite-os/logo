#!/usr/bin/env python3
"""Kyanite — round 3. A K cut from a block, for dark backgrounds.

Nothing is symmetrical: the two arms share neither slope, nor length,
nor thickness; the long edges carry jogs; the corners are chamfered
unevenly.

The material reads as granite: a broad structure (the kyanite blades,
which carry the light), then patches the size of a crystal, then a fine
grain mixing pale flecks (quartz) and dark specks (mica). Three scales,
no symmetry anywhere.

A single light, coming from the top left. No perspective.
Polygons only: no filter, no bitmap, no gradient.
"""
import math, random

LIGHT = (-math.sqrt(0.5), -math.sqrt(0.5))

# ------------------------------------------------------------------ palette
# Cut for a dark background: the mass stays well above the background,
# the top-left bevel carries the light, the hollows sink.
ROCK_DEEP = ["#15306A", "#1B3B7C", "#21468E", "#2851A0", "#2E5CB1",
             "#3668C1", "#3F75CE", "#4A83DA", "#5793E4"]
MICA   = ["#1C3C76", "#22477F"]   # dark specks (biotite)
QUARTZ = ["#86B6EE", "#A8CCF4"]   # pale flecks (quartz)
BEVEL_HARD = ["#112A58", "#1C4184", "#3A74C8", "#86B7F2", "#DBEBFF"]
SEAM = {"hollow": "#15376E", "floor": "#0E2650", "far_wall": "#3570C4", "lip": "#8FBDF4"}
FRACT = {"dark": "#1E4588", "light": "#6CA2E8"}
SPANGLE = ["#C6DEFA", "#A8CCF4", "#88B8F0", "#6AA0E8", "#4D86DA"]
PLANE_CLEAR, PLANE_SHADE = "#BBD8F8", "#0C2149"   # translucent planes
INK = "#DCE6F2"                                   # the word, in the logotype
GROUND = "#0F1522"                                # reference background
# the icon flattens its tints: at 16 px, stacked opacities only give mush
ICON_STONE = {"stem_lit": "#3A74CA", "stem_shade": "#234C92",
              "arm_lit":  "#74ABEE", "arm_shade":  "#4280D6",
              "leg_lit":  "#4D8ADA", "leg_shade":  "#2E60B4"}
ICON_SEAM = {"stone_lip": "#163A74", "body": "#7CA6E0", "meniscus": "#EAF4FF"}

# The earlier round's softer palette. Kept for the record; the shipped
# drawing uses ROCK_DEEP and BEVEL_HARD.
ROCK = ["#1B3C78", "#22488B", "#28539D", "#2F5FAF", "#366BC0",
        "#3F78CE", "#4A86DA", "#5795E4", "#67A4EC"]
BEVEL = ["#17376F", "#21488F", "#3A74C8", "#72ACEE", "#BEDCFA"]

# ------------------------------------------------ palette, light ground
# Cut for a light background. Same mineral, same single light from the
# top left; what changes is where the whole value scale sits.
#
# On a dark ground the block is a lit mass in a near-black room, and the
# keenest facet can blow out to near-white (#DBEBFF). On a light ground
# that cannot hold: white is now the brightest thing in the frame, so a
# near-white edge simply vanishes into the page — 1.21:1 against #FFFFFF,
# which is what opened the contour and is the whole reason this palette
# exists. The scale is therefore pushed BELOW the page: deep navy in
# shadow, mid blue in the light.
#
# What is preserved is not the values but the INTERVALS between them.
# The ratios that carry the chiselled read — the three strokes apart from
# each other, each stroke's lit face against its own shadow — land within
# a few hundredths of the dark palette's. The light still comes from the
# top left; it is the room that changed, not the lamp.
#
# The consequence is an asymmetry worth knowing. On a dark ground the
# contour is held by the keen lit edge (15:1) and the deepest facet is
# allowed to sink into the background. On a light ground it is the mass
# itself that holds the contour (18.6:1 at the deepest), and the lit edge
# is merely the palest part of the stone (3.47:1) — never paler than the
# page. That is why neither variant survives on the other's ground.
ROCK_LIGHT = ["#0B1C40", "#0F244E", "#132C5C", "#17356A", "#1C3E79",
              "#214887", "#285496", "#2F60A5", "#3A6DBE"]
BEVEL_LIGHT = ["#07122A", "#0F2350", "#23508F", "#3A74C8", "#4E8BDC"]
MICA_LIGHT   = ["#0A1835", "#0E1E42"]
QUARTZ_LIGHT = ["#5E90D8", "#7BA8E4"]
FRACT_LIGHT = {"dark": "#0D2048", "light": "#3E72C4"}
SPANGLE_LIGHT = ["#A8C8F0", "#8BB0E6", "#6E98DC", "#5480CE", "#3F6CC0"]
PLANE_CLEAR_LIGHT, PLANE_SHADE_LIGHT = "#A9C8EC", "#06102A"
INK_LIGHT = "#16253D"
GROUND_LIGHT = "#FFFFFF"
ICON_STONE_LIGHT = {"stem_lit": "#255494", "stem_shade": "#122C57",
                    "arm_lit":  "#4E8BDC", "arm_shade":  "#2A5FA8",
                    "leg_lit":  "#336FC0", "leg_shade":  "#1C4480"}
ICON_SEAM_LIGHT = {"stone_lip": "#0E2448", "body": "#5E8ECE", "meniscus": "#CFE2F8"}

# ---------------------------------------------------------------- geometry
SL, SR = 10.0, 40.0          # stem: 30 thick, it is the pillar
TOP, BOT = 10.0, 90.0
FORK = 48.0
ARM_Y0, ARM_Y1 = 22.0, FORK  # upper arm: slope 4/7
LEG_Y0, LEG_Y1 = FORK, 73.0  # lower arm: slope 5/8, shorter joint
ARM_S, LEG_S = -4.0 / 7.0, 5.0 / 8.0      # different slopes: no mirroring
ARM_X, LEG_X = 86.0, 88.0                 # short arms: it fits the square
X_ARM_TOP = SR + (ARM_Y0 - TOP) * 7.0 / 4.0
Y_ARM_TIP = ARM_Y1 + (ARM_X - SR) * ARM_S
Y_LEG_TIP = LEG_Y0 + (LEG_X - SR) * LEG_S
X_LEG_BOT = SR + (BOT - LEG_Y1) * 8.0 / 5.0

OUTLINE = [
    # The top and the foot of the stem are not of the same nature.
    # At the top: a single clean oblique cut, made in one stroke.
    # At the bottom: on the left a clean right angle, the flank plumb
    # all the way to the ground; on the right a step, the corner left
    # hanging in the air.
    ((SL, 17.0),         (7.0, 8.0)),   # top-left corner
    ((SR, TOP),          (4.5, 4.0)),   # top of the stem, clean cut
    ((SR, ARM_Y0),       (4.0, 5.0)),   # bottom of the upper notch
    ((X_ARM_TOP, TOP),   (6.0, 5.0)),   # start of the upper arm
    ((ARM_X, TOP),       (5.0, 3.5)),   # top-right corner
    ((ARM_X, Y_ARM_TIP), (3.5, 6.0)),   # foot of the upper blade edge
    ((65.0, 34.5),       (0.0, 0.0)),   # jog
    ((SR, FORK),         (7.0, 6.0)),   # the fork
    ((68.0, 66.6),       (0.0, 0.0)),   # jog
    ((LEG_X, Y_LEG_TIP), (5.0, 3.0)),   # top of the lower blade edge
    ((LEG_X, BOT),       (3.0, 5.0)),   # bottom-right corner
    ((X_LEG_BOT, BOT),   (5.0, 4.0)),   # start of the lower arm
    ((SR, LEG_Y1),       (4.0, 2.0)),   # bottom of the lower notch, raised
    ((SR, 85.0),         (2.0, 2.0)),   # the RIGHT corner of the foot is broken:
    ((26.0, 85.0),       (2.0, 2.0)),   # a step, it stays up in the air
    ((26.0, BOT),        (2.0, 2.5)),
    ((SL, BOT),          (0.0, 0.0)),   # bottom-left corner: clean right angle,
    ((SL, 72.0),         (0.0, 0.0)),   # the flank stays plumb up to here
    ((9.1, 58.0),        (0.0, 0.0)),   # jogs along the left flank
    ((10.9, 34.0),       (0.0, 0.0)),
]
BEVEL_W = 3.0

def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def unit(v):
    L = math.hypot(*v); return (v[0] / L, v[1] / L)

def chamfer(spec):
    out, n = [], len(spec)
    for i, (P, (ci, co)) in enumerate(spec):
        if ci <= 0 and co <= 0:
            out.append(P); continue
        A, B = spec[i - 1][0], spec[(i + 1) % n][0]
        ua, ub = unit(sub(A, P)), unit(sub(B, P))
        out.append((P[0] + ua[0] * ci, P[1] + ua[1] * ci))
        out.append((P[0] + ub[0] * co, P[1] + ub[1] * co))
    return out

def edge_frames(poly):
    n = len(poly)
    A = 0.5 * sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    out = []
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        u = unit(sub(q, p))
        out.append((p, u, (-u[1], u[0]) if A > 0 else (u[1], -u[0])))
    return out

def reversed_edges(outer, inner):
    """A bevel facet that flips over makes a tooth. We check that every
    inner edge still runs the same way as its outer one."""
    n, bad = len(outer), []
    for i in range(n):
        j = (i + 1) % n
        uo = (outer[j][0] - outer[i][0], outer[j][1] - outer[i][1])
        ui = (inner[j][0] - inner[i][0], inner[j][1] - inner[i][1])
        if uo[0] * ui[0] + uo[1] * ui[1] < -1e-9:
            bad.append((i, outer[i], outer[j]))
    return bad

def inset(poly, d):
    fr = edge_frames(poly)
    off = [((p[0] + ni[0] * d, p[1] + ni[1] * d), u) for p, u, ni in fr]
    out = []
    for i in range(len(poly)):
        (P1, u1), (P2, u2) = off[i - 1], off[i]
        cr = u1[0] * u2[1] - u1[1] * u2[0]
        if abs(cr) < 1e-9:
            out.append(P2); continue
        w = sub(P2, P1)
        t = (w[0] * u2[1] - w[1] * u2[0]) / cr
        out.append((P1[0] + u1[0] * t, P1[1] + u1[1] * t))
    # On an edge shorter than the bevel, the two neighbouring facets
    # would cross and make a tooth. We fold them to a point instead.
    for _ in range(6):
        bad = reversed_edges(poly, out)
        if not bad:
            break
        for i, _a, _b in bad:
            j = (i + 1) % len(out)
            m = ((out[i][0] + out[j][0]) / 2.0, (out[i][1] + out[j][1]) / 2.0)
            out[i] = m; out[j] = m
    return out

def bevel_ring(outer, inner, ramp):
    fr, n, q = edge_frames(outer), len(outer), []
    for i in range(n):
        no = (-fr[i][2][0], -fr[i][2][1])
        b = no[0] * LIGHT[0] + no[1] * LIGHT[1]
        k = min(len(ramp) - 1, max(0, round((b + 1) / 2 * (len(ramp) - 1))))
        q.append(([outer[i], outer[(i + 1) % n], inner[(i + 1) % n], inner[i]], ramp[k]))
    return q

# ------------------------------------------------ kyanite blades (structure)
XF = 118.0
ARM_A = [4.0, 11.0, 15.0, 20.0, 25.0, 29.5, 34.5, 40.0, 50.0]
ARM_D = [2.5, -1.8, 3.2, -2.6, 1.4, 3.6, -2.0, 2.2, -1.0]
ARM_V = [8, 7, 8, 6, 5, 6, 4, 5]
LEG_A = [45.0, 50.0, 54.0, 57.5, 61.5, 65.5, 69.0, 75.0]
LEG_D = [-1.5, 2.4, -2.9, 1.8, -2.2, 3.1, -1.4, 2.0]
LEG_V = [6, 7, 5, 6, 3, 4, 2]
STEM_X = [3.0, 11.0, 15.0, 19.5, 24.0, 28.0, 32.0, 36.0, 43.0]
STEM_D = [1.2, -0.9, 1.6, -1.3, 0.7, 1.9, -1.1, 0.9, -0.6]
STEM_V = [6, 5, 6, 4, 3, 4, 2, 1]

# ----------------------------------------- where we are inside the structure
def base_index(x, y):
    """The background value at a given point: used to lay the grain down
    without wiping out the light."""
    if x <= SR:
        bx = [STEM_X[i] + STEM_D[i] * (y + 8.0) / 116.0 for i in range(len(STEM_X))]
        for i in range(len(STEM_V)):
            if bx[i] <= x < bx[i + 1]:
                return STEM_V[i]
        return STEM_V[-1] if x >= bx[-1] else STEM_V[0]
    if y <= ARM_Y1 + (x - SR) * ARM_S:
        A, D, V, S = ARM_A, ARM_D, ARM_V, ARM_S
    else:
        A, D, V, S = LEG_A, LEG_D, LEG_V, LEG_S
    run = (XF - SR) * S
    t = (x - SR) / (XF - SR)
    by = [A[i] + (run + D[i]) * t for i in range(len(A))]
    for i in range(len(V)):
        if by[i] <= y < by[i + 1]:
            return V[i]
    return V[-1] if y >= by[-1] else V[0]

def broken_line(p0, p1, n, amp, rnd):
    """A cleavage plane is never a straight line: we break it into n
    segments, with a small perpendicular drift at each node."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    out = [p0]
    for i in range(1, n):
        t = i / n
        o = rnd.uniform(-amp, amp)
        out.append((p0[0] + dx * t + nx * o, p0[1] + dy * t + ny * o))
    out.append(p1)
    return out

def blades_axis(anchors, deltas, slope, vals, ramp, seed):
    """The blades of one arm. Two neighbouring planes share exactly the
    same break: the blades tile the band with no gap."""
    rnd = random.Random(seed)
    run = (XF - SR) * slope
    edges = [broken_line((SR, y), (XF, y + run + d), 6, 1.15, rnd)
             for y, d in zip(anchors, deltas)]
    return [(edges[i] + edges[i + 1][::-1], ramp[vals[i]]) for i in range(len(vals))]

def blades_stem(ramp, seed):
    rnd = random.Random(seed)
    edges = [broken_line((x, -8.0), (x + d, 108.0), 7, 0.95, rnd)
             for x, d in zip(STEM_X, STEM_D)]
    return [(edges[i] + edges[i + 1][::-1], ramp[STEM_V[i]]) for i in range(len(STEM_V))]

def fines_axis(y0, y1, slope, n, ramp, seed):
    """Fine lamellae caught between the big blades: this is what stops
    the eye from falling back onto the underlying shape."""
    rnd = random.Random(seed)
    run = (XF - SR) * slope
    out = []
    for _ in range(n):
        y = rnd.uniform(y0, y1)
        w = rnd.uniform(0.25, 0.8)
        d0, d1 = rnd.uniform(-2.5, 2.5), rnd.uniform(-2.5, 2.5)
        a = broken_line((SR, y), (XF, y + run + d0), 5, 0.9, rnd)
        b = broken_line((SR, y + w), (XF, y + w + run + d1), 5, 0.9, rnd)
        v = base_index(SR + 12.0, y + (12.0 * slope) + w / 2)
        out.append((a + b[::-1], ramp[max(0, min(len(ramp) - 1, v + rnd.choice((-1, -1, 1, 1, 2))))]))
    return out

def fines_stem(n, ramp, seed):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(SL - 1, SR + 1)
        w = rnd.uniform(0.25, 0.7)
        a = broken_line((x, -8.0), (x + rnd.uniform(-2.0, 2.0), 108.0), 6, 0.8, rnd)
        b = broken_line((x + w, -8.0), (x + w + rnd.uniform(-2.0, 2.0), 108.0), 6, 0.8, rnd)
        v = base_index(x + w / 2, 50.0)
        out.append((a + b[::-1], ramp[max(0, min(len(ramp) - 1, v + rnd.choice((-1, -1, 1, 1))))]))
    return out

KK = 14.0
BAND_STEM = [(-8, -8), (SR, -8), (SR, 108), (-8, 108)]
BAND_ARM = [(SR, ARM_Y0), (SR + 7 * KK, ARM_Y0 - 4 * KK), (SR + 7 * KK, ARM_Y1 - 4 * KK), (SR, ARM_Y1)]
BAND_LEG = [(SR, LEG_Y0), (SR + 8 * KK, LEG_Y0 + 5 * KK), (SR + 8 * KK, LEG_Y1 + 5 * KK), (SR, LEG_Y1)]

# ---------------------------------------------------------- granite grain
def fleck(rnd, cx, cy, r):
    k = rnd.randint(4, 6)
    a0 = rnd.random() * math.tau
    el = rnd.uniform(0.62, 1.35)
    out = []
    for j in range(k):
        a = a0 + math.tau * (j + rnd.uniform(-0.2, 0.2)) / k
        rr = r * rnd.uniform(0.55, 1.0)
        out.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * el))
    return out

def granite(seed, ramp, mica=None, quartz=None):
    """Three scales: patches, grains, flecks. Placed on a jittered grid so
    they cover without clumping."""
    mica, quartz = mica or MICA, quartz or QUARTZ
    rnd = random.Random(seed)
    res = []
    # the density varies from place to place: rock is not regular
    nests = [(rnd.uniform(12, 84), rnd.uniform(12, 84), rnd.uniform(14, 26)) for _ in range(6)]
    def density(x, y):
        k = 0.0
        for nx, ny, nr in nests:
            dd = math.hypot(x - nx, y - ny) / nr
            if dd < 1.0:
                k += (1.0 - dd) ** 2
        return min(1.0, k)
    for cols, rmin, rmax, kind, rate in ((9, 2.4, 4.3, "patch", 0.78),
                                         (19, 0.75, 1.7, "grain", 0.70),
                                         (28, 0.26, 0.62, "fleck", 0.52)):
        step = 86.0 / cols
        for gy in range(cols):
            for gx in range(cols):
                cx = 7.0 + (gx + rnd.uniform(0.05, 0.95)) * step
                cy = 7.0 + (gy + rnd.uniform(0.05, 0.95)) * step
                if rnd.random() > rate * (0.45 + 0.85 * density(cx, cy)):
                    continue
                r = rnd.uniform(rmin, rmax)
                b = base_index(cx, cy)
                if kind == "patch":
                    c = ramp[max(0, min(len(ramp) - 1, b + rnd.choice((-1, -1, 1, 1))))]
                elif kind == "grain":
                    c = ramp[max(0, min(len(ramp) - 1, b + rnd.choice((-2, -1, -1, 1, 1, 2))))]
                else:
                    u = rnd.random()
                    if u < 0.42:
                        c = mica[rnd.randint(0, 1)]
                    elif u < 0.72:
                        c = quartz[rnd.randint(0, 1)]
                    else:
                        c = ramp[max(0, min(len(ramp) - 1, b + rnd.choice((-2, 2))))]
                res.append((fleck(rnd, cx, cy, r), c))
    return res

def ribbon(ps, w, shift=0.0):
    n = len(ps)
    nor = [(lambda u: (-u[1], u[0]))(unit(sub(ps[min(i + 1, n - 1)], ps[max(i - 1, 0)]))) for i in range(n)]
    a = [(ps[i][0] + nor[i][0] * (w[i] + shift), ps[i][1] + nor[i][1] * (w[i] + shift)) for i in range(n)]
    b = [(ps[i][0] - nor[i][0] * (w[i] - shift), ps[i][1] - nor[i][1] * (w[i] - shift)) for i in range(n)]
    return a + b[::-1]

# ---------------------------------------------------------------- fractures
def fractures(seed):
    """Breaks running across the cleavage. Lengths, widths and contrasts
    all different: a regular break reads as a drawn line. One lip is in
    shadow, the other in the light."""
    rnd = random.Random(seed)
    zones = (                       # (x0, x1, y0, y1, direction across)
        (SL + 3, SR - 2, 16, 84, (1.0, 0.15)),          # stem: vertical blades
        (SR + 2, ARM_X - 8, 14, 44, (4.0, 7.0)),        # upper arm
        (SR + 2, LEG_X - 8, 50, 86, (5.0, -8.0)),       # lower arm
    )
    out = []
    for x0, x1, y0, y1, d in zones:
        for _ in range(5):
            u = unit((d[0] + rnd.uniform(-0.6, 0.6), d[1] + rnd.uniform(-0.6, 0.6)))
            L = rnd.uniform(5.0, 17.0)
            cx, cy = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
            p0 = (cx - u[0] * L / 2, cy - u[1] * L / 2)
            n = rnd.randint(2, 5)
            ps = [p0]
            for i in range(1, n + 1):
                t = i / n
                o = rnd.uniform(-0.9, 0.9) if i < n else 0.0
                ps.append((p0[0] + u[0] * L * t - u[1] * o, p0[1] + u[1] * L * t + u[0] * o))
            w = rnd.uniform(0.11, 0.3)
            lit = rnd.random() < 0.6          # not all of them catch the light
            out.append((ps, w, lit))
    return out

def fracture(ps, w, lit, fract=None):
    fract = fract or FRACT
    r = [(ribbon(ps, [w * 1.7] * len(ps)), fract["dark"])]
    if lit:
        r.append((ribbon(ps, [w] * len(ps), w * 0.8), fract["light"]))
    return r

# -------------------------------------------------------- the open crack
# A break has neither parallel lips, nor an even width, nor a continuous
# highlight. Everything here is irregular at the small scale: the path
# wanders, each lip drifts on its own, the width pinches and swells, the
# thread of light is intermittent, and chips are missing along the edges.
#
# This is the version the drawing moved away from — the filled seam below
# is what ships. It is kept because draw.py can still render it.
VEIN_STEM = [(17.0, 84.0), (23.0, 69.0), (19.0, 56.0), (25.0, 43.5), (21.0, 29.0), (23.5, 14.0)]
VEIN_ARM  = [(25.0, 43.5), (39.0, 39.0), (54.0, 30.5), (68.0, 23.0), (81.0, 17.0)]
W_STEM = [0.0, 1.45, 1.05, 1.5, 0.95, 0.0]
W_ARM  = [1.5, 1.35, 1.2, 0.9, 0.0]

def ribbon2(ps, left, right):
    """A ribbon whose two lips are independent."""
    n = len(ps)
    nor = [(lambda u: (-u[1], u[0]))(unit(sub(ps[min(i + 1, n - 1)], ps[max(i - 1, 0)]))) for i in range(n)]
    a = [(ps[i][0] + nor[i][0] * left[i], ps[i][1] + nor[i][1] * left[i]) for i in range(n)]
    b = [(ps[i][0] - nor[i][0] * right[i], ps[i][1] - nor[i][1] * right[i]) for i in range(n)]
    return a + b[::-1]

def noise(n, rnd, amp, smoothing=4):
    """Smoothed noise. Noise uncorrelated from one point to the next gives
    saw teeth; a fracture, by contrast, drifts slowly."""
    v = [rnd.uniform(-1.0, 1.0) for _ in range(n)]
    for _ in range(smoothing):
        v = [(v[max(i - 1, 0)] + 2.0 * v[i] + v[min(i + 1, n - 1)]) / 4.0 for i in range(n)]
    m = max(1e-6, max(abs(x) for x in v))
    return [x / m * amp for x in v]

def densify(ps, ws, step, amp, rnd):
    """Resamples the path and makes it wander. Returns the points and the
    base width interpolated at each of them."""
    pts_, wid, nrm = [], [], []
    for i in range(len(ps) - 1):
        p0, p1 = ps[i], ps[i + 1]
        d = sub(p1, p0)
        L = math.hypot(*d)
        k = max(1, int(L / step))
        u = unit(d); nn = (-u[1], u[0])
        for j in range(k):
            t = j / k
            pts_.append((p0[0] + d[0] * t, p0[1] + d[1] * t))
            nrm.append(nn)
            wid.append(ws[i] + (ws[i + 1] - ws[i]) * t)
    pts_.append(ps[-1]); nrm.append(nrm[-1]); wid.append(ws[-1])
    o = noise(len(pts_), rnd, amp)
    pts_ = [(p[0] + n_[0] * o[i], p[1] + n_[1] * o[i])
            for i, (p, n_) in enumerate(zip(pts_, nrm))]
    return pts_, wid

def _runs(n, rnd, lmin, lmax, gmin, gmax):
    """Cuts [0,n[ into stretches separated by gaps: a real highlight is
    never continuous."""
    out, i = [], rnd.randint(0, gmax)
    while i < n - 2:
        j = min(n - 1, i + rnd.randint(lmin, lmax))
        if j - i >= 2:
            out.append(list(range(i, j + 1)))
        i = j + rnd.randint(gmin, gmax)
    return out

def open_crack(seed, tints=None):
    """Every piece of the break, in painting order."""
    T = tints or SEAM
    rnd = random.Random(seed)
    out = []
    traces = []
    for ps, ws in ((VEIN_STEM, W_STEM), (VEIN_ARM, W_ARM)):
        P, W = densify(ps, ws, 1.7, 0.32, rnd)
        n = len(P)
        # the width pinches and swells, and the two lips are uncorrelated
        bl, br_ = noise(n, rnd, 0.42), noise(n, rnd, 0.42)
        g = [max(0.0, W[i] * (1.0 + bl[i]) * 0.92) for i in range(n)]
        d = [max(0.0, W[i] * (1.0 + br_[i]) * 0.92) for i in range(n)]
        traces.append((P, W, g, d))

        out.append((ribbon2(P, g, d), T["hollow"]))
        # the floor is not uniform: in places the break runs deeper.
        # Always dark, never pale: that is what keeps the line continuous.
        for idx in _runs(n, rnd, 2, 6, 1, 4):
            k = [max(0.0, g[i] * rnd.uniform(0.25, 0.6)) for i in idx]
            l = [max(0.0, d[i] * rnd.uniform(0.25, 0.6)) for i in idx]
            out.append((ribbon2([P[i] for i in idx], k, l), T["floor"]))
        # the far wall catches the light, in stretches. It stays on the far
        # side: the hollow must never be covered right across.
        for idx in _runs(n, rnd, 3, 9, 1, 3):
            k = [d[i] * rnd.uniform(-0.45, -0.25) for i in idx]
            l = [d[i] * rnd.uniform(0.8, 1.05) for i in idx]
            out.append((ribbon2([P[i] for i in idx], k, l), T["far_wall"]))
        # the thread along the near lip: intermittent, and uneven in width
        for idx in _runs(n, rnd, 2, 7, 1, 5):
            k = [g[i] * rnd.uniform(1.0, 1.35) for i in idx]
            l = [-g[i] * rnd.uniform(0.55, 0.85) for i in idx]
            out.append((ribbon2([P[i] for i in idx], k, l), T["lip"]))
        # chips missing from the lips
        for _ in range(int(n * 0.11)):
            i = rnd.randrange(n)
            if W[i] < 0.5:
                continue
            u = unit(sub(P[min(i + 1, n - 1)], P[max(i - 1, 0)])); nn = (-u[1], u[0])
            side = rnd.choice((1.0, -1.0))
            e = (g[i] if side > 0 else -d[i]) * rnd.uniform(0.8, 1.3)
            out.append((fleck(rnd, P[i][0] + nn[0] * e, P[i][1] + nn[1] * e,
                              rnd.uniform(0.2, 0.48)),
                        T["hollow"] if rnd.random() < 0.7 else T["floor"]))
        # secondary cracks: short starts, which die out
        for _ in range(4):
            i = rnd.randrange(2, n - 2)
            u = unit(sub(P[i + 1], P[i - 1])); nn = (-u[1], u[0])
            side = rnd.choice((1.0, -1.0))
            L = rnd.uniform(3.5, 11.0)
            dirn = unit((nn[0] * side + u[0] * rnd.uniform(-0.8, 0.8),
                         nn[1] * side + u[1] * rnd.uniform(-0.8, 0.8)))
            br = [P[i]]
            for j in range(1, 5):
                t = j / 4
                o = rnd.uniform(-0.5, 0.5)
                br.append((P[i][0] + dirn[0] * L * t - dirn[1] * o,
                           P[i][1] + dirn[1] * L * t + dirn[0] * o))
            w0 = min(0.42, W[i] * 0.45)
            ws_ = [w0 * (1 - j / 4) ** 0.7 for j in range(5)]
            out.append((ribbon2(br, ws_, ws_), T["hollow"]))
            if rnd.random() < 0.5:
                h = [x * 0.45 for x in ws_]
                out.append((ribbon2(br, [-x * 0.3 for x in ws_], h), T["far_wall"]))
    return out, traces

# ----------------------------------------------------------- the resin
# The shipped version: the crack is not a void, it is FILLED. A resin —
# in mineralogy, a secondary vein sealing the fracture.
#
# What makes it read "filled" rather than "broken" is continuity: a
# smooth, unbroken meniscus along the near lip, clean parallel edges, no
# missing chips. The material is translucent, so the grain of the stone
# shows through — hence fill-opacity rather than a flat fill.
#
# Two doses: milky (you see at once that it is filled) or mineral (more
# discreet, more stone-like).
RESIN_MILKY = {
    "stone_lip":   ("#12305F", 0.64),   # the old break edge, underneath
    "body":        ("#9CC6F4", 0.60),   # the resin itself
    "core":        ("#7FB3EE", 0.42),   # thicker in the middle of the channel
    "meniscus":    ("#F2F8FF", 0.97),   # the bead that catches the light
    "sheen":       ("#C6DFFA", 0.32),   # light coming back off the other edge
    "bubble_pale": ("#F7FBFF", 0.9),
    "bubble_dark": ("#285AA6", 0.55),
}
RESIN_MINERAL = {
    "stone_lip":   ("#12305F", 0.6),
    "body":        ("#2B5EAE", 0.72),
    "core":        ("#1C4080", 0.45),
    "meniscus":    ("#CFE4FC", 0.92),
    "sheen":       ("#6CA2E8", 0.3),
    "bubble_pale": ("#DCEBFE", 0.85),
    "bubble_dark": ("#13336A", 0.6),
}

# On a light ground the stone is darker, so the resin does not need to
# be as pale to read as filled — and it must NOT be near-white: a white
# thread inside the mass would read as a gap punched through to the page,
# which is the one thing the filled seam exists to deny. The meniscus
# stops at 1.32:1 against white.
RESIN_ON_LIGHT = {
    "stone_lip":   ("#091B3C", 0.66),
    "body":        ("#7FAEE4", 0.58),
    "core":        ("#5E90D4", 0.44),
    "meniscus":    ("#DCE9FA", 0.95),
    "sheen":       ("#9CC0EC", 0.32),
    "bubble_pale": ("#EAF2FD", 0.88),
    "bubble_dark": ("#16305E", 0.55),
}

def resin(seed, tints):
    """The pieces of the filled vein. Returns (polygon, tint, opacity)."""
    rnd = random.Random(seed)
    out, traces = [], []
    T = tints
    for ps, ws in ((VEIN_STEM, W_STEM), (VEIN_ARM, W_ARM)):
        # Less drift than for an open break: the resin follows the
        # fracture, but its own surface is smooth.
        P, W = densify(ps, ws, 1.7, 0.26, rnd)
        n = len(P)
        bl, br_ = noise(n, rnd, 0.2), noise(n, rnd, 0.2)
        g = [max(0.0, W[i] * (1.0 + bl[i]) * 0.94) for i in range(n)]
        d = [max(0.0, W[i] * (1.0 + br_[i]) * 0.94) for i in range(n)]
        traces.append((P, W, g, d))

        # the stone lip, under the resin: the fracture stays legible, and
        # this dark edging sets the vein *in* the stone instead of leaving
        # it floating on top
        out.append((ribbon2(P, [x * 1.22 for x in g], [x * 1.22 for x in d]),) + T["stone_lip"])
        # the body, translucent: the grain shows through
        out.append((ribbon2(P, g, d),) + T["body"])
        # thicker in the middle of the channel
        out.append((ribbon2(P, [x * 0.52 for x in g], [x * 0.52 for x in d]),) + T["core"])
        # The meniscus: the resin climbing against the wall. This is what
        # says "filled" — because it is CONTINUOUS, where a break edge
        # gives a choppy highlight. It must stay a thread: wide, it bleeds
        # as soon as the size comes down.
        out.append((ribbon2(P, [x * 1.06 for x in g], [-x * 0.58 for x in g]),) + T["meniscus"])
        # light coming back off the far edge, more discreet
        out.append((ribbon2(P, [-x * 0.46 for x in d], [x * 1.0 for x in d]),) + T["sheen"])
        # bubbles caught in the resin
        for _ in range(int(n * 0.55)):
            i = rnd.randrange(n)
            if W[i] < 0.35:
                continue
            u = unit(sub(P[min(i + 1, n - 1)], P[max(i - 1, 0)])); nn = (-u[1], u[0])
            o = rnd.uniform(-g[i] * 0.6, d[i] * 0.6)
            r = rnd.uniform(0.1, 0.3) * (0.5 + W[i])
            key = "bubble_pale" if rnd.random() < 0.62 else "bubble_dark"
            out.append((fleck(rnd, P[i][0] + nn[0] * o + u[0] * rnd.uniform(-0.6, 0.6),
                              P[i][1] + nn[1] * o + u[1] * rnd.uniform(-0.6, 0.6), r),) + T[key])
        # secondary cracks, sealed as well
        for _ in range(4):
            i = rnd.randrange(2, n - 2)
            u = unit(sub(P[i + 1], P[i - 1])); nn = (-u[1], u[0])
            side = rnd.choice((1.0, -1.0))
            L = rnd.uniform(3.5, 10.0)
            dirn = unit((nn[0] * side + u[0] * rnd.uniform(-0.7, 0.7),
                         nn[1] * side + u[1] * rnd.uniform(-0.7, 0.7)))
            br = [P[i]]
            for j in range(1, 5):
                t = j / 4
                o = rnd.uniform(-0.35, 0.35)
                br.append((P[i][0] + dirn[0] * L * t - dirn[1] * o,
                           P[i][1] + dirn[1] * L * t + dirn[0] * o))
            w0 = min(0.4, W[i] * 0.42)
            ws_ = [w0 * (1 - j / 4) ** 0.7 for j in range(5)]
            out.append((ribbon2(br, ws_, ws_),) + T["body"])
            out.append((ribbon2(br, [x * 0.9 for x in ws_], [-x * 0.4 for x in ws_]),) + T["meniscus"])
    return out, traces

# ------------------------------------------------------------------- output
def n_(v):
    s = f"{v:.1f}".rstrip("0").rstrip("."); return s if s else "0"
def pts(s): return " ".join(f"{n_(x)},{n_(y)}" for x, y in s)
OUTER = chamfer(OUTLINE)

# ------------------------------------------------------------- the themes
# Everything the drawing needs to know about its ground, in one place.
# The geometry is shared: only the values change.
ON_DARK = {
    "name": "dark", "ground": GROUND, "rock": ROCK_DEEP, "bevel": BEVEL_HARD,
    "mica": MICA, "quartz": QUARTZ, "fract": FRACT, "resin": RESIN_MILKY,
    "crack": SEAM, "spangle": SPANGLE,
    "clear": PLANE_CLEAR, "shade": PLANE_SHADE,
    "icon_stone": ICON_STONE, "icon_seam": ICON_SEAM, "ink": INK,
}
ON_LIGHT = {
    "name": "light", "ground": GROUND_LIGHT, "rock": ROCK_LIGHT,
    "bevel": BEVEL_LIGHT, "mica": MICA_LIGHT, "quartz": QUARTZ_LIGHT,
    "fract": FRACT_LIGHT, "resin": RESIN_ON_LIGHT, "crack": SEAM,
    "spangle": SPANGLE_LIGHT,
    "clear": PLANE_CLEAR_LIGHT, "shade": PLANE_SHADE_LIGHT,
    "icon_stone": ICON_STONE_LIGHT, "icon_seam": ICON_SEAM_LIGHT,
    "ink": INK_LIGHT,
}
THEMES = {"dark": ON_DARK, "light": ON_LIGHT}

def luminance(hex_):
    c = [int(hex_[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def check_ground(theme, floor=3.0):
    """The keen lit edge is what draws the contour, so it is the one value
    that may never melt into the ground. Measured, not assumed: this is
    exactly the check the dark palette fails on white (1.21:1).

    The deepest facet is deliberately NOT checked. On a dark ground it is
    meant to sink into the background — that is the shadow side doing its
    job — and on a light ground it is the strongest edge there is."""
    keen = theme["bevel"][-1]
    got = contrast(keen, theme["ground"])
    assert got >= floor, (f'theme "{theme["name"]}": the keen edge {keen} gives only '
                          f"{got:.2f}:1 on {theme['ground']}, below {floor}:1")
    return got
