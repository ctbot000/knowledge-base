---
title: A URL that differs only by its fragment does not reload the page
tags: [web, automation, browser]
added: 2026-09-19
sources:
  - https://html.spec.whatwg.org/multipage/browsing-the-web.html#scroll-to-the-fragment-identifier
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/hashchange_event
---

## Fact

When the current document's URL and the one being navigated to differ only after
the `#`, the browser performs a **same-document navigation**: it scrolls to the
fragment and fires `hashchange`. It does not request the document, and it does
not re-evaluate a single line of script.

So going from `/index.html` to `/index.html#chapter` after editing the source
runs the build that was already in memory. Cache headers are irrelevant here —
`Cache-Control: no-store` cannot help, because nothing is fetched at all.

## Why it matters

The page visibly jumps to the new section, so the navigation looks like it
happened, and the old code keeps running underneath. Anything checked afterwards
describes the previous build.

It bites hardest in an edit-then-verify loop: edit a module, navigate to
`#section`, screenshot, conclude the change had no effect. The natural next
suspect is caching, which sends the investigation into headers and hard reloads
that were never the problem.

ES modules fail the same way from the other side. A module is evaluated once per
document and kept in the module map, so re-importing the same URL hands back the
cached record rather than re-running the edited file.

## How to apply

- Force a real load by changing something other than the fragment — a throwaway
  query, `?r=2#section`, or an explicit `location.reload()`.
- Verify the code that is running, not the URL: read back a string or symbol the
  edit introduced before trusting the result of a check.
- Related, and easy to confuse with this: [[static-server-cache-hides-edits]].
