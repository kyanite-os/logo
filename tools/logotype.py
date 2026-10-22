#!/usr/bin/env python3
"""kyanite-logotype.svg — le symbole suivi du mot.

Le mot est compose en Inter SemiBold puis **vectorise** : le fichier ne
depend d'aucune police installee. Inter est sous licence SIL OFL, qui
autorise explicitement les travaux derives.

Inter a ete choisi pour sa neutralite : une grotesque geometrique,
technique, sans caractere propre. Le symbole porte toute l'expression ;
le mot se contente de le nommer.
"""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ICI, "..", "logo")
POLICE = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"

MOT = "Kyanite"
HAUTEUR_CAP = 34.0        # hauteur de capitale : 45 % de la hauteur du symbole
INTERLETTRE = -0.4        # approche generale, legerement serree
CRENAGE = {"Ky": -2.6, "at": -0.5, "te": -0.3}   # paires a reprendre a la main
ECART = 20.0              # blanc entre le symbole et le mot
ENCRE = "#DCE6F2"

def glyphes():
    f = TTFont(POLICE)
    cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    cap = f["OS/2"].sCapHeight
    k = HAUTEUR_CAP / cap
    sortie, x = [], 0.0
    for i, ch in enumerate(MOT):
        nom = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[nom].draw(pen)
        d = pen.getCommands()
        if d:
            sortie.append((x, d))
        x += hmtx[nom][0] * k + INTERLETTRE
        if i + 1 < len(MOT):
            x += CRENAGE.get(MOT[i:i + 2], 0.0)
    return sortie, x - INTERLETTRE, k

def ecris():
    gl, largeur_mot, k = glyphes()
    # Le symbole occupe 10..88 sur 10..90 dans son propre fichier : on le
    # recadre au ras pour que le logotype n'ait pas de blanc parasite.
    x0 = 78.0 + ECART
    base = 40.0 + HAUTEUR_CAP / 2.0     # le mot cale optiquement au centre
    total = x0 + largeur_mot

    logo = open(os.path.join(OUT, "kyanite-logo.svg")).read()
    corps = logo[logo.index("<defs>"):logo.rindex("</svg>")].rstrip()

    L = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total:.1f} 80"',
         f'     width="{total:.1f}" height="80" role="img" aria-label="Kyanite">',
         '  <title>Kyanite</title>',
         '  <desc>Le symbole de Kyanite suivi du mot, en Inter SemiBold vectorisé.</desc>',
         '', '  <g id="symbole" transform="translate(-10 -10)">',
         '  ' + corps.replace("\n", "\n  "), '  </g>', '',
         '  <!-- le mot, vectorise : aucune police requise a l\'affichage -->',
         f'  <g id="mot" fill="{ENCRE}">']
    for x, d in gl:
        L.append(f'    <path transform="translate({x0 + x:.2f} {base:.1f}) '
                 f'scale({k:.5f} -{k:.5f})" d="{d}"/>')
    L += ['  </g>', '</svg>']
    return "\n".join(L) + "\n", total

if __name__ == "__main__":
    svg, w = ecris()
    p = os.path.join(OUT, "kyanite-logotype.svg")
    open(p, "w").write(svg)
    print(f"ecrit {p}  {os.path.getsize(p) / 1024:.1f} Ko  —  viewBox {w:.1f} x 80")
