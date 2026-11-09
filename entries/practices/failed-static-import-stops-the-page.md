---
title: One static import that fails to load stops a page's whole module graph, so a module added before its server restarts blanks the page
tags: [javascript, esm, frontend, deployment]
added: 2026-11-09
sources:
  - https://html.spec.whatwg.org/multipage/webappapis.html#fetching-scripts
---

## Fact

A module script runs only once every module it imports, directly or through
others, has been fetched and linked. If one of them comes back 404, none of
the page's script runs: no exception from the page's own code, only a failed
request in the network panel and a page stuck on its loading state.

## Why it matters

A server that reads its client files from disk at request time, but routes
only the files it knew when it started, serves a freshly pulled entry script
and 404s the module that came with it. Every part of the page goes dead until
a restart, not just the new feature, and it reads as a broken release.

## How to apply

- Load a newly added, optional part on its own and run without it when it is
  missing: `const part = await import('./part.js').catch(() => null)`.
- Serve whatever is in the client folder rather than a list fixed at startup,
  or restart the server in the same step as the pull.
- When a page shows nothing after a pull, look for a 404 on a script before
  reading the page's code.
