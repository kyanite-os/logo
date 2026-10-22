#!/usr/bin/env python3
"""Kyanite — tour 3. Un K taille dans un bloc, pour fond sombre.

Rien de symetrique : les deux branches n'ont ni la meme pente, ni la
meme longueur, ni la meme epaisseur ; les aretes longues portent des
decrochements ; les angles sont coupes inegalement.

La matiere est lue comme du granite : une structure large (les lames de
kyanite, qui donnent la lumiere), puis des plages de la taille d'un
cristal, puis un grain fin ou se melent des eclats clairs (quartz) et
des points sombres (mica). Trois echelles, aucune symetrie.

Une seule lumiere, venant du haut-gauche. Aucune perspective.
Polygones uniquement : aucun filtre, aucun bitmap, aucun degrade.
"""
import math, os, random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logo")
LIGHT = (-math.sqrt(0.5), -math.sqrt(0.5))

# ------------------------------------------------------------------ palette
# Taillee pour fond sombre : la masse reste franchement au-dessus du fond,
# le biseau haut-gauche porte la lumiere, les creux plongent.
ROCK = ["#1B3C78", "#22488B", "#28539D", "#2F5FAF", "#366BC0",
        "#3F78CE", "#4A86DA", "#5795E4", "#67A4EC"]
ROCK_DEEP = ["#15306A", "#1B3B7C", "#21468E", "#2851A0", "#2E5CB1",
             "#3668C1", "#3F75CE", "#4A83DA", "#5793E4"]
MICA   = ["#1C3C76", "#22477F"]   # points sombres (biotite)
QUARTZ = ["#86B6EE", "#A8CCF4"]   # eclats clairs (quartz)
BEVEL      = ["#17376F", "#21488F", "#3A74C8", "#72ACEE", "#BEDCFA"]
BEVEL_HARD = ["#112A58", "#1C4184", "#3A74C8", "#86B7F2", "#DBEBFF"]
SEAM = {"creux": "#15376E", "fond": "#0E2650", "aval": "#3570C4", "levre": "#8FBDF4"}
FRACT = {"dark": "#1E4588", "light": "#6CA2E8"}

# ---------------------------------------------------------------- geometrie
SL, SR = 10.0, 40.0          # jambage : 30 d'epaisseur, c'est le pilier
TOP, BOT = 10.0, 90.0
FORK = 48.0
ARM_Y0, ARM_Y1 = 22.0, FORK  # branche haute : pente 4/7
LEG_Y0, LEG_Y1 = FORK, 73.0  # branche basse : pente 5/8, attache plus courte
ARM_S, LEG_S = -4.0 / 7.0, 5.0 / 8.0      # pentes differentes : pas de miroir
ARM_X, LEG_X = 86.0, 88.0                 # bras courts : on tient dans le carre
X_ARM_TOP = SR + (ARM_Y0 - TOP) * 7.0 / 4.0
Y_ARM_TIP = ARM_Y1 + (ARM_X - SR) * ARM_S
Y_LEG_TIP = LEG_Y0 + (LEG_X - SR) * LEG_S
X_LEG_BOT = SR + (BOT - LEG_Y1) * 8.0 / 5.0

OUTLINE = [
    # Le sommet et le pied du jambage ne sont pas de meme nature.
    # En haut : une seule coupe oblique, franche, d'un seul coup.
    # En bas : a gauche un angle droit franc, le flanc d'aplomb jusqu'au
    # sol ; a droite un gradin, le coin reste en l'air.
    ((SL, 17.0),         (7.0, 8.0)),   # coin haut-gauche
    ((SR, TOP),          (4.5, 4.0)),   # haut du jambage, coupe nette
    ((SR, ARM_Y0),       (4.0, 5.0)),   # fond de l'encoche haute
    ((X_ARM_TOP, TOP),   (6.0, 5.0)),   # depart de la branche haute
    ((ARM_X, TOP),       (5.0, 3.5)),   # coin haut-droit
    ((ARM_X, Y_ARM_TIP), (3.5, 6.0)),   # bas du tranchant haut
    ((65.0, 34.5),       (0.0, 0.0)),   # decrochement
    ((SR, FORK),         (7.0, 6.0)),   # la fourche
    ((68.0, 66.6),       (0.0, 0.0)),   # decrochement
    ((LEG_X, Y_LEG_TIP), (5.0, 3.0)),   # haut du tranchant bas
    ((LEG_X, BOT),       (3.0, 5.0)),   # coin bas-droit
    ((X_LEG_BOT, BOT),   (5.0, 4.0)),   # depart de la branche basse
    ((SR, LEG_Y1),       (4.0, 2.0)),   # fond de l'encoche basse, remonte
    ((SR, 85.0),         (2.0, 2.0)),   # le coin DROIT du pied est casse :
    ((26.0, 85.0),       (2.0, 2.0)),   # un gradin, il reste en l'air
    ((26.0, BOT),        (2.0, 2.5)),
    ((SL, BOT),          (0.0, 0.0)),   # coin bas-gauche : angle droit franc,
    ((SL, 72.0),         (0.0, 0.0)),   # le flanc reste d'aplomb jusqu'ici
    ((9.1, 58.0),        (0.0, 0.0)),   # decrochements du flanc gauche
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

def verifie(outer, inner):
    """Un pan de biseau qui se retourne fabrique une dent. On verifie que
    chaque arete interieure va bien dans le meme sens que son exterieure."""
    n, mauvais = len(outer), []
    for i in range(n):
        j = (i + 1) % n
        uo = (outer[j][0] - outer[i][0], outer[j][1] - outer[i][1])
        ui = (inner[j][0] - inner[i][0], inner[j][1] - inner[i][1])
        if uo[0] * ui[0] + uo[1] * ui[1] < -1e-9:
            mauvais.append((i, outer[i], outer[j]))
    return mauvais

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
    # Sur une arete plus courte que le biseau, les deux pans voisins se
    # croiseraient et fabriqueraient une dent. On les referme en pointe.
    for _ in range(6):
        mauvais = verifie(poly, out)
        if not mauvais:
            break
        for i, _a, _b in mauvais:
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

# -------------------------------------------- lames de kyanite (structure)
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

# ------------------------------------------- ou en est-on dans la structure
def base_index(x, y):
    """Valeur de fond au point donne : sert a poser le grain sans
    effacer la lumiere."""
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

def brisee(p0, p1, n, amp, rnd):
    """Un plan de clivage n'est jamais une droite : on le brise en n
    segments, avec une petite derive perpendiculaire a chaque noeud."""
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
    """Lames d'une branche. Deux plans voisins partagent exactement la
    meme brisure : les lames pavent la bande sans jour."""
    rnd = random.Random(seed)
    run = (XF - SR) * slope
    bords = [brisee((SR, y), (XF, y + run + d), 6, 1.15, rnd)
             for y, d in zip(anchors, deltas)]
    return [(bords[i] + bords[i + 1][::-1], ramp[vals[i]]) for i in range(len(vals))]

def blades_stem(ramp, seed):
    rnd = random.Random(seed)
    bords = [brisee((x, -8.0), (x + d, 108.0), 7, 0.95, rnd)
             for x, d in zip(STEM_X, STEM_D)]
    return [(bords[i] + bords[i + 1][::-1], ramp[STEM_V[i]]) for i in range(len(STEM_V))]

def fines_axis(y0, y1, slope, n, ramp, seed):
    """Lamelles fines prises entre les grandes. Ce sont des eclats courts,
    pas des traits qui traversent : c'est ce qui empeche l'oeil de
    retomber sur la forme de base."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        y = rnd.uniform(y0, y1)
        w = rnd.uniform(0.25, 0.85)
        xa = rnd.uniform(SR - 2.0, SR + 46.0)
        xb = xa + rnd.uniform(14.0, 40.0)
        ya, yb = y + (xa - SR) * slope, y + (xb - SR) * slope
        drv = rnd.uniform(-1.6, 1.6)
        a = brisee((xa, ya), (xb, yb + drv), 4, 0.6, rnd)
        b = brisee((xa, ya + w), (xb, yb + w + drv), 4, 0.6, rnd)
        v = base_index(min(XF - 1, (xa + xb) / 2), (ya + yb) / 2 + w / 2)
        out.append((a + b[::-1], ramp[max(0, min(len(ramp) - 1, v + rnd.choice((-1, -1, 1, 1, 2))))]))
    return out

def fines_stem(n, ramp, seed):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(SL - 1, SR + 1)
        w = rnd.uniform(0.25, 0.7)
        ya = rnd.uniform(4.0, 70.0)
        yb = ya + rnd.uniform(16.0, 42.0)
        drv = rnd.uniform(-1.4, 1.4)
        a = brisee((x, ya), (x + drv, yb), 4, 0.55, rnd)
        b = brisee((x + w, ya), (x + w + drv, yb), 4, 0.55, rnd)
        v = base_index(x + w / 2, (ya + yb) / 2)
        out.append((a + b[::-1], ramp[max(0, min(len(ramp) - 1, v + rnd.choice((-1, -1, 1, 1))))]))
    return out

# -------------------------------------------- lames de kyanite (structure)
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

# ------------------------------------------- ou en est-on dans la structure
def base_index(x, y):
    """Valeur de fond au point donne : sert a poser le grain sans
    effacer la lumiere."""
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

def brisee(p0, p1, n, amp, rnd):
    """Un plan de clivage n'est jamais une droite : on le brise en n
    segments, avec une petite derive perpendiculaire a chaque noeud."""
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
    """Lames d'une branche. Deux plans voisins partagent exactement la
    meme brisure : les lames pavent la bande sans jour."""
    rnd = random.Random(seed)
    run = (XF - SR) * slope
    bords = [brisee((SR, y), (XF, y + run + d), 6, 1.15, rnd)
             for y, d in zip(anchors, deltas)]
    return [(bords[i] + bords[i + 1][::-1], ramp[vals[i]]) for i in range(len(vals))]

def blades_stem(ramp, seed):
    rnd = random.Random(seed)
    bords = [brisee((x, -8.0), (x + d, 108.0), 7, 0.95, rnd)
             for x, d in zip(STEM_X, STEM_D)]
    return [(bords[i] + bords[i + 1][::-1], ramp[STEM_V[i]]) for i in range(len(STEM_V))]

def fines_axis(y0, y1, slope, n, ramp, seed):
    """Lamelles fines prises entre les grandes : c'est ce qui empeche
    l'oeil de retomber sur la forme de base."""
    rnd = random.Random(seed)
    run = (XF - SR) * slope
    out = []
    for _ in range(n):
        y = rnd.uniform(y0, y1)
        w = rnd.uniform(0.25, 0.8)
        d0, d1 = rnd.uniform(-2.5, 2.5), rnd.uniform(-2.5, 2.5)
        a = brisee((SR, y), (XF, y + run + d0), 5, 0.9, rnd)
        b = brisee((SR, y + w), (XF, y + w + run + d1), 5, 0.9, rnd)
        v = base_index(SR + 12.0, y + (12.0 * slope) + w / 2)
        out.append((a + b[::-1], ramp[max(0, min(len(ramp) - 1, v + rnd.choice((-1, -1, 1, 1, 2))))]))
    return out

def fines_stem(n, ramp, seed):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(SL - 1, SR + 1)
        w = rnd.uniform(0.25, 0.7)
        a = brisee((x, -8.0), (x + rnd.uniform(-2.0, 2.0), 108.0), 6, 0.8, rnd)
        b = brisee((x + w, -8.0), (x + w + rnd.uniform(-2.0, 2.0), 108.0), 6, 0.8, rnd)
        v = base_index(x + w / 2, 50.0)
        out.append((a + b[::-1], ramp[max(0, min(len(ramp) - 1, v + rnd.choice((-1, -1, 1, 1))))]))
    return out

KK = 14.0
BAND_STEM = [(-8, -8), (SR, -8), (SR, 108), (-8, 108)]
BAND_ARM = [(SR, ARM_Y0), (SR + 7 * KK, ARM_Y0 - 4 * KK), (SR + 7 * KK, ARM_Y1 - 4 * KK), (SR, ARM_Y1)]
BAND_LEG = [(SR, LEG_Y0), (SR + 8 * KK, LEG_Y0 + 5 * KK), (SR + 8 * KK, LEG_Y1 + 5 * KK), (SR, LEG_Y1)]

# ------------------------------------------------------------ grain granitique
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

def granite(seed, ramp):
    """Trois echelles : plages, grains, eclats. Position en grille brouillee
    pour couvrir sans faire de paquets."""
    rnd = random.Random(seed)
    res = []
    # la densite varie d'un endroit a l'autre : la roche n'est pas reguliere
    nids = [(rnd.uniform(12, 84), rnd.uniform(12, 84), rnd.uniform(14, 26)) for _ in range(6)]
    def densite(x, y):
        k = 0.0
        for nx, ny, nr in nids:
            dd = math.hypot(x - nx, y - ny) / nr
            if dd < 1.0:
                k += (1.0 - dd) ** 2
        return min(1.0, k)
    for cols, rmin, rmax, kind, taux in ((9, 2.4, 4.3, "plage", 0.78),
                                         (19, 0.75, 1.7, "grain", 0.70),
                                         (28, 0.26, 0.62, "eclat", 0.52)):
        step = 86.0 / cols
        for gy in range(cols):
            for gx in range(cols):
                cx = 7.0 + (gx + rnd.uniform(0.05, 0.95)) * step
                cy = 7.0 + (gy + rnd.uniform(0.05, 0.95)) * step
                if rnd.random() > taux * (0.45 + 0.85 * densite(cx, cy)):
                    continue
                r = rnd.uniform(rmin, rmax)
                b = base_index(cx, cy)
                if kind == "plage":
                    c = ramp[max(0, min(len(ramp) - 1, b + rnd.choice((-1, -1, 1, 1))))]
                elif kind == "grain":
                    c = ramp[max(0, min(len(ramp) - 1, b + rnd.choice((-2, -1, -1, 1, 1, 2))))]
                else:
                    u = rnd.random()
                    if u < 0.42:
                        c = MICA[rnd.randint(0, 1)]
                    elif u < 0.72:
                        c = QUARTZ[rnd.randint(0, 1)]
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
    """Cassures en travers du clivage. Longueurs, largeurs et contrastes
    tous differents : une cassure reguliere se lit comme un trait dessine.
    Une levre est a l'ombre, l'autre au jour."""
    rnd = random.Random(seed)
    zones = (                       # (x0, x1, y0, y1, direction en travers)
        (SL + 3, SR - 2, 16, 84, (1.0, 0.15)),          # jambage : lames verticales
        (SR + 2, ARM_X - 8, 14, 44, (4.0, 7.0)),        # branche haute
        (SR + 2, LEG_X - 8, 50, 86, (5.0, -8.0)),       # branche basse
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
            clair = rnd.random() < 0.6        # toutes ne prennent pas la lumiere
            out.append((ps, w, clair))
    return out

def fracture(ps, w, clair):
    r = [(ribbon(ps, [w * 1.7] * len(ps)), FRACT["dark"])]
    if clair:
        r.append((ribbon(ps, [w] * len(ps), w * 0.8), FRACT["light"]))
    return r

# -------------------------------------------------------------- la fente
# Une cassure n'a pas deux levres paralleles, ni une largeur reguliere,
# ni un reflet continu. Tout ici est irregulier a la petite echelle :
# le trace divague, chaque levre a sa propre derive, la largeur pince et
# gonfle, le filet de lumiere est intermittent, et des eclats manquent
# sur les bords.
VEIN_STEM = [(17.0, 84.0), (23.0, 69.0), (19.0, 56.0), (25.0, 43.5), (21.0, 29.0), (23.5, 14.0)]
VEIN_ARM  = [(25.0, 43.5), (39.0, 39.0), (54.0, 30.5), (68.0, 23.0), (81.0, 17.0)]
W_STEM = [0.0, 1.45, 1.05, 1.5, 0.95, 0.0]
W_ARM  = [1.5, 1.35, 1.2, 0.9, 0.0]

def ribbon2(ps, gauche, droite):
    """Ruban dont les deux levres sont independantes."""
    n = len(ps)
    nor = [(lambda u: (-u[1], u[0]))(unit(sub(ps[min(i + 1, n - 1)], ps[max(i - 1, 0)]))) for i in range(n)]
    a = [(ps[i][0] + nor[i][0] * gauche[i], ps[i][1] + nor[i][1] * gauche[i]) for i in range(n)]
    b = [(ps[i][0] - nor[i][0] * droite[i], ps[i][1] - nor[i][1] * droite[i]) for i in range(n)]
    return a + b[::-1]

def bruit(n, rnd, amp, lissage=4):
    """Bruit lisse. Un bruit decorrele d'un point au suivant donne des
    dents de scie ; une cassure, elle, derive lentement."""
    v = [rnd.uniform(-1.0, 1.0) for _ in range(n)]
    for _ in range(lissage):
        v = [(v[max(i - 1, 0)] + 2.0 * v[i] + v[min(i + 1, n - 1)]) / 4.0 for i in range(n)]
    m = max(1e-6, max(abs(x) for x in v))
    return [x / m * amp for x in v]

def densifie(ps, ws, pas, amp, rnd):
    """Reechantillonne le trace et le fait divaguer. Renvoie les points
    et la largeur de base interpolee en chacun d'eux."""
    pts_, wid, nrm = [], [], []
    for i in range(len(ps) - 1):
        p0, p1 = ps[i], ps[i + 1]
        d = sub(p1, p0)
        L = math.hypot(*d)
        k = max(1, int(L / pas))
        u = unit(d); nn = (-u[1], u[0])
        for j in range(k):
            t = j / k
            pts_.append((p0[0] + d[0] * t, p0[1] + d[1] * t))
            nrm.append(nn)
            wid.append(ws[i] + (ws[i + 1] - ws[i]) * t)
    pts_.append(ps[-1]); nrm.append(nrm[-1]); wid.append(ws[-1])
    o = bruit(len(pts_), rnd, amp)
    pts_ = [(p[0] + n_[0] * o[i], p[1] + n_[1] * o[i])
            for i, (p, n_) in enumerate(zip(pts_, nrm))]
    return pts_, wid

def _tronçons(n, rnd, lmin, lmax, gmin, gmax):
    """Decoupe [0,n[ en morceaux separes par des trous : un reflet reel
    n'est jamais continu."""
    out, i = [], rnd.randint(0, gmax)
    while i < n - 2:
        j = min(n - 1, i + rnd.randint(lmin, lmax))
        if j - i >= 2:
            out.append(list(range(i, j + 1)))
        i = j + rnd.randint(gmin, gmax)
    return out

def fente(seed):
    """Tous les morceaux de la cassure, dans l'ordre de pose."""
    rnd = random.Random(seed)
    out = []
    traces = []
    for ps, ws in ((VEIN_STEM, W_STEM), (VEIN_ARM, W_ARM)):
        P, W = densifie(ps, ws, 1.7, 0.32, rnd)
        n = len(P)
        # la largeur pince et gonfle, et les deux levres sont decorrelees
        bg, bd = bruit(n, rnd, 0.42), bruit(n, rnd, 0.42)
        g = [max(0.0, W[i] * (1.0 + bg[i]) * 0.92) for i in range(n)]
        d = [max(0.0, W[i] * (1.0 + bd[i]) * 0.92) for i in range(n)]
        traces.append((P, W, g, d))

        out.append((ribbon2(P, g, d), SEAM["creux"]))
        # le fond n'est pas uniforme : par endroits la cassure est plus
        # profonde. Toujours sombre, jamais clair : c'est ce qui garde
        # la continuite du trait.
        for idx in _tronçons(n, rnd, 2, 6, 1, 4):
            k = [max(0.0, g[i] * rnd.uniform(0.25, 0.6)) for i in idx]
            l = [max(0.0, d[i] * rnd.uniform(0.25, 0.6)) for i in idx]
            out.append((ribbon2([P[i] for i in idx], k, l), SEAM["fond"]))
        # la paroi aval prend la lumiere, par plages. Elle reste du cote
        # aval : le creux ne doit jamais etre recouvert de part en part.
        for idx in _tronçons(n, rnd, 3, 9, 1, 3):
            k = [d[i] * rnd.uniform(-0.45, -0.25) for i in idx]
            l = [d[i] * rnd.uniform(0.8, 1.05) for i in idx]
            out.append((ribbon2([P[i] for i in idx], k, l), SEAM["aval"]))
        # le filet sur la levre amont : intermittent, et d'epaisseur variable
        for idx in _tronçons(n, rnd, 2, 7, 1, 5):
            k = [g[i] * rnd.uniform(1.0, 1.35) for i in idx]
            l = [-g[i] * rnd.uniform(0.55, 0.85) for i in idx]
            out.append((ribbon2([P[i] for i in idx], k, l), SEAM["levre"]))
        # eclats manquants sur les levres
        for _ in range(int(n * 0.11)):
            i = rnd.randrange(n)
            if W[i] < 0.5:
                continue
            u = unit(sub(P[min(i + 1, n - 1)], P[max(i - 1, 0)])); nn = (-u[1], u[0])
            sens = rnd.choice((1.0, -1.0))
            e = (g[i] if sens > 0 else -d[i]) * rnd.uniform(0.8, 1.3)
            out.append((fleck(rnd, P[i][0] + nn[0] * e, P[i][1] + nn[1] * e,
                              rnd.uniform(0.2, 0.48)),
                        SEAM["creux"] if rnd.random() < 0.7 else SEAM["fond"]))
        # fissures secondaires : de courts departs, qui s'eteignent
        for _ in range(4):
            i = rnd.randrange(2, n - 2)
            u = unit(sub(P[i + 1], P[i - 1])); nn = (-u[1], u[0])
            sens = rnd.choice((1.0, -1.0))
            L = rnd.uniform(3.5, 11.0)
            dirn = unit((nn[0] * sens + u[0] * rnd.uniform(-0.8, 0.8),
                         nn[1] * sens + u[1] * rnd.uniform(-0.8, 0.8)))
            br = [P[i]]
            for j in range(1, 5):
                t = j / 4
                o = rnd.uniform(-0.5, 0.5)
                br.append((P[i][0] + dirn[0] * L * t - dirn[1] * o,
                           P[i][1] + dirn[1] * L * t + dirn[0] * o))
            w0 = min(0.42, W[i] * 0.45)
            ws_ = [w0 * (1 - j / 4) ** 0.7 for j in range(5)]
            out.append((ribbon2(br, ws_, ws_), SEAM["creux"]))
            if rnd.random() < 0.5:
                h = [x * 0.45 for x in ws_]
                out.append((ribbon2(br, [-x * 0.3 for x in ws_], h), SEAM["aval"]))
    return out, traces

# ------------------------------------------------------------- la resine
# Variante : la fente n'est pas un vide, elle est COMBLEE. Une resine
# — en mineralogie, un filon secondaire qui colmate la fracture.
#
# Ce qui fait lire « rempli » plutot que « casse », c'est la continuite :
# un menisque lisse et ininterrompu le long de la levre amont, des bords
# nets et paralleles, aucun eclat manquant. La matiere est translucide,
# donc le grain de la pierre transparait au travers — d'ou fill-opacity
# plutot qu'un aplat.
#
# Deux dosages : laiteuse (on voit tout de suite que c'est rempli) ou
# transparente (plus minerale, plus discrete).
RESINE_CLAIRE = {
    "levre_pierre": ("#14346C", 0.55),   # l'ancienne arete de cassure, dessous
    "corps":        ("#A8CEF6", 0.62),   # la resine elle-meme
    "coeur":        ("#86B8F0", 0.38),   # plus epaisse au milieu
    "menisque":     ("#EAF4FF", 0.95),   # le bourrelet qui prend la lumiere
    "reflet":       ("#CBE2FB", 0.34),   # retour de lumiere sur l'autre bord
    "bulle_claire": ("#F2F8FF", 0.9),
    "bulle_sombre": ("#2A5BA8", 0.55),
}
RESINE_SOMBRE = {
    "levre_pierre": ("#12305F", 0.6),
    "corps":        ("#2B5EAE", 0.72),
    "coeur":        ("#1C4080", 0.45),
    "menisque":     ("#CFE4FC", 0.92),
    "reflet":       ("#6CA2E8", 0.3),
    "bulle_claire": ("#DCEBFE", 0.85),
    "bulle_sombre": ("#13336A", 0.6),
}

def resine(seed, teintes):
    """Les morceaux du filon comble. Renvoie (polygone, teinte, opacite)."""
    rnd = random.Random(seed)
    out, traces = [], []
    T = teintes
    for ps, ws in ((VEIN_STEM, W_STEM), (VEIN_ARM, W_ARM)):
        # Moins de derive que pour une cassure ouverte : la resine epouse
        # la fracture mais sa surface, elle, est lisse.
        P, W = densifie(ps, ws, 1.7, 0.26, rnd)
        n = len(P)
        bg, bd = bruit(n, rnd, 0.2), bruit(n, rnd, 0.2)
        g = [max(0.0, W[i] * (1.0 + bg[i]) * 0.94) for i in range(n)]
        d = [max(0.0, W[i] * (1.0 + bd[i]) * 0.94) for i in range(n)]
        traces.append((P, W, g, d))

        # la levre de pierre, sous la resine : la fracture reste lisible
        out.append((ribbon2(P, [x * 1.2 for x in g], [x * 1.2 for x in d]),) + T["levre_pierre"])
        # le corps, translucide : le grain transparait
        out.append((ribbon2(P, g, d),) + T["corps"])
        # plus epaisse au milieu du chenal
        out.append((ribbon2(P, [x * 0.52 for x in g], [x * 0.52 for x in d]),) + T["coeur"])
        # le menisque : continu, c'est lui qui dit « rempli »
        out.append((ribbon2(P, [x * 1.02 for x in g], [-x * 0.66 for x in g]),) + T["menisque"])
        # retour de lumiere sur le bord aval
        out.append((ribbon2(P, [-x * 0.5 for x in d], [x * 0.98 for x in d]),) + T["reflet"])
        # bulles prises dans la resine
        for _ in range(int(n * 0.55)):
            i = rnd.randrange(n)
            if W[i] < 0.35:
                continue
            u = unit(sub(P[min(i + 1, n - 1)], P[max(i - 1, 0)])); nn = (-u[1], u[0])
            o = rnd.uniform(-g[i] * 0.6, d[i] * 0.6)
            r = rnd.uniform(0.1, 0.3) * (0.5 + W[i])
            cle = "bulle_claire" if rnd.random() < 0.62 else "bulle_sombre"
            out.append((fleck(rnd, P[i][0] + nn[0] * o + u[0] * rnd.uniform(-0.6, 0.6),
                              P[i][1] + nn[1] * o + u[1] * rnd.uniform(-0.6, 0.6), r),) + T[cle])
        # fissures secondaires, comblees elles aussi
        for _ in range(4):
            i = rnd.randrange(2, n - 2)
            u = unit(sub(P[i + 1], P[i - 1])); nn = (-u[1], u[0])
            sens = rnd.choice((1.0, -1.0))
            L = rnd.uniform(3.5, 10.0)
            dirn = unit((nn[0] * sens + u[0] * rnd.uniform(-0.7, 0.7),
                         nn[1] * sens + u[1] * rnd.uniform(-0.7, 0.7)))
            br = [P[i]]
            for j in range(1, 5):
                t = j / 4
                o = rnd.uniform(-0.35, 0.35)
                br.append((P[i][0] + dirn[0] * L * t - dirn[1] * o,
                           P[i][1] + dirn[1] * L * t + dirn[0] * o))
            w0 = min(0.4, W[i] * 0.42)
            ws_ = [w0 * (1 - j / 4) ** 0.7 for j in range(5)]
            out.append((ribbon2(br, ws_, ws_),) + T["corps"])
            out.append((ribbon2(br, [x * 0.9 for x in ws_], [-x * 0.4 for x in ws_]),) + T["menisque"])
    return out, traces

# ------------------------------------------------------------------- sortie
def n_(v):
    s = f"{v:.1f}".rstrip("0").rstrip("."); return s if s else "0"
def pts(s): return " ".join(f"{n_(x)},{n_(y)}" for x, y in s)
OUTER = chamfer(OUTLINE)

def build(title, ramp, bev, seed, vein):
    L = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"',
         '     role="img" aria-label="Kyanite">',
         f'  <title>Kyanite — {title}</title>', '',
         '  <defs>',
         f'    <clipPath id="bloc"><polygon points="{pts(OUTER)}"/></clipPath>',
         f'    <clipPath id="jambage"><polygon points="{pts(BAND_STEM)}"/></clipPath>',
         f'    <clipPath id="haute"><polygon points="{pts(BAND_ARM)}"/></clipPath>',
         f'    <clipPath id="basse"><polygon points="{pts(BAND_LEG)}"/></clipPath>',
         '  </defs>', '',
         '  <g clip-path="url(#bloc)">',
         f'    <polygon points="{pts(OUTER)}" fill="{ramp[4]}"/>', '']
    for cid, nom, bl in (("jambage", "jambage", blades_stem(ramp)),
                         ("haute", "branche haute", blades_axis(ARM_A, ARM_D, ARM_S, ARM_V, ramp)),
                         ("basse", "branche basse", blades_axis(LEG_A, LEG_D, LEG_S, LEG_V, ramp))):
        L.append(f'    <!-- {nom} : lames de kyanite -->')
        L.append(f'    <g clip-path="url(#{cid})">')
        for poly, c in bl:
            L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
        L.append('    </g>')
    L += ['', '    <!-- grain : plages, grains, eclats de quartz et points de mica -->', '    <g>']
    for poly, c in granite(seed, ramp):
        L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
    L.append('    </g>')
    L += ['', '    <!-- fractures en travers du clivage -->']
    for ps, w in FRACTURES:
        for poly, c in fracture(ps, w):
            L.append(f'    <polygon points="{pts(poly)}" fill="{c}"/>')
    if vein:
        L += ['', "    <!-- filon : la paroi a l'ombre, puis le coeur clair -->"]
        for seq, w in ((VEIN_STEM, W_STEM), (VEIN_ARM, W_ARM)):
            L.append(f'    <polygon points="{pts(ribbon(seq, [x * 1.45 for x in w]))}" fill="{SEAM["wall"]}"/>')
            L.append(f'    <polygon points="{pts(ribbon(seq, [x * 1.15 for x in w], 0.4))}" fill="{SEAM["halo"]}"/>')
            L.append(f'    <polygon points="{pts(ribbon(seq, [x * 0.8 for x in w], 0.62))}" fill="{SEAM["core"]}"/>')
    L += ['', '    <!-- biseau : un pan par arete, une seule lumiere haut-gauche -->']
    for poly, c in bevel_ring(OUTER, inset(OUTER, BEVEL_W), bev):
        L.append(f'    <polygon points="{pts(poly)}" fill="{c}"/>')
    L += ['  </g>', '</svg>']
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    VARIANTS = [
        ("variante-i-granite", "I — granite", ROCK, BEVEL, 20260, False),
        ("variante-j-filon", "J — granite + filon", ROCK, BEVEL, 20260, True),
        ("variante-k-mine", "K — fond de mine", ROCK_DEEP, BEVEL_HARD, 81177, True),
    ]
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.startswith("variante-"):
            os.remove(os.path.join(OUT, f))
    for slug, title, r, b, s, v in VARIANTS:
        p = os.path.join(OUT, slug + ".svg")
        open(p, "w").write(build(title, r, b, s, v))
        print(f"ecrit {slug}  {os.path.getsize(p)//1024} Ko")
