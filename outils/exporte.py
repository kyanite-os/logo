#!/usr/bin/env python3
"""Les exports PNG, a fond transparent.

En dessous de 64 px on exporte depuis kyanite-icon.svg, au-dessus
depuis kyanite-logo.svg : le dessin complet se brouille en petit, et
l'icone est trop nue en grand. La bascule est a 64.

Le rendu passe par Chromium sans interface, qui est le moteur SVG de
reference pour ce qui s'affichera dans un navigateur ou dans Plasma.
"""
import os, subprocess, sys

ICI = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(ICI, "..", "logo")
PNG = os.path.join(LOGO, "png")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
TAILLES = [16, 22, 24, 32, 48, 64, 128, 256, 512]
BASCULE = 64

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

if __name__ == "__main__":
    os.makedirs(PNG, exist_ok=True)
    for t in TAILLES:
        src = os.path.join(LOGO, "kyanite-icon.svg" if t < BASCULE else "kyanite-logo.svg")
        dest = os.path.join(PNG, f"kyanite-{t}.png")
        rend(src, t, dest)
        print(f"{os.path.basename(dest):<20} {os.path.getsize(dest):>7} o   "
              f"depuis {os.path.basename(src)}")
