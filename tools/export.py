#!/usr/bin/env python3
"""Les exports PNG, a fond transparent.

En dessous de 128 px on exporte depuis kyanite-icon.svg, au-dessus
depuis kyanite-logo.svg : le dessin complet se brouille en petit, et
l'icone est trop nue en grand.

La bascule est a 128 et pas plus bas. A 64 et 96 px, le grain et les
paillettes du dessin complet ne font plus que du bruit et la fente
bave : le rendu y est moins lisible que celui de l'icone a 48 px.
Verifie au rendu, pas suppose.

On exporte aussi une banniere, fond sombre inclus. Les PNG a fond
transparent sont illisibles sur fond clair — or un README GitHub
s'affiche en theme clair pour une bonne part des visiteurs.

Le rendu passe par Chromium sans interface, qui est le moteur SVG de
reference pour ce qui s'affichera dans un navigateur ou dans Plasma.
"""
import os, re, subprocess, sys

ICI = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(ICI, "..", "logo")
PNG = os.path.join(LOGO, "png")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
TAILLES = [16, 22, 24, 32, 48, 64, 128, 256, 512]
BASCULE = 128

def rend(src, taille, dest):
    svg = open(src).read().replace('width="100" height="100"', '')
    page = os.path.join(PNG, ".page.html")
    open(page, "w").write(
        "<!doctype html><meta charset='utf-8'><style>*{margin:0;padding:0}"
        f"html,body{{background:transparent}}svg{{display:block;width:{taille}px;height:{taille}px}}"
        "</style>" + svg)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--default-background-color=00000000", f"--screenshot={dest}",
                    f"--window-size={taille},{taille}", "--virtual-time-budget=5000",
                    "file://" + page], capture_output=True)
    os.remove(page)
    if not os.path.exists(dest):
        sys.exit(f"echec du rendu : {dest}")

def banniere(dest, largeur=1200, hauteur=340, fond="#0F1522"):
    """Le logotype, fond sombre compris : utilisable dans un README,
    quel que soit le theme du lecteur."""
    svg = open(os.path.join(LOGO, "kyanite-logotype.svg")).read()
    svg = re.sub(r'\s(width|height)="[\d.]+"', "", svg, count=2)
    page = os.path.join(PNG, ".page.html")
    open(page, "w").write(
        "<!doctype html><meta charset='utf-8'><style>*{margin:0;padding:0}"
        f"html,body{{background:{fond};height:100%}}"
        "body{display:flex;align-items:center;justify-content:center}"
        f".k{{width:{int(largeur * 0.62)}px}}svg{{display:block;width:100%;height:auto}}"
        "</style>" + f"<div class='k'>{svg}</div>")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    f"--screenshot={dest}", f"--window-size={largeur},{hauteur}",
                    "--virtual-time-budget=5000", "file://" + page], capture_output=True)
    os.remove(page)
    if not os.path.exists(dest):
        sys.exit(f"echec du rendu : {dest}")

if __name__ == "__main__":
    os.makedirs(PNG, exist_ok=True)
    for t in TAILLES:
        src = os.path.join(LOGO, "kyanite-icon.svg" if t < BASCULE else "kyanite-logo.svg")
        dest = os.path.join(PNG, f"kyanite-{t}.png")
        rend(src, t, dest)
        print(f"{os.path.basename(dest):<20} {os.path.getsize(dest):>7} o   "
              f"depuis {os.path.basename(src)}")
    d = os.path.join(PNG, "banniere.png")
    banniere(d)
    print(f"{'banniere.png':<20} {os.path.getsize(d):>7} o   depuis kyanite-logotype.svg")
