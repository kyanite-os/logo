# The Kyanite logo

A K cut from a block of kyanite, crossed by a vein of resin that seals its
fracture.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="png/banner.png">
  <source media="(prefers-color-scheme: light)" srcset="png/banner-light.png">
  <img alt="The Kyanite logotype" src="png/banner.png">
</picture>

## The files

No suffix means **dark** background; `-light` means **light**. Same geometry,
same light from the top left — only the values differ.

| file | what for |
|---|---|
| `kyanite-logo[-light].svg` | The full drawing, for **64 px and up**. |
| `kyanite-icon[-light].svg` | Simplified, for **under 64 px**: system icon, favicon, taskbar. |
| `kyanite-logotype[-light].svg` | The symbol followed by the word. |
| `png/kyanite-<size>[-light].png` | 16, 22, 24, 32, 48, 64, 128, 256, 512 px, transparent. |
| `png/banner[-light].png` | The logotype **with its background**, for a page whose theme you do not control. |

PNGs under 128 px come from the icon, the rest from the full logo. Already
optimised — no need to run them through a compressor again.

Rebuild: `sh ../tools/build.sh`.

## Which ground

Get this one right; the rest is taste. **Dark files on a dark background**
(`#0A0E18` to `#1E2534`, reference `#0F1522`). **Light files on a light one**
(`#FFFFFF` down to about `#E6E9ED`, reference `#FFFFFF`).

It is not a preference. The drawing is lit from the top left, and on a dark
ground its keenest facet blows out to near-white — which against white is
1.21:1, invisible. Put the dark files on a white page and about 40% of the
contour drops below 3:1: the top-left edges dissolve and the shape opens up.
The light palette puts none of its contour below 3:1. Reasoning and
measurements in [`NOTES.md`](../NOTES.md#the-two-grounds).

If you cannot know the background, use a banner, which carries its own — or
serve both and let the reader's theme choose:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="png/banner.png">
  <source media="(prefers-color-scheme: light)" srcset="png/banner-light.png">
  <img alt="Kyanite" src="png/banner.png">
</picture>
```

## Palette

| series | dark ground | light ground |
|---|---|---|
| background | `#0F1522` | `#FFFFFF` |
| the rock, 9 values | `#15306A` `#1B3B7C` `#21468E` `#2851A0` `#2E5CB1` `#3668C1` `#3F75CE` `#4A83DA` `#5793E4` | `#0B1C40` `#0F244E` `#132C5C` `#17356A` `#1C3E79` `#214887` `#285496` `#2F60A5` `#3A6DBE` |
| the bevel, 5 values | `#112A58` `#1C4184` `#3A74C8` `#86B7F2` `#DBEBFF` | `#07122A` `#0F2350` `#23508F` `#3A74C8` `#4E8BDC` |
| the filled seam | stone lip `#12305F` · resin `#9CC6F4` · core `#7FB3EE` · meniscus `#F2F8FF` · sheen `#C6DFFA` | stone lip `#091B3C` · resin `#7FAEE4` · core `#5E90D4` · meniscus `#DCE9FA` · sheen `#9CC0EC` |
| bubbles in the resin | `#F7FBFF` `#285AA6` | `#EAF2FD` `#16305E` |
| spangles | `#C6DEFA` `#A8CCF4` `#88B8F0` `#6AA0E8` `#4D86DA` | `#A8C8F0` `#8BB0E6` `#6E98DC` `#5480CE` `#3F6CC0` |
| quartz · mica | `#86B6EE` `#A8CCF4` · `#1C3C76` `#22477F` | `#5E90D8` `#7BA8E4` · `#0A1835` `#0E1E42` |
| fractures | `#1E4588` `#6CA2E8` | `#0D2048` `#3E72C4` |
| planes passing through | `#BBD8F8` · `#0C2149` | `#A9C8EC` · `#06102A` |
| the word, in the logotype | `#DCE6F2` | `#16253D` |

The icon flattens its tints — at 16 px, stacked opacities only give mush:

| role | dark ground | light ground |
|---|---|---|
| stem, lit · shadow | `#3A74CA` · `#234C92` | `#255494` · `#122C57` |
| upper arm, lit · shadow | `#74ABEE` · `#4280D6` | `#4E8BDC` · `#2A5FA8` |
| lower arm, lit · shadow | `#4D8ADA` · `#2E60B4` | `#336FC0` · `#1C4480` |
| seam: stone lip · body · meniscus | `#163A74` · `#7CA6E0` · `#EAF4FF` | `#0E2448` · `#5E8ECE` · `#CFE2F8` |

## Using it

Leave **a quarter of its height** clear around the symbol, free of text, rules
and edges; the 10% internal margin in the SVGs does not count towards it.
Minimum 16 px for the icon, 120 px wide for the logotype — below that the word
goes illegible well before the symbol does.

Do not: put a variant on the wrong ground · recolour it (the values are
computed from each facet's orientation) · rotate or mirror it (the light would
come from elsewhere) · stretch it · add a shadow, glow, outline or relief (the
relief is in the drawing) · crop it into a circle or rounded square (the foot
and blade edges would be cut) · use the symbol as a letter in a word · redraw
the word in another typeface.

Need a ground that is not here? Ask rather than improvise — the two palettes
were built by moving the whole value scale, not by tinting.

The files use **polygons only**, plus `clipPath` and `fill-opacity`: no
filter, bitmap or gradient, so they survive icon themes and automatic
conversions. The word is Inter SemiBold converted to outlines, so no font is
needed to display it.

## Name and logo

The code is free software; the name and this logo are not. You may reproduce
them to talk about Kyanite, not to name or sign anything else. Terms in
[`LICENSE`](../LICENSE).
