#!/usr/bin/env python3
"""Kyanite — tour 4. Variante K (fond de mine), enrichie.

Deux ajouts :

1. Des PAILLETTES dans le filon : de petits eclats anguleux et des
   losanges, semes le long de la crevasse, serres vers la levre eclairee.

2. Des PLANS TRANSLUCIDES : la kyanite est un mineral transparent. On
   superpose de larges plans a faible opacite, suivant trois directions
   de clivage qui ne sont celles d'aucune des faces visibles. La ou ils
   se croisent, la valeur s'accumule : c'est ce qui fait lire l'epaisseur
   du cristal plutot qu'une surface peinte.

   L'opacite est un attribut SVG ordinaire (fill-opacity), pas un filtre :
   le rendu reste identique partout, y compris en icone systeme.
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bloc as G

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logo")

GLINT = ["#C6DEFA", "#A8CCF4", "#88B8F0", "#6AA0E8", "#4D86DA"]
CLEAR = "#BBD8F8"      # plan translucide clair
SHADE = "#0C2149"      # plan translucide sombre

# ---------------------------------------------------- plans de transparence
# (direction, decalage, largeur, teinte, opacite)
PLANS = [
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
# deux plans passes par-dessus tout : la lumiere qui traverse la masse
PLANS_DESSUS = [((9, -3), -20, 18, CLEAR, 0.043), ((2, 7), 16, 14, CLEAR, 0.031),
                ((-3, 8), 6, 9, CLEAR, 0.031)]
# un grand coin de lumiere, entrant par le haut-gauche
COIN = ([(-10, -10), (62, -10), (-10, 58)], CLEAR, 0.07)

def plan(d, o, w, rnd, long_=150.0):
    """Un plan interne n'a pas de bord rectiligne : on le brise, sinon
    l'oeil lit une bande posee sur le dessin."""
    u = G.unit(d); nn = (-u[1], u[0])
    c = (50 + nn[0] * o, 50 + nn[1] * o)
    def bord(k):
        p0 = (c[0] + nn[0] * k - u[0] * long_, c[1] + nn[1] * k - u[1] * long_)
        p1 = (c[0] + nn[0] * k + u[0] * long_, c[1] + nn[1] * k + u[1] * long_)
        return G.brisee(p0, p1, 7, max(0.5, w * 0.16), rnd)
    return bord(w / 2) + bord(-w / 2)[::-1]

# ------------------------------------------------------------- paillettes
def losange(cx, cy, r, rot, ap=0.45):
    return [(cx + math.cos(rot + i * math.pi / 2) * (r if i % 2 == 0 else r * ap),
             cy + math.sin(rot + i * math.pi / 2) * (r if i % 2 == 0 else r * ap))
            for i in range(4)]

def paillettes(seed, force, traces):
    """Semees le long de la crevasse, serrees vers la levre eclairee."""
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
                le = rnd.uniform(-0.8, 0.8)
                cx = P[i][0] + nn[0] * off + u[0] * le
                cy = P[i][1] + nn[1] * off + u[1] * le
                r = rnd.uniform(0.09, 0.3) * (0.5 + W[i]) * force
                c = GLINT[min(4, int(rnd.random() * 5.4))]
                out.append((G.fleck(rnd, cx, cy, r * 1.35) if rnd.random() < 0.45
                            else losange(cx, cy, r, rnd.random() * math.pi,
                                         rnd.uniform(0.28, 0.72)), c))
    # quelques eclats isoles pris dans la roche, autour de la fente
    for cx, cy in ((33.0, 25.0), (15.5, 46.0), (34.0, 62.0), (50.0, 36.0), (70.0, 26.0)):
        r = rnd.uniform(0.3, 0.55) * force
        out.append((losange(cx, cy, r, rnd.random() * math.pi, 0.4), GLINT[rnd.randint(2, 3)]))
    return out

# ------------------------------------------------------------------ sortie
n_, pts, OUTER = G.n_, G.pts, G.OUTER
ramp, bev = G.ROCK_DEEP, G.BEVEL_HARD

def build(title, dose_plans, force_paillettes, seed=81177, resine=None):
    def op(v): return f"{min(0.85, v * dose_plans):.3f}".rstrip("0").rstrip(".")
    L = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"',
         '     role="img" aria-label="Kyanite">',
         f'  <title>Kyanite — {title}</title>', '',
         '  <defs>',
         f'    <clipPath id="bloc"><polygon points="{pts(OUTER)}"/></clipPath>',
         f'    <clipPath id="jambage"><polygon points="{pts(G.BAND_STEM)}"/></clipPath>',
         f'    <clipPath id="haute"><polygon points="{pts(G.BAND_ARM)}"/></clipPath>',
         f'    <clipPath id="basse"><polygon points="{pts(G.BAND_LEG)}"/></clipPath>',
         '  </defs>', '',
         '  <g clip-path="url(#bloc)">',
         f'    <polygon points="{pts(OUTER)}" fill="{ramp[4]}"/>', '']
    paquets = (
        ("jambage", "jambage",
         G.blades_stem(ramp, seed + 1) + G.fines_stem(26, ramp, seed + 11)),
        ("haute", "branche haute",
         G.blades_axis(G.ARM_A, G.ARM_D, G.ARM_S, G.ARM_V, ramp, seed + 2)
         + G.fines_axis(G.ARM_Y0 - 4, G.ARM_Y1, G.ARM_S, 24, ramp, seed + 12)),
        ("basse", "branche basse",
         G.blades_axis(G.LEG_A, G.LEG_D, G.LEG_S, G.LEG_V, ramp, seed + 3)
         + G.fines_axis(G.LEG_Y0, G.LEG_Y1 + 4, G.LEG_S, 22, ramp, seed + 13)),
    )
    for cid, nom, bl in paquets:
        L.append(f'    <!-- {nom} : lames de kyanite, grandes puis fines -->')
        L.append(f'    <g clip-path="url(#{cid})">')
        for poly, c in bl:
            L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
        L.append('    </g>')
    L += ['', '    <!-- grain : plages, grains, eclats de quartz, points de mica -->', '    <g>']
    for poly, c in G.granite(seed, ramp):
        L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
    L.append('    </g>')
    L += ['', '    <!-- fractures en travers du clivage -->']
    for ps, w, clair in G.fractures(seed + 5):
        for poly, c in G.fracture(ps, w, clair):
            L.append(f'    <polygon points="{pts(poly)}" fill="{c}"/>')
    L += ['', '    <!-- plans de clivage traversants : l\'epaisseur du cristal -->', '    <g>']
    rp = random.Random(seed + 31)
    tri, tc, to = COIN
    L.append(f'      <polygon points="{pts(tri)}" fill="{tc}" fill-opacity="{op(to)}"/>')
    for d, o, w, c, a in PLANS:
        L.append(f'      <polygon points="{pts(plan(d, o, w, rp))}" fill="{c}" fill-opacity="{op(a)}"/>')
    L.append('    </g>')
    if resine is None:
        morceaux, traces = G.fente(seed + 23)
        L += ['', "    <!-- la fente : creux a l'ombre, fond inegal, paroi aval",
              "         eclairee par plages, filet intermittent sur la levre amont,",
              "         eclats manquants, fissures secondaires -->", '    <g>']
        for poly, c in morceaux:
            L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
    else:
        morceaux, traces = G.resine(seed + 23, resine)
        L += ['', "    <!-- la fente comblee : levre de pierre dessous, resine",
              "         translucide, menisque continu sur la levre amont,",
              "         bulles prises dans la masse -->", '    <g>']
        for poly, c, a in morceaux:
            o = f"{a:.2f}".rstrip("0").rstrip(".")
            L.append(f'      <polygon points="{pts(poly)}" fill="{c}" fill-opacity="{o}"/>')
    L.append('    </g>')
    L += ['', '    <!-- paillettes : les eclats pris dans la crevasse -->', '    <g>']
    for poly, c in paillettes(seed + 7, force_paillettes, traces):
        L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
    L.append('    </g>')
    L += ['', '    <!-- deux plans passes par-dessus tout : la lumiere qui traverse -->']
    for d, o, w, c, a in PLANS_DESSUS:
        L.append(f'    <polygon points="{pts(plan(d, o, w, rp))}" fill="{c}" fill-opacity="{op(a)}"/>')
    L += ['', "    <!-- biseau : une arete vive etroite, puis le pan principal.",
          '         Un pan par arete, une seule lumiere haut-gauche. -->']
    arete = G.inset(OUTER, 0.8)
    # l'arete vive s'ecarte du pan : plus sombre a l'ombre, plus vive au jour
    vif = [bev[0], bev[0], bev[1], bev[4], bev[4]]
    for poly, c in G.bevel_ring(OUTER, arete, vif):
        L.append(f'    <polygon points="{pts(poly)}" fill="{c}"/>')
    for poly, c in G.bevel_ring(arete, G.inset(arete, G.BEVEL_W - 0.8), bev):
        L.append(f'    <polygon points="{pts(poly)}" fill="{c}"/>')
    L += ['  </g>', '</svg>']
    return "\n".join(L) + "\n"

# Deux molettes : l'opacite des plans traversants, la taille des paillettes.
VARIANTS = [
    ("kyanite-logo", "K", 1.55, 1.30, None),
]
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for slug, title, dp, fp, res in VARIANTS:
        p = os.path.join(OUT, slug + ".svg")
        open(p, "w").write(build(title, dp, fp, resine=res))
        print(f"ecrit {slug}  {os.path.getsize(p)//1024} Ko")
