---
title: A cache-busting query on a page does not bust the CSS and JS it links
tags: [web, caching, static-sites]
added: 2026-09-07
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching
---

## Fact

The stock static servers used during development — Python's `http.server`, most
`serve`-style one-liners — send no `Cache-Control` at all. Browsers then apply a
heuristic freshness lifetime and serve the file from cache without revalidating.

The reflex fix, appending `?v=<timestamp>` to the page URL, only creates a new
cache key **for the document**. The `<link>` and `<script>` URLs inside it are
unchanged, so their cached copies are reused. Reloading gets fresh HTML stapled
to a stale stylesheet and a stale script.

## Why it matters

The symptom is that an edit did not take effect, which reads as a bug in the
edit. New markup appears while the CSS that styles it does not, so the page
renders as unstyled fragments; or the HTML updates while the old script runs
against it and throws on elements it does not know about. Either way the
investigation starts in the code that was just changed, which is correct.

It also poisons automated checks silently: a test drives the previous build and
reports on behaviour that no longer exists in the working tree.

## How to apply

- Serve development assets with `Cache-Control: no-store`. For Python that is a
  four-line subclass overriding `end_headers`; most other dev servers have a
  flag.
- Confirm what is actually being executed before debugging a change that "did
  not apply" — read back a string or symbol the edit introduced, rather than
  trusting the reload.
- Version the subresource URLs, not the document, when a query string is the
  only lever available.
- A hard reload fixes it once; it does not fix the next edit, so fix the headers.
