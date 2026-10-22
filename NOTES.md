# Design journal for the logo

This file keeps the reasons behind the drawing. To use it, see
[`logo/README.md`](logo/README.md); to rebuild it, see
[`tools/README.md`](tools/README.md).

## The drawing

A K **cut from a block**, not drawn with a pen. A single outline,
chisel-cut corners, a bevel of constant width all the way round. Each
facet of the bevel takes its value from the orientation of its edge
under **a single light coming from the top left**. No perspective.

### Asymmetry

- The two obliques share neither slope (4/7 and 5/8), nor length, nor
  thickness, nor the abscissa of their blade edge.
- **The joints are short.** The fork is dropped to mid-height minus two,
  and the lower arm meets the stem over only 23 units: the lower
  counter-punch is 19 units tall against 11 before. Without that, the
  lower arm and the stem read as a single mass.
- Thicknesses: stem 30, upper arm 22.6, lower arm 21.2. The bevel is at
  3, to let the notches breathe.
- **The top and the foot of the stem are not of the same nature**: at the
  top a single clean oblique cut, made in one stroke; at the bottom a
  clean right angle on the left — no cut at all, the flank stays plumb to
  the ground — and on the right a step, the corner left hanging like a
  detached block.
- The corners take two cuts of different lengths.
- The long edges carry jogs.

## The material

Read as granite, at three scales: the kyanite blades (broad structure and
light), then patches the size of a crystal, then the fine grain — pale
quartz flecks, dark mica specks. The density of the grain is not uniform:
six nests make it vary.

Over the top, **fractures** broken across the cleavage.

## The two additions of that round

**The crack is filled.** This was the last substantive change, and the
most important.

An open crack in the logo of a system that sells itself as immutable and
hardened says the opposite of what we want: it reads as damage. A
**filled** crack says the reverse — sealed, consolidated. In mineralogy
it is a secondary vein sealing a fracture; elsewhere it is kintsugi. Same
mineral language, message turned around.

What makes it read "filled" rather than "broken" is not the colour, it is
**continuity**:

- a **meniscus** — the resin climbing against the wall — running
  unbroken along the near lip. A break edge, by contrast, gives a choppy
  highlight. It has to stay a thread: wide, it bleeds at small sizes;
- clean edges, and **no missing chips**: the chipping of the open version
  is removed;
- a dark stone edging underneath, which sets the vein *in* the stone
  instead of leaving it floating on top;
- the material is translucent, so the grain shows through —
  `fill-opacity`, not a flat fill;
- the secondary cracks are sealed too: it is the whole network that is
  closed.

The path keeps its irregularities — it wanders, it pinches and swells,
the two lips drift independently — but less than the open break: the
resin follows the fracture, its own surface is smooth.

The noise driving all of this is **smoothed**. Noise uncorrelated from
one point to the next would give saw teeth; a fracture drifts slowly.

Two doses live in `tools/block.py` — `RESIN_MILKY`, the one shipped, and
`RESIN_MINERAL`, more discreet and more stone-like.

**Spangles.** They become **bubbles caught in the resin**: small angular
shards and diamonds, pale and dark. No star shapes.

**Translucent planes.** Kyanite is transparent. Fifteen broad planes at
low opacity cross along three cleavage directions that match none of the
visible faces; where they overlap, the value builds up. Two planes pass
over everything, like light travelling through the mass.

The opacity is the SVG attribute `fill-opacity`, **not a filter**: the
rendering stays identical everywhere, system icons included.

## Fineness: four scales that overlap

So that the underlying shapes stop reading, none of the four has a
straight contour:

1. **The blades** of kyanite, broken into six segments with a
   perpendicular drift at each node. Two neighbouring blades share
   exactly the same break: they tile the band with no gap.
2. **The lamellae**, fine striations caught between the big blades. They
   run the full length of the band — the whole height of the stem, the
   whole width of each arm — each one wandering a couple of units
   sideways over that span and broken into five or six segments, so that
   none of them is a straight line. Kyanite grows in long blades; striations
   that follow the same habit read as the grain of the mineral, where
   shorter marks would read as scattering.
3. **The granite grain**, at three sizes, with uneven density.
4. **The dry fractures**, across the cleavage, all of different length,
   width and contrast. One in three does not catch the light. These stay
   open: they are surface micro-cracks, not the fracture that runs
   through.

An earlier pair of `fines_axis` and `fines_stem` drew the lamellae as
short shards instead, and this journal described them that way for a
while. Those two functions sat in `block.py` alongside their
replacements, shadowed by them, so the shards had never actually
rendered — the drawing has always had the crossing version. Put side by
side the two differ across about a third of the pixels but by an average
of 2.3 out of 255: broad and shallow, texture rather than structure. The
crossing version is kept, and the dead copy is gone.

The bevel is double: a narrow keen edge (0.8) that parts from its facet —
darker in shadow, keener in daylight — then the main facet.

Setting shipped: `K3 — deep mine`, translucent planes at 1.55 and
spangles at 1.30. Both knobs are at the bottom of `tools/draw.py`.

## The two grounds

The drawing was cut for a dark background, and does not survive on a
light one — not for a reason that tuning can fix.

The keenest facet, the one that draws the contour, blows out to
near-white (`#DBEBFF`). Against `#0F1522` that is 15.07:1; against
`#FFFFFF` it is **1.21:1**. Measured on the rendered pixels, about 40% of
the contour falls below 3:1 on white, and the shape opens up at the top
left.

The fix is neither to move the light nor to recolour, but to move the
whole value scale. On a dark ground the block is a lit mass in a
near-black room, so its brightest facet can exceed everything around it.
On a light ground white is the brightest thing in the frame, so the stone
has to sit **below** the page instead of above it: deep navy in shadow,
mid blue in the light.

What is preserved is not the values but the **intervals** between them.
The ratios that carry the chiselled read land within a few hundredths of
the dark palette's:

| | dark | light |
|---|---|---|
| stem against upper arm | 1.94 | 2.18 |
| upper arm against lower arm | 1.48 | 1.45 |
| lit face against its own shadow | 1.80 | 1.82 |

The light comes from the same place; it is the room that changed.

The asymmetry explains why there have to be two files and not one clever
one. On a dark ground the contour is held by the **bright** keen edge,
and the deepest facet is *meant* to melt into the background. On a light
ground the contour is held by the **mass**, 18.6:1 at its deepest, and
the keen edge is merely the palest part of the stone at 3.47:1 — lighter
than the stone, never lighter than the page. On Breeze Light (`#EFF0F1`),
which is where most of this will actually be seen, it still holds at
3.04:1.

`block.py` checks this numerically on every build, the same way it checks
that no bevel facet flips over: the keen edge must clear 3:1 against its
own ground. That assertion is exactly what the dark palette fails on
white, which is how the gap was found rather than guessed at.

## Palette

Both grounds in full in [`logo/README.md`](logo/README.md#palette).

## Constraints held

Polygons only. No filter, no bitmap, no gradient. The clipping masks are
polygons.

The generator checks numerically that no bevel facet flips over: on an
edge shorter than the bevel, the two neighbouring facets would close in
on each other and make a tooth. They are folded to a point instead.

The drawing deliberately resembles neither Fedora's "f" nor KDE's gear,
which are registered trademarks.

## The icon version

Below 128 px the grain, the spangles and the planes are nothing but
noise. `kyanite-icon.svg` drops them, strips the jogs from the outline,
and takes the bevel from 3 to 5.

**What survives, measured rather than assumed:**

| | 16 px | 22–32 px | 48–128 px |
|---|---|---|---|
| silhouette | yes | yes | yes |
| contrast between the three strokes | yes | yes | yes |
| lit edge at the top left | yes, dominant | yes | yes |
| the seam | **does not read** | muted line | yes |

That last row used to say plainly **no**, and "measured rather than
assumed" had not been applied to it. It is wrong: the seam is not absent
at 16 px. Render the icon twice, with and without the `seam` group, and
compare pixel by pixel:

| | 16 px | 22 px | 24 px | 32 px | 48 px |
|---|---|---|---|---|---|
| pixels touched | 26 / 256 | 43 / 484 | 48 / 576 | 74 / 1024 | 141 / 2304 |
| | 10.2% | 8.9% | 8.3% | 7.2% | 6.1% |
| largest difference | 47 / 255 | 74 | 79 | 94 | 127 |

The light icon measures the same to within one pixel.

So the seam is drawn at 16 px, and it costs almost nothing to draw.
What it does not do there is *read* as a vein: all the eye is left with
is the silhouette, the contrast between the strokes, and a pale edge
pulling towards the top-left corner. That is the order in which the icon
has to be thought about — and the distinction matters when tuning it.
There is nothing to reclaim by cutting the seam at that size; there is
only no point counting on it.
