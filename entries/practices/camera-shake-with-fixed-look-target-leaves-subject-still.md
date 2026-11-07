---
title: A camera shake that moves the camera but keeps its look-at target leaves the subject still on screen
tags: [3d, camera, game-design]
added: 2026-11-07
---

## Fact

Jittering a follow camera's position and then calling `lookAt(target)` rotates
the view about the target, so whatever stands at the target does not move on
screen, and things near it barely do. In a third-person game the player and what
they are hitting are exactly there. Measured at 1280×800 and a camera distance
of 8: a jitter of ±0.1 world units moved a ground point three blocks from the
target by about 2 px, and ±0.03 by about 1 px. The shake is in the code, reads
as tuned, and nobody can see it.

## Why it matters

The usual response is "hits feel weak" and more particles or a longer freeze. The
code looks right, the amounts look moderate, and raising them only shakes the
distant scenery. Spring-based kicks lose more: integrating the spring in the
same frame that applies the kick throws away about half of the peak (at 9 Hz and
60 fps) before it is ever drawn.

## How to apply

- Move the picture, not the camera: a view offset (three.js `setViewOffset`,
  normalised to shares of the screen's height) shifts everything equally, needs
  no collision check, keeps picking right and works from any camera distance. A
  narrower view window at the same centre is a zoom punch in the same call.
- For a blow, kick once in the blow's on-screen direction and let a damped
  spring (9 Hz or so, damping ratio about 0.4) bring it back; for ground shake,
  use a rattle of sines that dies away. Skip the spring on the first frame after
  a kick, so that frame shows all of it.
- Integrate the spring in fixed small steps, or one late frame throws the picture
  further than it was kicked.
- Measure it: project a fixed world point near the action each frame and log how
  many pixels it moved. Under about 5 px at 800 high reads as nothing.
