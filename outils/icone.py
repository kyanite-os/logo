#!/usr/bin/env python3
"""kyanite-icon.svg — la version pour petites tailles.

Meme silhouette que le logo complet, et rien d'autre : pas de grain,
pas de lamelles, pas de fractures, pas de plans translucides, pas de
paillettes. En dessous de 64 px tout cela ne fait plus que du bruit.

Restent la silhouette, le contraste entre les trois traits, et la
fente comblee — cette derniere disparait a 16 px, elle ne revient
qu'a partir de 22. Le biseau est elargi de
3 a 5 pour qu'il pese encore un demi-pixel a 16 px.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bloc as G

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logo")

# Contour simplifie : on retire les decrochements des aretes longues,
# invisibles sous 64 px et couteux en sommets. Les coupes d'angle, le
# sommet oblique et le gradin du pied restent : c'est l'identite du mark.
CONTOUR = [
    ((G.SL, 17.0),           (7.0, 8.0)),   # coin haut-gauche
    ((G.SR, G.TOP),          (4.5, 4.0)),   # haut du jambage, coupe nette
    ((G.SR, G.ARM_Y0),       (4.0, 5.0)),   # fond de l'encoche haute
    ((G.X_ARM_TOP, G.TOP),   (6.0, 5.0)),
    ((G.ARM_X, G.TOP),       (5.0, 3.5)),   # coin haut-droit
    ((G.ARM_X, G.Y_ARM_TIP), (3.5, 6.0)),   # tranchant haut
    ((G.SR, G.FORK),         (7.0, 6.0)),   # la fourche
    ((G.LEG_X, G.Y_LEG_TIP), (5.0, 3.0)),   # tranchant bas
    ((G.LEG_X, G.BOT),       (3.0, 5.0)),   # coin bas-droit
    ((G.X_LEG_BOT, G.BOT),   (5.0, 4.0)),
    ((G.SR, G.LEG_Y1),       (4.0, 2.0)),   # fond de l'encoche basse
    ((G.SR, 85.0),           (2.0, 2.0)),   # gradin du pied
    ((26.0, 85.0),           (2.0, 2.0)),
    ((26.0, G.BOT),          (2.0, 2.5)),
    ((G.SL, G.BOT),          (0.0, 0.0)),   # coin bas-gauche : angle droit
]
BISEAU = 5.0
PIERRE = {"jambage_clair": "#3A74CA", "jambage_ombre": "#234C92",
          "haute_clair":   "#74ABEE", "haute_ombre":   "#4280D6",
          "basse_clair":   "#4D8ADA", "basse_ombre":   "#2E60B4"}
RAMPE = ["#112A58", "#1C4184", "#3A74C8", "#86B7F2", "#DBEBFF"]
# La fente est COMBLEE, comme dans le logo complet : une resine
# translucide, et surtout un menisque continu le long de la levre
# amont. C'est la continuite de ce filet, pas sa couleur, qui fait
# lire « scelle » plutot que « casse ».
# Ici les teintes sont aplaties : a 16 px, empiler des opacites ne
# donne que de la bouillie. La valeur du corps est celle que donne la
# resine du logo composee sur la pierre.
FENTE = {"levre_pierre": "#163A74", "corps": "#7CA6E0", "menisque": "#EAF4FF"}

# La fente, reduite a son trace principal : le jambage puis la branche haute.
TRACE = [(17.5, 84.0), (23.0, 69.0), (19.5, 56.0), (25.0, 43.5), (21.5, 29.0), (23.5, 14.0)]
TRACE_BRAS = [(25.0, 43.5), (40.0, 38.5), (56.0, 29.5), (70.0, 21.5), (81.0, 17.0)]
LARG = [0.0, 1.35, 1.0, 1.4, 0.95, 0.0]
LARG_BRAS = [1.4, 1.25, 1.1, 0.85, 0.0]

SPLIT_JAMBAGE = 21.5
SPLIT_HAUTE = 32.0
SPLIT_BASSE = 58.0
D = 13.0   # debord : tout est recoupe par le masque du contour

def bande_haute(a, b):
    return [(G.SR, a), (G.SR + 7 * D, a - 4 * D), (G.SR + 7 * D, b - 4 * D), (G.SR, b)]
def bande_basse(a, b):
    return [(G.SR, a), (G.SR + 8 * D, a + 5 * D), (G.SR + 8 * D, b + 5 * D), (G.SR, b)]
def bande_jambage(a, b):
    return [(a, -5), (b, -5), (b, 105), (a, 105)]

def ecris():
    n, pts = G.n_, G.pts
    ext = G.chamfer(CONTOUR)
    arete = G.inset(ext, 1.2)
    assert not G.verifie(ext, arete), "pan de biseau retourne"
    dedans = G.inset(arete, BISEAU - 1.2)
    assert not G.verifie(arete, dedans), "pan de biseau retourne"
    vif = [RAMPE[0], RAMPE[0], RAMPE[1], RAMPE[4], RAMPE[4]]

    L = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"',
         '     role="img" aria-label="Kyanite">',
         '  <title>Kyanite</title>',
         '  <desc>Un K taillé dans un bloc de kyanite. Version pour petites tailles.</desc>',
         '',
         '  <defs>',
         f'    <clipPath id="bloc"><polygon points="{pts(ext)}"/></clipPath>',
         f'    <clipPath id="jambage"><polygon points="{pts(bande_jambage(-5, G.SR))}"/></clipPath>',
         f'    <clipPath id="haute"><polygon points="{pts(bande_haute(G.ARM_Y0, G.FORK))}"/></clipPath>',
         f'    <clipPath id="basse"><polygon points="{pts(bande_basse(G.FORK, G.LEG_Y1))}"/></clipPath>',
         '  </defs>',
         '',
         '  <g clip-path="url(#bloc)">',
         f'    <polygon points="{pts(ext)}" fill="{PIERRE["jambage_ombre"]}"/>',
         '',
         "    <!-- une seule lumiere, venant du haut-gauche : la face tournee",
         '         vers elle est claire, l\'autre est dans l\'ombre -->']
    for cid, nom, parts in (
        ("jambage", "jambage", [(bande_jambage(-5, SPLIT_JAMBAGE), "jambage_clair"),
                                (bande_jambage(SPLIT_JAMBAGE, G.SR), "jambage_ombre")]),
        ("haute", "branche haute", [(bande_haute(G.ARM_Y0 - D, SPLIT_HAUTE), "haute_clair"),
                                    (bande_haute(SPLIT_HAUTE, G.FORK), "haute_ombre")]),
        ("basse", "branche basse", [(bande_basse(G.FORK, SPLIT_BASSE), "basse_clair"),
                                    (bande_basse(SPLIT_BASSE, G.LEG_Y1 + D), "basse_ombre")])):
        L.append(f'    <g id="{nom.replace(" ", "-")}" clip-path="url(#{cid})">')
        for poly, c in parts:
            L.append(f'      <polygon points="{pts(poly)}" fill="{PIERRE[c]}"/>')
        L.append('    </g>')

    L += ['', '    <!-- la fente comblee : levre de pierre, resine, menisque -->',
          '    <g id="fente">']
    for tr, lg in ((TRACE, LARG), (TRACE_BRAS, LARG_BRAS)):
        L.append(f'      <polygon points="{pts(G.ribbon(tr, [x * 1.25 for x in lg]))}"'
                 f' fill="{FENTE["levre_pierre"]}"/>')
        L.append(f'      <polygon points="{pts(G.ribbon(tr, lg))}" fill="{FENTE["corps"]}"/>')
        L.append(f'      <polygon points="{pts(G.ribbon(tr, [x * 0.26 for x in lg], -1.1))}"'
                 f' fill="{FENTE["menisque"]}"/>')
    L.append('    </g>')

    L += ['', '    <!-- biseau : une arete vive, puis le pan principal -->', '    <g id="biseau">']
    for poly, c in G.bevel_ring(ext, arete, vif):
        L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
    for poly, c in G.bevel_ring(arete, dedans, RAMPE):
        L.append(f'      <polygon points="{pts(poly)}" fill="{c}"/>')
    L += ['    </g>', '  </g>', '</svg>']
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    p = os.path.join(OUT, "kyanite-icon.svg")
    open(p, "w").write(ecris())
    print(f"ecrit {p}  {os.path.getsize(p) / 1024:.1f} Ko")
