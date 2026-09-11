---
title: A library's ESM build file can be a façade that imports siblings, so vendoring the named file alone breaks it
tags: [javascript, esm, vendoring]
added: 2026-09-11
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules
---

## Fact

The single build file a library's install instructions name is not necessarily
self-contained. Libraries increasingly split their ESM output and make that file
a re-export of its neighbours: three.js `three.module.min.js` is 330KB of real
code and still opens with `import{…}from"./three.core.min.js"`, a second 380KB
file nobody mentioned.

Copy only the named file into a `vendor/` directory and the page fails at load.
The misleading part is which name the failure carries:

```
GET /three.module.min.js  → 200 OK
GET /three.core.min.js    → 404
TypeError: Failed to fetch dynamically imported module: …/three.module.min.js
```

The thrown error names the file that loaded perfectly, because a module that
cannot resolve an import counts as failed. Only the network log names the file
that is actually missing.

## Why it matters

Every check that would normally confirm a good copy passes. The download
returned 200, the file is the expected size, and its export list contains every
symbol the code imports — they are re-exports. So the evidence says the vendored
file is fine, and the error agrees by pointing straight at it.

That sends the search to the import statement, the MIME type, the server config
and the module graph, none of which is wrong. The one signal that identifies it
is a 404 for a filename that appears nowhere in the project's own source.

## How to apply

- Before vendoring any ESM build, list what it pulls in:
  `grep -o 'from"[^"]*"' build.min.js | sort -u`. Copy every relative sibling it
  names, into the same directory, keeping the filenames.
- Prefer fetching the package's whole `build/` or `dist/` directory over the one
  file the README mentions.
- When a module fails to load, read the network log before the error message:
  the error names the importer, the log names the import.
- A bundled CDN URL resolves its own siblings, so it hides this — and trades it
  for a runtime dependency on that CDN.
