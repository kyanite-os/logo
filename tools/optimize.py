#!/usr/bin/env python3
"""PNG optimisation: exactly the squoosh.app chain.

Two engines, the same two the online tool uses:

  pngquant (libimagequant)  cuts the palette down. It is the only large
                            gain: these images have few distinct colours
                            for their area.
  oxipng                    recompresses losslessly, with zopfli.

For each file we try both routes — lossless alone, and palette then
lossless — measure the deviation from the original, and keep the
smaller of the two as long as the deviation stays under the limit.

The deviation is measured on premultiplied channels: on an image with a
transparent background, comparing the raw RGB of an invisible pixel
means nothing.
"""
import os, re, subprocess, sys, tempfile
import oxipng
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(HERE, "..", "logo", "png")

PALETTE_MAX = 256
QUALITY = "88-100"     # pngquant refuses to go below 88
RMSE_LIMIT = 1.1       # root-mean-square deviation tolerated, out of 255

def deviation(a, b):
    """Root-mean-square deviation between two images, premultiplied."""
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

def lossless(src, dest):
    oxipng.optimize(src, dest, level=6, interlace=oxipng.Interlacing.Off,
                    deflate=oxipng.Deflaters.zopfli(15),
                    strip=oxipng.StripChunks.safe(), optimize_alpha=True)

def palette(src, dest):
    r = subprocess.run(["pngquant", "--force", "--speed", "1",
                        "--quality", QUALITY, "--strip",
                        str(PALETTE_MAX), "--output", dest, "--", src],
                       capture_output=True)
    return r.returncode == 0 and os.path.exists(dest)

def process(path):
    before = os.path.getsize(path)
    with tempfile.TemporaryDirectory() as tmp:
        a = os.path.join(tmp, "a.png")
        lossless(path, a)
        best, route, rmse = a, "lossless", 0.0

        b0, b1 = os.path.join(tmp, "b0.png"), os.path.join(tmp, "b1.png")
        if palette(path, b0):
            lossless(b0, b1)
            e = deviation(path, b1)
            if e <= RMSE_LIMIT and os.path.getsize(b1) < os.path.getsize(a):
                best, route, rmse = b1, f"palette {PALETTE_MAX}", e
        after = os.path.getsize(best)
        if after < before:
            os.replace(best, path)
        else:
            route, after = "unchanged", before
    return before, after, route, rmse

if __name__ == "__main__":
    def order(f):
        """Dark set by size, then its banner, then the light set."""
        m = re.search(r"-(\d+)", f)
        return ("-light" in f, 0 if m else 1, int(m.group(1)) if m else 0, f)
    files = sorted((f for f in os.listdir(PNG) if f.endswith(".png")), key=order)
    ta = tb = 0
    print(f"{'file':<22}{'before':>9}{'after':>9}{'saved':>7}   route")
    for f in files:
        a, b, route, e = process(os.path.join(PNG, f))
        ta += a; tb += b
        note = f"{route}" + (f", deviation {e:.2f}/255" if e else "")
        print(f"{f:<22}{a:>9}{b:>9}{100 - b * 100 // a:>6}%   {note}")
    print(f"{'TOTAL':<22}{ta:>9}{tb:>9}{100 - tb * 100 // ta:>6}%")
