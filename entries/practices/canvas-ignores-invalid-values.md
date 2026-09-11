---
title: A canvas 2D context silently ignores an invalid value and keeps the previous one
tags: [canvas, graphics, frontend]
added: 2026-09-11
sources:
  - https://html.spec.whatwg.org/multipage/canvas.html#dom-context-2d-font
---

## Fact

Assigning a value the 2D context cannot parse is not an error and not a no-op on
the drawing — the property keeps whatever it held before, and drawing continues
with that. Nothing throws and nothing is logged.

```js
ctx.font = '700 40px monospace';
ctx.font = '600 13px var(--font), sans-serif';  // ctx.font is still 700 40px monospace
ctx.font = '13px';                              // incomplete shorthand: ignored
ctx.fillStyle = '#123456';
ctx.fillStyle = 'var(--nope)';                  // still #123456
ctx.lineWidth = 5;
ctx.lineWidth = -3;                             // still 5
```

CSS custom properties are the sharpest edge of this. `var(--x)` is resolved
against an element's computed style, and a canvas context has no element, so
every `var()` is a parse failure — even though the same string is valid in a
stylesheet and looks right in review.

## Why it matters

The symptom appears in unrelated code. Text drawn with a rejected `font` renders
in whatever font the *last successful* assignment set, which is usually a
different call site entirely — so a heading painted in 40px monospace looks like
a bug in the code that drew the heading, not in the line that failed.

It also survives refactoring in the wrong direction: moving a shared style into a
CSS variable is normally a safe change, and here it silently disables it.

## How to apply

- Build canvas font strings from JS constants, never from CSS variables:
  `const FONT = 'ui-sans-serif, system-ui, sans-serif'` then
  `ctx.font = \`600 ${size}px ${FONT}\``.
- Read the property back to test one: `ctx.font = x;` then compare `ctx.font`.
  An assignment that "did nothing" is the signature.
- Set every property a draw depends on at the start of that draw. Relying on
  inherited context state is what turns a rejected value into a distant symptom.
