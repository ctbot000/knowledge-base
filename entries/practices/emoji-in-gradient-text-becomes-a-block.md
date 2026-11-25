---
title: An emoji inside gradient text (background-clip text with a transparent colour) turns into a solid block
tags: [css, emoji, background-clip, text]
added: 2026-11-26
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/background-clip
---

## Fact

Gradient headings are made with `background-clip: text` and `color: transparent`
(or `-webkit-text-fill-color: transparent`). The transparent fill also removes an
emoji's own colours, so what shows is the gradient clipped to the emoji's shape.
For the many emoji drawn as a framed picture that shape is a plain square or
rectangle. Seen in Chrome on macOS with Apple Color Emoji.

## Why it matters

Plain-letter headings look right in review, and the block only appears for a
title that happens to carry an emoji, often one that comes from data. It reads as
a missing-glyph box, which sends the search towards fonts.

## How to apply

Give the emoji a fill of its own; its glyph is then painted in its own colours
over the clipped gradient:

```html
<h2 class="gradient"><span class="icon">🌌</span> Midnight</h2>
```

```css
.gradient {
  background: linear-gradient(90deg, gold, hotpink);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.gradient .icon { color: #fff; }  /* any opaque colour */
```

With `-webkit-text-fill-color`, reset that property on the icon too. Where the
text comes as one string, split the emoji off it before rendering.
