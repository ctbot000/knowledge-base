---
title: A level-of-detail ring selected by cell centre must overlap its neighbour by more than one cell
tags: [graphics, terrain, level-of-detail]
added: 2026-09-19
---

## Fact

Concentric level-of-detail rings are usually built by generating each level's
grid and keeping the cells whose **centre** falls between an inner and an outer
radius. A centre inside the boundary keeps a cell whose far half sticks out past
it, and a centre outside drops a cell whose near half should have been drawn.
The uncovered band is therefore up to half a cell wide on each side — and the
coarse level's cell is the large one.

So the overlap between two rings has to be measured in the *coarser* level's
cells, not as a percentage of the radius. A 6% overlap at a 3600 m boundary is
216 m, while the ring outside it has 1100 m cells: guaranteed gaps. Start each
ring at `previousRadius - cell * 1.2` and the wedges close.

## Why it matters

What shows through the gap is the background, and a sky or haze colour drawn in
a thin sliver below the horizon does not read as a hole. It reads as water, as
a cloud shadow, or as a lit field, so the bug is investigated as a colour or
sorting problem in the terrain rather than as missing geometry.

The gaps also move with the camera, because each level snaps its grid to a
different multiple, which makes them look like flicker rather than absence.

## How to apply

- Derive the inner radius from the cell size: `inner = prevRadius - cell * 1.2`.
- Let the rings overlap and settle the tie deliberately — push the coarse ring
  back in the depth sort so the finer quads always paint last.
- Test it without rendering: sweep the radius and assert that some level's
  `[inner, outer]` band, widened by its own cell size, contains every value.
