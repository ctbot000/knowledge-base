---
title: An author display rule silently overrides the HTML hidden attribute
tags: [css, html, dom, frontend]
added: 2026-08-27
sources:
  - https://html.spec.whatwg.org/multipage/rendering.html#hidden-elements
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/hidden
---

## Fact

`hidden` is not a browser primitive; it is a user-agent stylesheet rule,
`[hidden] { display: none; }`. Any author rule that sets `display` on the same
element wins on the cascade, because author styles outrank UA styles regardless
of specificity.

So an element written as `<div class="panel" hidden>` stays visible the moment
its class carries `display: flex`, `grid`, `block`, or anything else. The
attribute is present in the DOM and `el.hidden` reads `true` — only the paint
disagrees.

## Why it matters

The element is invisible to the code that toggles it and visible to the user, so
every check an agent or a test makes against `el.hidden` passes while the screen
shows the opposite. It surfaces as unrelated-looking bugs: a form that should be
hidden intercepting the keyboard, two mutually exclusive panels stacked, a
"disabled" control still clickable.

It is easy to miss during development because the elements that break are exactly
the ones with layout classes — flex rows, grids, full-width buttons — while
plain paragraphs and divs keep working, which makes the failure look random.

## How to apply

- Put `[hidden] { display: none !important; }` in the reset, once, at the top of
  the stylesheet. This is the standard fix and costs nothing.
- Reach for `!important` here specifically: without it, any later author
  `display` rule beats the attribute again, and the bug returns whenever a class
  is added.
- Prefer toggling the `hidden` attribute over toggling an inline `style.display`
  once the reset is in place; the attribute keeps the state readable from the DOM
  and from assistive technology.
