# The tools that write the `logo/` directory

The drawing is **asymmetrical and irregular by construction**: granite
grain, broken cleavage planes, lamellae, fractures, a seam that wanders.
All of it comes out of a fixed-seed generator — so perfectly
reproducible — but would be unbearable to maintain by hand.

The SVGs the scripts write stay commented, polygons only, and can be
edited by hand without trouble. svgo strips the comments on the way to
`logo/`, so the delivered files carry none — run a generator on its own
to get the commented version.

```sh
sh build.sh        # rebuilds the six SVGs and the twenty PNGs
```

| file | role |
|---|---|
| `block.py` | The geometry: outline, corner cuts, bevel, kyanite blades, grain, fractures, seam. Also both palettes and the two themes. Checks numerically that no bevel facet flips over, and that the keen edge clears 3:1 against its own ground. |
| `draw.py` | The full logo: translucent planes, spangles, double bevel, writing the SVG. |
| `icon.py` | The simplified version for small sizes. |
| `logotype.py` | The symbol followed by the word, Inter SemiBold converted to outlines (fontTools). |
| `export.py` | The PNGs, through headless Chromium. |
| `optimize.py` | PNG compression: pngquant then oxipng, with the deviation measured. |
| `svgo.config.mjs` | Optimisation settings. Keeps the identifiers, which the clipping masks depend on. |

## The two grounds

The geometry is shared; only the values change. A theme is a plain dict
at the bottom of `block.py` — `ON_DARK` and `ON_LIGHT` — and a third
ground would be a third dict, not a change to any drawing code.
`check_ground()` says straight away if its keen edge is too pale to hold
the contour; [`../NOTES.md`](../NOTES.md#the-two-grounds) says why that
is the value that matters.

## The two knobs

At the bottom of `draw.py`: the opacity of the planes passing through and
the size of the spangles. The shipped setting is `1.55` / `1.30`, and it
serves both grounds.

## PNG optimisation

`optimize.py` reproduces the squoosh.app chain: **pngquant** to cut the
palette down, then **oxipng** with zopfli to recompress losslessly. It
tries both routes — lossless alone, and palette then lossless — and keeps
the smaller as long as the deviation stays under the limit. That
deviation is measured on **premultiplied** channels: on an image with a
transparent background, comparing the raw RGB of an invisible pixel means
nothing.

On the delivered set: 591 kB → 206 kB, −65%, for a root mean square
deviation of at most 1.07 out of 255.

## Dependencies

`python3`, `pillow`, `fonttools` (logotype), `pyoxipng`, `pngquant`,
`svgo`, and a headless Chromium (PNGs). Chromium's path is at the top of
`export.py`.
