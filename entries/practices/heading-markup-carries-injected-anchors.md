---
title: A rendered heading contains more than its text, so a contents list built from its markup nests a link inside a link
tags: [frontend, dom, static-sites]
added: 2026-09-18
sources:
  - https://github.com/bryanbraun/anchorjs
---

## Fact

Documentation themes routinely enhance headings after load: GitHub Pages' Primer
theme runs anchor.js, and most doc generators ship the same idea, appending an
`<a class="anchorjs-link" href="#id">` **inside** every `h2`/`h3`. A script that
builds a table of contents with

```js
a.innerHTML = heading.innerHTML;   // copies the injected anchor too
```

therefore puts an anchor inside its own anchor. The HTML parser tolerates what
the DOM API produced, so nothing throws and the list looks roughly right.

## Why it matters

The damage is quiet: invalid nested links, a doubled anchor count, a stray link
glyph in each entry, and a nested `href` that intercepts the click. Because the
enhancement runs on the deployed page and not in the source Markdown, none of it
reproduces when the generator's output is inspected on disk — only in a browser.

Order makes it intermittent, too. If the contents script happens to run before
the enhancement, the copy is clean; a change in script order later reintroduces
the bug with no edit to the code that broke.

## How to apply

Build navigation from a cleaned clone rather than from live markup:

```js
var text = heading.cloneNode(true);
text.querySelectorAll('.anchorjs-link, .headerlink, .anchor').forEach(function (a) {
  a.remove();
});
```

`textContent` is the blunt version — correct, but it drops the `<code>` and
`<em>` that make a heading readable. Assert `container.querySelectorAll('a a')`
is empty after building; it catches the whole class of problem in one line.
