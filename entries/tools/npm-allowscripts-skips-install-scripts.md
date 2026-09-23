---
title: npm 11 skips dependency install scripts that allowScripts has not approved, and still exits 0
tags: [npm, node, ci]
added: 2026-09-23
sources:
  - https://docs.npmjs.com/cli/commands/npm-install-scripts
---

## Fact

Recent npm (seen in 11.19) does not run dependencies' `preinstall`, `install`
or `postinstall` scripts unless the package is approved in the `allowScripts`
field of `package.json`. Unapproved scripts are skipped, the install exits 0,
and the only sign is a warning at the very end of the output ("package has
install scripts not yet covered by allowScripts").

## Why it matters

Whatever a script was meant to fetch or build is missing: Puppeteer's browser
download, native addons compiled by node-gyp. The failure surfaces later, at
runtime, and often only on a fresh machine or CI runner, because a cache left by
an older npm hides it locally.

## How to apply

- Approve once and commit the result:
  `npm install-scripts approve <pkg> --no-allow-scripts-pin`.
- Approvals are pinned to the installed version by default (`pkg@1.2.3`), so the
  next upgrade silently drops back to skipping; `--no-allow-scripts-pin` writes
  a name-only entry.
- `--allow-scripts` on the command line is an error in a project install; it is
  meant for `npx` and global installs.
- In CI, run the tool's own download step explicitly (for Puppeteer,
  `npx puppeteer browsers install chrome`); it is a no-op when already present.
