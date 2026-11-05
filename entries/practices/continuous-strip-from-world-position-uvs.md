---
title: Tiles that must read as one continuous strip need only world-position UVs and one shared texture
tags: [graphics, 3d, textures, three.js]
added: 2026-11-05
---

## Fact

A marquee or road built from separate pieces joins up by itself when each piece's UVs
come from its world position along the strip and all pieces share one wrapped texture.
Scrolling is one `texture.offset` write. No piece needs to know its neighbours.

## Why it matters

The obvious design finds the row each piece belongs to and re-meshes it on every edit,
which reaches across chunks and has to handle gaps and rows that merge. World-position
UVs make all of that vanish: a piece placed or removed anywhere is already right, and a
gap simply skips that stretch of text.

## How to apply

- Take the coordinate along the viewer's right as they face the piece's front:
  `along = cx * rightX + cz * rightZ`, with `right = (fz, -fx)` for a front direction
  `(fx, fz)` on a grid in a Y-up, right-handed world. Getting this sign wrong mirrors the
  order of the pieces while each still looks fine close up.
- `u = (along ± 0.5) / stripLength`, with `RepeatWrapping` on S; the texture's aspect
  should match `stripLength` to one piece's height.
- Add a per-row term to `along` so rows stacked one above another do not all read alike.
- In three.js the geometry per piece is its own (dispose it with the piece); the
  material and texture stay shared, and only a piece in view needs to update them.
