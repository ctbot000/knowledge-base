---
title: <center> computes to text-align: -webkit-center, which tables reset
tags: [css, html, layout]
added: 2026-09-23
---

## Fact

The HTML `<center>` element is not `text-align: center`. Browsers give it
`text-align: -webkit-center` (`-moz-center` in Gecko), a value that centres
inline content *and* centres block-level children that have a width — which is
how a page wrapped in `<center>` gets its whole layout table centred without
any `margin: 0 auto`.

That value inherits into ordinary descendants but stops at a table. Measured in
Chromium, inside a `<center>`: a `<p>`, `<div>` and `<span>` all compute to
`-webkit-center`, while the `<table>` computes to `start`, and its cells
inherit `start` from it.

## Why it matters

It is two rules, and implementing either half alone is visibly wrong. Treat
`<center>` as plain `text-align: center` and the old table-based layout it
wraps is no longer centred on the page. Let the centring inherit the way a
normal value would, and every cell of every table inside it comes out centred —
which is how a site whose text is left-aligned in a real browser renders as a
column of centred text instead.

## How to apply

- In a user-agent stylesheet, write both halves:

  ```css
  center { text-align: -webkit-center }
  table  { text-align: start }
  ```

- Treat `-webkit-center` and `-moz-center` as `center` when aligning inline
  content, and separately centre block children whose used width is smaller
  than the containing block.
- The same pair of rules is why `<table align="center">` still has to work:
  a presentational attribute outranks the user-agent stylesheet, so the
  `table { text-align: start }` rule must not be able to override it.
