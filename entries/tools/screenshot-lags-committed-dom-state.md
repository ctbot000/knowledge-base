---
title: A screenshot can show a frame older than the DOM state you just set
tags: [testing, automation, browser, frontend]
added: 2026-09-02
---

## Fact

A screenshot captures whatever the compositor last painted, which is not
guaranteed to reflect DOM and CSS changes that have already been committed. A
capture taken immediately after a mutation can precede the paint that renders
it, and an occluded, backgrounded or otherwise hidden rendering surface may not
paint at all — so the returned image can be arbitrarily stale rather than merely
one frame behind.

`getComputedStyle()` and the DOM read the committed state directly and do not
wait on a paint, so they disagree with the image, and the DOM is the one telling
the truth.

## Why it matters

The failure is inverted from the usual one: the code is correct and the
*evidence* is wrong. A stale image shows the pre-change colour, the old label or
a half-finished transition, which reads as a broken selector or an unapplied
custom property. Time then goes into fixing styling that was never broken, and
the "fix" is validated against another stale capture.

It is worst exactly where automation tends to run — hidden panes and headless or
backgrounded surfaces — and invisible in manual testing, where a human always
looks at a surface that is visible and painting.

## How to apply

- Assert styling and text against the DOM, not the picture: read
  `getComputedStyle(el).stroke`, `el.textContent`, `aria-*` attributes.
- Keep screenshots for what they are good at — layout, overlap, overall
  composition — and treat a colour or text mismatch in one as unconfirmed until
  the DOM agrees.
- When an image must be trusted, make the surface visible first, then capture.
- A hidden surface may also refuse synthetic input entirely; see
  [[animation-lifetime-in-frames]] for the same throttling from the other side.
