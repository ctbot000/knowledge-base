---
title: Moving a close-up subject clear of a dialog by moving the camera sinks the camera into the ground
tags: [3d, camera, layout]
added: 2026-10-02
sources:
  - https://threejs.org/docs/#api/en/cameras/PerspectiveCamera.setViewOffset
---

## Fact

To show a subject a share `f` of the half-height above the centre of the screen
by translating the camera (or lowering its aim point, the same thing), the
camera must move down by `f · d · tan(fov/2)`: in proportion to its distance.
In a close-up that is about the subject's own height. On an upright phone (80°
vertical field, d = 3.4) clearing a sheet over the bottom 60 % takes 1.7 units,
and a camera at head height ends at the subject's feet.

A view offset (an off-axis frustum, what a shift lens does) slides the picture
by exactly `f` and leaves the camera where it was: the subject keeps its shape
and nothing new comes between them. Tilting the camera down instead puts the
subject off-axis, where a wide field stretches and keystones it.

## Why it matters

Lowering the aim works at follow distance on a wide screen, so it gets reused
for close-ups on phones and fails there in ways that look unrelated: a step in
the floor hides the subject, a collision ray cast from the lowered aim point
starts inside the ground and snaps the camera in, and the shot turns worm's-eye.

## How to apply

- three.js: `camera.setViewOffset(camera.aspect, 1, 0, share, camera.aspect, 1)`
  lifts the picture by `share` of the screen height; `clearViewOffset()` undoes
  it. `setViewOffset` sets `aspect = fullWidth / fullHeight`, so normalised
  arguments such as `(1, 1, …)` squash the picture.
- Picking through `unproject` and frustum culling stay right, since they read
  the same projection matrix; `updateProjectionMatrix()` keeps the offset.
- Measure the room from the dialog's layout box (`offsetTop`; a pop-in
  transform skews `getBoundingClientRect()`), and again on every resize.
- When the room is shorter than the subject, stand back as well: it fills
  `height / (2 · d · tan(fov/2))` of the screen. See also
  [[auto-framing-collapses-to-face-on]].
