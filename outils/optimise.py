#!/usr/bin/env python3
"""Optimisation des PNG : exactement la chaine de squoosh.app.

Deux moteurs, les memes que l'outil en ligne :

  pngquant (libimagequant)  reduit la palette. C'est le seul gain
                            important : ces images ont peu de couleurs
                            distinctes pour leur surface.
  oxipng                    recompresse sans perte, avec zopfli.

Pour chaque fichier on essaie les deux chemins — sans perte seul, et
palette puis sans perte — on mesure l'ecart avec l'original, et on
garde le plus petit des deux tant que l'ecart reste sous le seuil.

L'ecart est mesure sur les canaux premultiplies : sur une image a fond
transparent, comparer les RGB bruts d'un pixel invisible n'a aucun sens.
"""
import os, subprocess, sys, tempfile
import oxipng
from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(ICI, "..", "logo", "png")

PALETTE_MAX = 256
QUALITE = "88-100"     # pngquant refuse de descendre sous 88
SEUIL_EQM = 1.1        # ecart quadratique moyen tolere, sur 255

def ecart(a, b):
    """Ecart quadratique moyen entre deux images, canaux premultiplies."""
    ia, ib = Image.open(a).convert("RGBA"), Image.open(b).convert("RGBA")
    if ia.size != ib.size:
        return 1e9
    pa, pb = ia.load(), ib.load()
    s, n = 0, 0
    for y in range(ia.height):
        for x in range(ia.width):
            ra, ga, ba, aa = pa[x, y]
            rb, gb, bb, ab = pb[x, y]
            for u, v in ((ra * aa, rb * ab), (ga * aa, gb * ab),
                         (ba * aa, bb * ab), (aa * 255, ab * 255)):
                d = (u - v) / 255.0
                s += d * d
                n += 1
    return (s / n) ** 0.5

def sans_perte(src, dest):
    oxipng.optimize(src, dest, level=6, interlace=oxipng.Interlacing.Off,
                    deflate=oxipng.Deflaters.zopfli(15),
                    strip=oxipng.StripChunks.safe(), optimize_alpha=True)

def palette(src, dest):
    r = subprocess.run(["pngquant", "--force", "--speed", "1",
                        "--quality", QUALITE, "--strip",
                        str(PALETTE_MAX), "--output", dest, "--", src],
                       capture_output=True)
    return r.returncode == 0 and os.path.exists(dest)

def traite(chemin):
    avant = os.path.getsize(chemin)
    with tempfile.TemporaryDirectory() as tmp:
        a = os.path.join(tmp, "a.png")
        sans_perte(chemin, a)
        meilleur, voie, eqm = a, "sans perte", 0.0

        b0, b1 = os.path.join(tmp, "b0.png"), os.path.join(tmp, "b1.png")
        if palette(chemin, b0):
            sans_perte(b0, b1)
            e = ecart(chemin, b1)
            if e <= SEUIL_EQM and os.path.getsize(b1) < os.path.getsize(a):
                meilleur, voie, eqm = b1, f"palette {PALETTE_MAX}", e
        apres = os.path.getsize(meilleur)
        if apres < avant:
            os.replace(meilleur, chemin)
        else:
            voie, apres = "inchange", avant
    return avant, apres, voie, eqm

if __name__ == "__main__":
    def rang(f):
        tete, _, queue = f[:-4].rpartition("-")
        return (0, int(queue)) if queue.isdigit() else (1, 0)
    fichiers = sorted((f for f in os.listdir(PNG) if f.endswith(".png")), key=rang)
    ta = tb = 0
    print(f"{'fichier':<22}{'avant':>9}{'après':>9}{'gain':>7}   voie")
    for f in fichiers:
        a, b, voie, e = traite(os.path.join(PNG, f))
        ta += a; tb += b
        note = f"{voie}" + (f", écart {e:.2f}/255" if e else "")
        print(f"{f:<22}{a:>9}{b:>9}{100 - b * 100 // a:>6}%   {note}")
    print(f"{'TOTAL':<22}{ta:>9}{tb:>9}{100 - tb * 100 // ta:>6}%")
