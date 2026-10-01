---
title: A small marker is read as pointing along its sharpest corner, so a deeply notched arrowhead points backwards
tags: [graphics, ui, maps, perception]
added: 2026-10-01
---

## Fact

At map and HUD sizes the eye has only corners to go on, and it reads a pointer
as pointing along its most acute one. A notched arrowhead has three acute
corners, the tip and the two wings. Once the wings are sharper than the tip, it
reads as a chevron flying tail-first.

With the tip at `(L, 0)`, the wings at `(-a, ±w)` and the notch at `(-n, 0)`:

```
tip  = 2 * atan(w / (L + a))
wing = atan(w / (a - n)) - atan(w / (L + a))
```

`L = 1.25, a = 0.85, w = 0.95, n = 0.35` looks like an ordinary arrow when
drawn large, but its tip is 48.7° and each wing 37.9°.

## Why it matters

Nothing is wrong with the geometry or the rotation: a pixel probe ahead of the
marker finds its tip exactly where it should be. The fault only shows as a
person, often its author, reading the direction backwards at a glance, so it
gets past the tests that check the maths.

## How to apply

- Make the tip the single sharpest corner by a clear margin: keep the notch
  shallow or drop it. An unnotched isosceles triangle's base angles are each
  `(180° - tip) / 2`, so its tip must stay under 60°.
- A teardrop has one corner and cannot be misread. A tip two radii out leaves
  the circle at ±60°: `moveTo(2 * r, 0); arc(0, 0, r, Math.PI / 3, -Math.PI / 3); closePath();`
- Judge the marker rendered at its real size and at an off-axis angle, not as a
  large mock-up.
