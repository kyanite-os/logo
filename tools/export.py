#!/usr/bin/env python3
"""The PNG exports, on a transparent background.

Below 128 px we export from kyanite-icon.svg, above it from
kyanite-logo.svg: the full drawing muddles at small sizes, and the icon
is too bare at large ones.

The switch is at 128 and no lower. At 64 and 96 px the grain and the
spangles of the full drawing are nothing but noise and the seam bleeds:
the result there is less legible than the icon at 48 px. Checked at the
rendering, not assumed.

Everything is exported twice, once per ground: the dark set, and the
light set with a "-light" suffix. The PNGs themselves have a
transparent background, so what makes them usable on a light page is
the palette, not a baked-in backdrop.

We also export the two banners, background included. They are what a
README should use when it cannot know the reader's theme — or better,
both of them inside a <picture>, which is what this repository does.

Rendering goes through headless Chromium, which is the reference SVG
engine for anything that will be shown in a browser or in Plasma.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", "logo")
PNG = os.path.join(LOGO, "png")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
SIZES = [16, 22, 24, 32, 48, 64, 128, 256, 512]
SWITCH = 128
# (suffix, icon, full logo, logotype, banner background)
GROUNDS = [("", "kyanite-icon.svg", "kyanite-logo.svg",
            "kyanite-logotype.svg", "banner.png", "#0F1522"),
           ("-light", "kyanite-icon-light.svg", "kyanite-logo-light.svg",
            "kyanite-logotype-light.svg", "banner-light.png", "#FFFFFF")]

def render(src, size, dest):
    svg = open(src).read().replace('width="100" height="100"', '')
    page = os.path.join(PNG, ".page.html")
    open(page, "w").write(
        "<!doctype html><meta charset='utf-8'><style>*{margin:0;padding:0}"
        f"html,body{{background:transparent}}svg{{display:block;width:{size}px;height:{size}px}}"
        "</style>" + svg)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--default-background-color=00000000", f"--screenshot={dest}",
                    f"--window-size={size},{size}", "--virtual-time-budget=5000",
                    "file://" + page], capture_output=True)
    os.remove(page)
    if not os.path.exists(dest):
        sys.exit(f"rendering failed: {dest}")

def banner(dest, src="kyanite-logotype.svg", width=1200, height=340, background="#0F1522"):
    """The logotype, background included: usable in a README whatever
    theme the reader is in."""
    svg = open(os.path.join(LOGO, src)).read()
    svg = re.sub(r'\s(width|height)="[\d.]+"', "", svg, count=2)
    page = os.path.join(PNG, ".page.html")
    open(page, "w").write(
        "<!doctype html><meta charset='utf-8'><style>*{margin:0;padding:0}"
        f"html,body{{background:{background};height:100%}}"
        "body{display:flex;align-items:center;justify-content:center}"
        f".k{{width:{int(width * 0.62)}px}}svg{{display:block;width:100%;height:auto}}"
        "</style>" + f"<div class='k'>{svg}</div>")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    f"--screenshot={dest}", f"--window-size={width},{height}",
                    "--virtual-time-budget=5000", "file://" + page], capture_output=True)
    os.remove(page)
    if not os.path.exists(dest):
        sys.exit(f"rendering failed: {dest}")

if __name__ == "__main__":
    os.makedirs(PNG, exist_ok=True)
    for suffix, small, large, logotype, banner_png, background in GROUNDS:
        for t in SIZES:
            src = os.path.join(LOGO, small if t < SWITCH else large)
            dest = os.path.join(PNG, f"kyanite-{t}{suffix}.png")
            render(src, t, dest)
            print(f"{os.path.basename(dest):<22} {os.path.getsize(dest):>7} B   "
                  f"from {os.path.basename(src)}")
        d = os.path.join(PNG, banner_png)
        banner(d, logotype, background=background)
        print(f"{banner_png:<22} {os.path.getsize(d):>7} B   from {logotype}")
