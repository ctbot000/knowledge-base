---
title: The camera pitch that fits a ground plane to a frame is asin(footprintAspect / canvasAspect)
tags: [3d, camera, layout, game-design]
added: 2026-09-14
---

## Fact

A flat board of width `W` and depth `D` viewed at pitch `p` above the horizon
projects to `W` by `D·sin(p)`, so its projected aspect is

```
projected = (W / D) / sin(p)
```

Setting that equal to the canvas aspect `A` and solving gives the pitch that
fits the board to the frame with nothing left over:

```
sin(p) = (W / D) / A        p = asin(clamp((W / D) / A, lo, hi))
```

A 20x13 board in a 2:1 canvas wants `p = 50°`; in a 1.7:1 canvas, `65°`. The
clamp is what keeps it usable: an `A` near the board's own aspect drives the
solution to 90° — straight down, with the perspective thrown away — and a very
wide `A` skims the camera along the ground.

## Why it matters

Pitch is otherwise picked by eye on one window size and then quietly wrong
everywhere else, because the mismatch does not look like a camera bug. It
looks like wasted space, which invites tuning the canvas, the field of view,
or the zoom — three knobs that cannot fix an angle.

The same relation also says which canvas shape to *choose*: measured against
a 20x13 board, going from a canvas at the board's own 1.54 aspect to one at
2.0 raised the fraction of frame height the board covered from 0.65 to 0.81.
Sizing a 3D viewport to the subject's 2D footprint is the reflex to avoid —
the projection is always wider than the footprint.

## How to apply

- Derive the pitch per layout from the measured canvas aspect; never store it
  as a constant.
- Clamp it to an angle range that still reads as a 3D view, roughly
  `sin(p) ∈ [0.6, 0.97]`, and treat the clamp as the design decision.
- Shape the canvas to the *projected* aspect, not to the subject's footprint.
- Solve the distance separately, per corner of the bounding box.
- A pitch the viewer has since changed by dragging must not be overwritten on
  the next resize; keep a flag for it.

Related: [[framing-a-box-is-a-per-corner-solve]], [[auto-framing-collapses-to-face-on]].
