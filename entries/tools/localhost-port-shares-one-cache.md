---
title: Two projects served on the same localhost port share one browser cache
tags: [web, caching, dev-server]
added: 2026-09-08
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching
---

## Fact

The HTTP cache is keyed by URL, and `http://localhost:8000` is one origin
whichever project's server happens to be listening. Start a different project on
a port an earlier one used, and the browser will serve the earlier project's
files from cache: a completely different app at `/`, and — worse — the previous
project's copy of any path both happen to use, like `/src/app.js` or
`/styles.css`.

## Why it matters

The error names your own code and looks impossible. An ES module import fails
with *"does not provide an export named X"* while the file on disk plainly
exports `X`; `curl` against the same URL returns the correct file, because curl
does not share the browser's cache. The investigation goes to the export, the
bundler, the module graph — none of which are involved.

The mixed state is the confusing part: fresh HTML with a stale sibling script,
or a page whose title belongs to a project you are not working on.

## How to apply

- Give each project its own port, and treat a familiar default (3000, 8000,
  8080) as shared ground.
- Serve development assets with `Cache-Control: no-store`, which fixes this and
  the related staleness in [[static-server-cache-hides-edits]].
- When the page looks like another app, check the document title before anything
  else, and fetch a path only the current project contains.
- Check for a service worker too: registration is scoped to the origin, so an
  old one left on that port intercepts requests for the new project as well.
